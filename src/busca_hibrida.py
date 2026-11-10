"""Busca híbrida: combina a busca vetorial com BM25 (palavras-chave) por Reciprocal Rank Fusion.

A busca vetorial representa a pergunta inteira num único vetor. Em pedidos com várias condições
("inativos da carteira de campo com visita quinzenal") ele fica dominado por uma parte do pedido e perde
as outras. O BM25 pontua cada termo separadamente e recupera justamente as cláusulas que o usuário escreveu
de forma literal ("sem venda", "prospect", "ramo de atividade"). A fusão por posição (RRF) junta as duas
listas sem precisar calibrar as escalas de pontuação, que são incomparáveis entre si.
"""
from __future__ import annotations

import math
import re
from collections import Counter
from typing import Callable, Dict, List, Sequence

from gerar_explicacoes_gobr import canon

# palavras sem poder de discriminação neste domínio ("cliente" aparece em praticamente toda regra);
# "sem" e "nao" ficam de fora da lista porque fazem parte de cláusulas (sem venda, sem choque, nao agendar)
STOPWORDS = frozenset('a ao aos as com da das de do dos e em na nas no nos o os ou para pela pelo por que se um '
                      'uma cliente clientes deve devem ser'.split())


def tokenizar(texto: str) -> List[str]:
    out = []
    for t in re.findall(r'[a-z0-9]+', canon(texto)):
        if t in STOPWORDS:
            continue
        # plural simples: vendas → venda, inativos → inativo (o suficiente para o vocabulário do GoBR)
        out.append(t[:-1] if len(t) > 3 and t.endswith('s') else t)
    return out


class BM25:
    """Okapi BM25 sobre uma lista de textos fixa (k1 e b nos valores usuais da literatura)."""

    def __init__(self, textos: Sequence[str], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.docs = [Counter(tokenizar(t)) for t in textos]
        self.tamanhos = [sum(d.values()) for d in self.docs]
        self.media = (sum(self.tamanhos) / len(self.docs)) if self.docs else 0.0
        df = Counter(termo for d in self.docs for termo in d)
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def pontuar(self, consulta: str) -> List[float]:
        termos = [t for t in set(tokenizar(consulta)) if t in self.idf]
        scores = []
        for d, tam in zip(self.docs, self.tamanhos):
            s = 0.0
            norm = self.k1 * (1 - self.b + self.b * tam / self.media) if self.media else self.k1
            for t in termos:
                tf = d.get(t, 0)
                if tf:
                    s += self.idf[t] * tf * (self.k1 + 1) / (tf + norm)
            scores.append(s)
        return scores


def fundir_rrf(rankings: Sequence[Sequence[int]], k: int = 60) -> List[int]:
    """Reciprocal Rank Fusion: cada lista contribui 1/(k + posição); devolve os índices em ordem decrescente."""
    pontos: Dict[int, float] = {}
    for ranking in rankings:
        for pos, i in enumerate(ranking, 1):
            pontos[i] = pontos.get(i, 0.0) + 1.0 / (k + pos)
    return sorted(pontos, key=lambda i: (-pontos[i], i))


class BuscaHibrida:
    """Envolve uma busca vetorial e devolve os resultados no mesmo formato, reordenados pela fusão com o BM25.

    `vetorial(consulta, n)` deve devolver dicts com 'id' e 'score' (similaridade de cosseno), em ordem.
    `documentos` são os mesmos dicts sem score, e `textos` os textos usados pelo BM25, na mesma ordem.
    O 'score' de cada resultado continua sendo a similaridade de cosseno, para manter o significado no prompt.
    """

    def __init__(self, vetorial: Callable[[str, int], List[Dict]], documentos: Sequence[Dict],
                 textos: Sequence[str], profundidade: int = 50, k_rrf: int = 60):
        if len(documentos) != len(textos):
            raise ValueError('documentos e textos com tamanhos diferentes')
        self.vetorial = vetorial
        self.documentos = list(documentos)
        self.posicao = {d['id']: i for i, d in enumerate(self.documentos)}
        self.bm25 = BM25(textos)
        self.profundidade = profundidade
        self.k_rrf = k_rrf

    def buscar(self, consulta: str, k: int) -> List[Dict]:
        if k <= 0:
            return []
        todos = self.vetorial(consulta, len(self.documentos))
        cosseno = {r['id']: r['score'] for r in todos}
        rank_vetorial = [self.posicao[r['id']] for r in todos[:self.profundidade]]
        lexico = self.bm25.pontuar(consulta)
        rank_lexico = [i for i in sorted(range(len(lexico)), key=lambda i: (-lexico[i], i))
                       if lexico[i] > 0][:self.profundidade]
        ordem = fundir_rrf([rank_vetorial, rank_lexico], self.k_rrf)[:k]
        return [{**self.documentos[i], 'score': cosseno[self.documentos[i]['id']]} for i in ordem]
