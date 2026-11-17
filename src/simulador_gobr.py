"""Simulador semântico de regras `parametros` do GoBR, para verificar regras geradas e comparar com um gabarito.

Comparar regras pelo texto engana: `recencia de positivacao em 90 dias` depois de uma regra de 60 dias pega os mesmos
clientes que `recencia de positivacao em 90 dias e fora da recencia de positivacao em 60 dias`, e uma regra sem filtro
no fim do arquivo equivale a `fora da recencia de positivacao em 90 dias` se as anteriores cobrem o resto. O que
importa é a decisão para cada cliente.

O simulador aplica as regras como o manual descreve (seção 7.6, "Sem repetição: clientes parametrizados em uma regra
anterior não são reprocessados por regras subsequentes. A ordem importa."): cada cliente recebe a ação da 1ª regra
cujas condições ele satisfaz. Os clientes são sintéticos e cobrem as dimensões que as regras comerciais usam:

    dias desde a última compra: nunca comprou (prospect) ou 0…400 · baixado na Receita · inadimplente · rota na semana
    · curva A (exemplo de condição própria, que no agente é escrita pelo modelo com RAG, sem molde)

Só um subconjunto da linguagem é interpretado (o das regras comerciais de recência, ciclo de vida e bloqueios). Uma
condição fora dele torna a regra "não verificável", e isso é informado em vez de adivinhado.

Convenções (assumidas; o manual não define os limites):
- `recencia de positivacao em N dias`: comprou há no máximo N dias (d ≤ N); prospects não satisfazem;
- `fora da recencia de positivacao em N dias`: já comprou, mas há mais de N dias (d > N); prospects não satisfazem;
- `recencia de positivacao entre A dias e B dias`: A ≤ d ≤ B;
- `inatividade de N dias`: já comprou e está há pelo menos N dias sem comprar (d ≥ N);
- `global` / `do vendedor`: tratados como iguais (um único vendedor por cliente na simulação).
"""
from __future__ import annotations

import itertools
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple

from gerar_explicacoes_gobr import parse_blocks

DIAS_MAXIMO = 400


@dataclass(frozen=True)
class Cliente:
    dias_sem_compra: Optional[int]  # None = nunca comprou (prospect)
    baixado: bool = False
    inadimplente: bool = False
    rota_semana: bool = False
    curva_a: bool = False


def clientes_sinteticos(dias_maximo: int = DIAS_MAXIMO) -> List[Cliente]:
    dias: List[Optional[int]] = [None, *range(0, dias_maximo + 1)]
    return [Cliente(d, b, i, r, a) for d, b, i, r, a in itertools.product(dias, *([[False, True]] * 4))]


class CondicaoNaoSuportada(ValueError):
    """Trecho de condição que o simulador não sabe interpretar."""


def _normalizar(s: str) -> str:
    s = unicodedata.normalize('NFKD', s.lower())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'\s+', ' ', s).strip()


Predicado = Callable[[Cliente], bool]
_ESCOPO = r'(?: global| do vendedor| da empresa)?'
_DIAS = r'(\d+) dias?'


def _rec_em(n: int) -> Predicado:
    return lambda c: c.dias_sem_compra is not None and c.dias_sem_compra <= n


def _fora_em(n: int) -> Predicado:
    return lambda c: c.dias_sem_compra is not None and c.dias_sem_compra > n


def _rec_entre(a: int, b: int) -> Predicado:
    return lambda c: c.dias_sem_compra is not None and a <= c.dias_sem_compra <= b


# (padrão, fábrica do predicado a partir dos grupos). A ordem importa: os mais específicos primeiro.
_PADROES: List[Tuple[re.Pattern, Callable[..., Predicado]]] = [
    (re.compile(rf'fora da recencia de positivacao{_ESCOPO} entre {_DIAS} e {_DIAS}'),
     lambda a, b: (lambda c, p=_rec_entre(int(a), int(b)): c.dias_sem_compra is not None and not p(c))),
    (re.compile(rf'recencia de positivacao{_ESCOPO} entre {_DIAS} e {_DIAS}'), lambda a, b: _rec_entre(int(a), int(b))),
    (re.compile(rf'fora da recencia de positivacao{_ESCOPO} em {_DIAS}'), lambda n: _fora_em(int(n))),
    (re.compile(rf'recencia de positivacao{_ESCOPO} em {_DIAS}'), lambda n: _rec_em(int(n))),
    (re.compile(rf'inatividade(?: global)? de {_DIAS}'),
     lambda n: (lambda c, n=int(n): c.dias_sem_compra is not None and c.dias_sem_compra >= n)),
    (re.compile(r'no ciclo de vida prospects? com (?:a empresa|o vendedor)'), lambda: (lambda c: c.dias_sem_compra is None)),
    (re.compile(r'(?:prospects|sem venda)(?: da empresa| do vendedor)?'), lambda: (lambda c: c.dias_sem_compra is None)),
    (re.compile(r'status na receita federal definido como baixada'), lambda: (lambda c: c.baixado)),
    (re.compile(r'inadimplentes'), lambda: (lambda c: c.inadimplente)),
    (re.compile(r'adimplentes'), lambda: (lambda c: not c.inadimplente)),
    (re.compile(r'data da rota na semana'), lambda: (lambda c: c.rota_semana)),
    (re.compile(r'curva a com (?:a empresa|o vendedor)'), lambda: (lambda c: c.curva_a)),
]
_NEGACAO = re.compile(r'(?:nao|não) ')
_CONECTOR = re.compile(r' e ')


def interpretar_condicoes(texto: str) -> List[Predicado]:
    """Converte o texto de `quando …` / `e …` (sem a palavra inicial) em predicados ligados por "e"."""
    resto = _normalizar(texto)
    out: List[Predicado] = []
    while resto:
        negar = bool(_NEGACAO.match(resto))
        if negar:
            resto = resto[_NEGACAO.match(resto).end():]
        for padrao, fabrica in _PADROES:
            m = padrao.match(resto)
            if m and (m.end() == len(resto) or _CONECTOR.match(resto, m.end())):
                p = fabrica(*m.groups())
                out.append((lambda c, p=p: not p(c)) if negar else p)
                resto = resto[m.end():]
                break
        else:
            raise CondicaoNaoSuportada(resto)
        m = _CONECTOR.match(resto)
        if m:
            resto = resto[m.end():]
    return out


_FREQ_FIXA = {'diaria()': 1, 'semanal()': 7, 'quinzenal()': 15, 'mensal()': 30, 'bimestral()': 60,
              'trimestral()': 90, 'semestral()': 180, 'anual()': 365}


def interpretar_acao(clausula: str) -> Optional[str]:
    """'nao agendar', 'frequencia N' ou None se a cláusula não define frequência nem bloqueio."""
    s = _normalizar(clausula)
    if s in ('nao agendar', 'não agendar'):
        return 'nao agendar'
    m = re.fullmatch(r'frequencia de (\d+) dias?', s)
    if m:
        return f'frequencia {int(m.group(1))}'
    m = re.fullmatch(r'frequencia (\w+\(\))', s)
    if m and m.group(1) in _FREQ_FIXA:
        return f'frequencia {_FREQ_FIXA[m.group(1)]}'
    if s.startswith('frequencia'):
        return 'frequencia ?'
    return None


@dataclass
class RegraSimulada:
    nome: str
    condicoes: List[Predicado]
    acao: str
    nao_suportado: List[str] = field(default_factory=list)

    @property
    def verificavel(self) -> bool:
        return not self.nao_suportado and self.acao not in ('', 'frequencia ?')


def regras_do_texto(gobr: str) -> List[RegraSimulada]:
    out = []
    for b in parse_blocks(gobr):
        if b['type'] != 'parametros':
            continue
        condicoes: List[Predicado] = []
        acoes: List[str] = []
        nao_suportado: List[str] = []
        for cl in b['clauses']:
            n = _normalizar(cl)
            if n.startswith(('do time', 'da carteira', 'da segmentacao')):
                continue
            m = re.match(r'(quando|e) (.*)', n)
            if m:
                try:
                    condicoes += interpretar_condicoes(m.group(2))
                except CondicaoNaoSuportada as e:
                    nao_suportado.append(str(e))
                continue
            acao = interpretar_acao(cl)
            if acao:
                acoes.append(acao)
        acao = acoes[0] if len(acoes) == 1 else ('' if not acoes else 'conflito: ' + ', '.join(acoes))
        out.append(RegraSimulada(b['name'], condicoes, acao, nao_suportado))
    return out


SEM_REGRA = 'sem regra'


def decidir(regras: Sequence[RegraSimulada], cliente: Cliente) -> Tuple[str, Optional[int]]:
    """(ação, índice da regra) da 1ª regra que o cliente satisfaz; regra não verificável devolve ação '?'."""
    for i, r in enumerate(regras):
        if r.nao_suportado:
            return '?', i  # não dá para saber se o cliente passaria por ela
        if all(p(cliente) for p in r.condicoes):
            return r.acao, i
    return SEM_REGRA, None


def simular(regras: Sequence[RegraSimulada], clientes: Optional[Sequence[Cliente]] = None) -> Dict[Cliente, Tuple[str, Optional[int]]]:
    clientes = clientes_sinteticos() if clientes is None else clientes
    return {c: decidir(regras, c) for c in clientes}


def descrever_cliente(c: Cliente) -> str:
    partes = ['prospect (nunca comprou)' if c.dias_sem_compra is None else f'{c.dias_sem_compra} dias sem comprar']
    if c.baixado:
        partes.append('baixado na Receita')
    if c.inadimplente:
        partes.append('inadimplente')
    if c.rota_semana:
        partes.append('com rota na semana')
    if c.curva_a:
        partes.append('curva A')
    return ', '.join(partes)


def _faixas(dias: Iterable[Optional[int]]) -> str:
    """Resume dias em faixas: [None, 0, 1, 2, 5] → 'prospect, 0–2, 5'."""
    vals = sorted({d for d in dias if d is not None})
    partes = ['prospect'] if any(d is None for d in dias) else []
    i = 0
    while i < len(vals):
        j = i
        while j + 1 < len(vals) and vals[j + 1] == vals[j] + 1:
            j += 1
        partes.append(str(vals[i]) if i == j else f'{vals[i]}–{vals[j]}')
        i = j + 1
    return ', '.join(partes)


@dataclass
class Comparacao:
    total: int
    iguais: int
    divergencias: List[Tuple[Cliente, str, str]]  # (cliente, esperado, obtido)
    indeterminados: int

    @property
    def concordancia(self) -> float:
        return self.iguais / self.total if self.total else 0.0

    def resumo(self, limite: int = 6) -> List[str]:
        """Divergências agrupadas por (flags, esperado, obtido), com as faixas de dias."""
        grupos: Dict[Tuple, List[Optional[int]]] = {}
        for c, esp, obt in self.divergencias:
            chave = (c.baixado, c.inadimplente, c.rota_semana, c.curva_a, esp, obt)
            grupos.setdefault(chave, []).append(c.dias_sem_compra)
        linhas = []
        for (b, i, r, a, esp, obt), dias in sorted(grupos.items(), key=lambda kv: -len(kv[1]))[:limite]:
            flags = [n for n, v in (('baixado', b), ('inadimplente', i), ('rota na semana', r), ('curva A', a))
                     if v] or ['sem flags']
            linhas.append(f'clientes {"/".join(flags)} com dias sem compra = {_faixas(dias)}: '
                          f'esperado "{esp}", obtido "{obt}"')
        return linhas


def comparar(esperado: Sequence[RegraSimulada], obtido: Sequence[RegraSimulada],
             clientes: Optional[Sequence[Cliente]] = None) -> Comparacao:
    clientes = clientes_sinteticos() if clientes is None else clientes
    iguais, indeterminados, div = 0, 0, []
    for c in clientes:
        a, _ = decidir(esperado, c)
        b, _ = decidir(obtido, c)
        if '?' in (a, b):
            indeterminados += 1
        if a == b and a != '?':
            iguais += 1
        else:
            div.append((c, a, b))
    return Comparacao(len(clientes), iguais, div, indeterminados)


def distribuicao(regras: Sequence[RegraSimulada], clientes: Optional[Sequence[Cliente]] = None) -> Counter:
    return Counter(a for a, _ in simular(regras, clientes).values())
