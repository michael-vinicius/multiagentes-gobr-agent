from __future__ import annotations

from pathlib import Path

from buscar_manual import IndiceManual

# Cada consulta é uma pergunta ou descrição livre; o acerto é medido pela seção do manual que contém a resposta.
# Algumas respostas aparecem em mais de uma seção (a tabela de referência e um exemplo de uso), e todas contam.
CASOS = [
    ('dar preferência de visita na segunda e na terça', {'7.2', '7.3.2', '7.3.3'}),
    ('dia prioritário com intensidade maior, normal ou menor', {'7.3.3'}),
    ('tirar clientes inativos da agenda', {'7.3.4'}),
    ('manter a frequência que o vendedor já configurou para o cliente', {'7.3.5', '7.4.3'}),
    ('quais frequências fixas existem, como quinzenal ou mensal', {'7.4.1'}),
    ('clientes que não compram há mais de 90 dias', {'6.1', '6.2', '4.6.1'}),
    ('clientes com pendências financeiras ou sem crédito', {'6.3'}),
    ('clientes que estão na curva A de faturamento', {'6.7'}),
    ('aplicar a regra apenas na primeira semana do mês', {'5.4'}),
    ('rodar a parametrização somente de segunda a sexta', {'5.3', '7.3.7'}),
    ('impedir que o televendas ligue no mesmo dia em que o vendedor de campo visita', {'7.3.8'}),
    ('o cliente só pode entrar na agenda a partir da segunda semana do mês', {'7.3.9', '7.5'}),
    ('incluir o cliente na rota presencial e travar a parametrização', {'7.3.10'}),
    ('montar um time com os televendas de um supervisor específico', {'3.1', '3.3', '3.3.1', '3.4'}),
    ('diferença entre carteira exclusiva e carteira livre', {'4.2', '4.4'}),
    ('não atender clientes que são filiais', {'6.5'}),
    ('como começa um arquivo de regras e qual a ordem dos blocos', {'2.2', '10', '3.1'}),
    ('mandar o alerta por WhatsApp para o gestor', {'8.6', '8.7', '8.2'}),
    ('quais variáveis posso usar no texto do alerta', {'8.5', '8.5.1', '8.5.2', '8.5.3', '8.5.4'}),
    ('um cliente que já foi parametrizado por uma regra anterior é processado de novo?', {'7.6'}),
    ('clientes que nunca compraram nada', {'6.1', '6.7'}),
    ('última visita entre 10 e 90 dias atrás', {'6.2', '4.3.2'}),
    ('apagar as parametrizações do GoBR antes de aplicar as novas regras', {'7.3.11'}),
    ('em que formato escrevo uma data na regra', {'10', '6.13'}),
]


def avaliar(indice: IndiceManual, k: int) -> None:
    hits1 = hitsk = 0
    for consulta, esperadas in CASOS:
        res = indice.buscar(consulta, k)
        ok = [r['secao'] in esperadas for r in res]
        hits1 += ok[0]
        hitsk += any(ok)
        rank = ok.index(True) + 1 if any(ok) else '-'
        print(f'[{rank}] {consulta}  →  {res[0]["titulo"]}')
    n = len(CASOS)
    print(f'\nacerto@1: {hits1}/{n}   acerto@{k}: {hitsk}/{n}')


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='Avalia a busca no manual com consultas de referência.')
    ap.add_argument('-k', type=int, default=5)
    ap.add_argument('--indice', type=Path, default=Path('index/manual'))
    args = ap.parse_args()
    avaliar(IndiceManual(args.indice), args.k)
