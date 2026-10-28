from __future__ import annotations

import re
from pathlib import Path

from buscar_explicacoes import IndiceExplicacoes

# Cada consulta é uma descrição livre; o acerto é medido pela DSL do resultado conter o padrão esperado,
# porque muitas regras equivalentes existem em arquivos diferentes.
CASOS = [
    ('não visitar clientes que são filiais', r'filial[\s\S]*nao agendar'),
    ('prospect que nunca fez pedido deve ser atendido', r'ciclo de vida prospect'),
    ('clientes sem comprar há mais de 90 dias', r'fora da recencia de positivacao em 90 dias'),
    ('clientes inativos usam a frequência média da empresa', r'frequencia de inativos da empresa'),
    ('clientes ativos usam a frequência média da empresa', r'frequencia de ativos da empresa'),
    ('cliente que comprou entre 7 e 30 dias atrás', r'recencia de positivacao[^\n]*entre 7 dias e 30 dias'),
    ('visitar clientes toda semana', r'frequencia (semanal\(\)|de 7 dias)'),
    ('atendimento mensal dos clientes', r'frequencia (mensal\(\)|de 30 dias)'),
    ('prospect que fez só um pedido e não comprou mais', r'unica compra'),
    ('dar preferência de atendimento aos dias úteis', r'preferencia'),
    ('parametrização marcada como fixa', r'\bfixo\b'),
    ('clientes do ramo consumidor final', r'CONS\. FINAL'),
]


def avaliar(indice: IndiceExplicacoes, k: int) -> None:
    hits1 = hitsk = 0
    for consulta, padrao in CASOS:
        res = indice.buscar(consulta, k)
        ok = [bool(re.search(padrao, r['dsl_original'] or '', re.I)) for r in res]
        hits1 += ok[0]
        hitsk += any(ok)
        rank = ok.index(True) + 1 if any(ok) else '-'
        print(f'[{rank}] {consulta}  →  {res[0]["nome_regra"]}')
    n = len(CASOS)
    print(f'\nacerto@1: {hits1}/{n}   acerto@{k}: {hitsk}/{n}')


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='Avalia a busca semântica com consultas de referência.')
    ap.add_argument('-k', type=int, default=5)
    ap.add_argument('--indice', type=Path, default=Path('index'))
    ap.add_argument('--explicadas', type=Path, default=Path('data/parametrizacoes_explicadas.jsonl'))
    args = ap.parse_args()
    avaliar(IndiceExplicacoes(args.indice, args.explicadas), args.k)
