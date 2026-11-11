"""Catálogo das cláusulas GoBR conhecidas, para conferir cláusula a cláusula a regra gerada pelo modelo.

O catálogo junta três fontes:
- as cláusulas das 1700 regras reais (data/parametrizacoes_explicadas.jsonl);
- os moldes das tabelas de referência do manual (`inatividade de <<N>> dias`), convertidos em padrões;
- as cláusulas dos exemplos de código do manual.

As cláusulas são comparadas pelo seu molde: sem acentos, com números trocados por N, textos entre aspas por S,
e quebradas em partes nas conjunções " e " (os dois lados são quebrados do mesmo jeito, então
"recencia de positivacao entre N dias e N dias" continua batendo). Uma parte que não aparece em nenhuma fonte
indica sintaxe inventada, como `quando nao choque na rota`.

Só as condições (`quando …` / `e …`) e os nomes das fontes de clientes são conferidos. As ações (frequência,
preferência, `sem choque`, `restrito`) são composicionais, com cascatas de alternativas
(`frequencia do vendedor ou de qualquer vendedor ou de 35 dias`); conferi-las por partes acusou 8 das 43 ações
válidas dos exemplos do manual quando o catálogo não conhecia esses exemplos, enquanto nenhuma condição válida
foi acusada.
"""
from __future__ import annotations

import difflib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List, Optional, Pattern, Set

from gerar_explicacoes_gobr import canon, classify_clause, parse_blocks

_PREFIXO = re.compile(r'^(quando|e)\s+')
_ARGS_TEXTO = re.compile(r'\(\s*"[^)]*\)')
_NUMERO = re.compile(r'\d+(?:[.,]\d+)*')
_MARCADOR = re.compile(r'<<[^>]*>>|\.\.\.|…')


def molde(clausula: str) -> str:
    s = re.sub(r'\s+\(', '(', re.sub(r'\s+', ' ', canon(clausula)))
    s = _ARGS_TEXTO.sub('(S)', s)
    s = re.sub(r'"[^"]*"', 'S', s)
    return _NUMERO.sub('N', s).strip()


def partes(clausula: str) -> List[str]:
    corpo = _PREFIXO.sub('', molde(clausula))
    return [p.strip() for p in re.split(r'\s+e\s+', corpo) if p.strip()]


def _padrao(entrada_do_manual: str) -> Optional[Pattern]:
    """`inatividade de <<N>> dias` → regex que aceita qualquer valor no lugar do marcador."""
    s = re.sub(r'\s+', ' ', canon(entrada_do_manual)).replace('(...)', '(S)').replace('(…)', '(S)')
    s = _ARGS_TEXTO.sub('(S)', s)
    pedacos = _MARCADOR.split(s)
    if len(pedacos) == 1:
        return None
    if len(re.sub(r'[^a-z]', '', ''.join(pedacos))) < 4:
        raise ValueError(f'molde genérico demais para virar padrão: {entrada_do_manual!r}')
    return re.compile('.+?'.join(re.escape(_NUMERO.sub('N', p)) for p in pedacos))


@dataclass
class Catalogo:
    partes: Set[str] = field(default_factory=set)
    padroes: List[Pattern] = field(default_factory=list)
    condicoes: Set[str] = field(default_factory=set)
    nomes_de_fonte: Set[str] = field(default_factory=set)

    def adicionar_dsl(self, dsl: str) -> None:
        for bloco in parse_blocks(dsl):
            for cl in bloco['clauses']:
                self.partes.update(partes(cl))
                tipo = classify_clause(cl)
                if tipo == 'condition':
                    self.condicoes.update(partes(cl))
                elif tipo == 'target':
                    self.nomes_de_fonte.update(canon(v) for v in re.findall(r'"([^"]+)"', cl))

    def adicionar_tabela(self, entrada: str) -> None:
        try:
            p = _padrao(entrada)
        except ValueError:
            return  # um molde só com marcador (`<<N>>`) aceitaria qualquer coisa
        if p:
            self.padroes.append(p)
        else:
            self.partes.update(partes(entrada))

    def conhece(self, parte: str) -> bool:
        return parte in self.partes or any(p.fullmatch(parte) for p in self.padroes)

    def parecida(self, parte: str) -> Optional[str]:
        achadas = difflib.get_close_matches(parte, sorted(self.partes), n=1, cutoff=0.6)
        return achadas[0] if achadas else None

    def problemas(self, clausulas: Iterable[str]) -> List[str]:
        out = []
        for cl in clausulas:
            tipo = classify_clause(cl)
            desconhecidas = [p for p in partes(cl) if not self.conhece(p)] if tipo == 'condition' else []
            if desconhecidas:
                dicas = [d for d in map(self.parecida, desconhecidas) if d]
                dica = f' (a forma conhecida mais parecida é "{dicas[0]}")' if dicas else ''
                out.append(f'condição fora do manual e das regras reais: "{cl.strip()}"{dica}')
            if tipo == 'target':
                for nome in re.findall(r'"([^"]+)"', cl):
                    c = canon(nome)
                    if c in self.condicoes and c not in self.nomes_de_fonte:
                        out.append(f'"{nome}" é um filtro, não o nome de uma fonte de clientes: use '
                                   f'`quando {nome}` depois da fonte, em "{cl.strip()}"')
        return out


_CODIGO = re.compile(r'```gobr\n(.*?)```', re.S)
_LINHA_TABELA = re.compile(r'^\|\s*`([^`]+)`\s*\|', re.M)


def carregar_catalogo(explicadas: Path = Path('data/parametrizacoes_explicadas.jsonl'),
                      chunks_manual: Optional[Path] = Path('index/manual/chunks.jsonl')) -> Catalogo:
    cat = Catalogo()
    with explicadas.open(encoding='utf-8') as f:
        for linha in f:
            if linha.strip():
                cat.adicionar_dsl(json.loads(linha)['dsl_original'])
    if chunks_manual and chunks_manual.exists():
        with chunks_manual.open(encoding='utf-8') as f:
            for linha in f:
                if not linha.strip():
                    continue
                texto = json.loads(linha)['texto']
                for codigo in _CODIGO.findall(texto):
                    cat.adicionar_dsl(codigo)
                for entrada in _LINHA_TABELA.findall(texto):
                    cat.adicionar_tabela(entrada)
    return cat
