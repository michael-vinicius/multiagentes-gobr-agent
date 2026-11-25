from __future__ import annotations

import pytest

from simulador_gobr import (SEM_REGRA, Cliente, CondicaoNaoSuportada, comparar, decidir, interpretar_acao,
                            interpretar_condicoes, regras_do_texto)

ARQUIVO = '''version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Baixados":
    do time("televendas")
    quando status na receita federal definido como baixada
    nao agendar

parametros "Prospects":
    do time("televendas")
    quando no ciclo de vida prospect com a empresa
    frequencia de 7 dias

parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 60 dias
    frequencia de 14 dias

parametros "Risco":
    do time("televendas")
    quando recencia de positivacao em 90 dias
    frequencia de 7 dias

parametros "Inativos":
    do time("televendas")
    frequencia de 28 dias
'''


def test_primeira_regra_que_pega_o_cliente_vale():
    regras = regras_do_texto(ARQUIVO)
    assert decidir(regras, Cliente(30))[0] == 'frequencia 14'
    assert decidir(regras, Cliente(60))[0] == 'frequencia 14'  # limite: "em 60 dias" inclui o 60
    assert decidir(regras, Cliente(61))[0] == 'frequencia 7'  # já passou pelos ativos
    assert decidir(regras, Cliente(91))[0] == 'frequencia 28'  # regra final sem filtro
    assert decidir(regras, Cliente(None))[0] == 'frequencia 7'  # prospect
    assert decidir(regras, Cliente(10, baixado=True))[0] == 'nao agendar'  # bloqueio vem antes


def test_formas_equivalentes_decidem_igual():
    reescrito = ARQUIVO.replace('    quando recencia de positivacao em 90 dias\n',
                                '    quando recencia de positivacao global em 90 dias\n'
                                '    e fora da recencia de positivacao do vendedor em 60 dias\n')
    reescrito = reescrito.replace('    do time("televendas")\n    frequencia de 28 dias',
                                  '    do time("televendas")\n    quando fora da recencia de positivacao em 90 dias\n'
                                  '    frequencia de 28 dias')
    cmp = comparar(regras_do_texto(ARQUIVO), regras_do_texto(reescrito))
    assert cmp.concordancia == 1.0 and not cmp.divergencias


def test_diferenca_aparece_agrupada_por_faixa():
    outro = ARQUIVO.replace('em 60 dias', 'em 45 dias')
    cmp = comparar(regras_do_texto(ARQUIVO), regras_do_texto(outro))
    assert cmp.divergencias
    resumo = ' | '.join(cmp.resumo())
    assert '46–60' in resumo and 'esperado "frequencia 14", obtido "frequencia 7"' in resumo


def test_condicoes_compostas_e_negacao():
    preds = interpretar_condicoes('recencia de positivacao entre 30 dias e 60 dias e inadimplentes')
    assert len(preds) == 2
    assert all(p(Cliente(45, inadimplente=True)) for p in preds)
    assert not all(p(Cliente(45)) for p in preds)
    (nao_rota,) = interpretar_condicoes('nao data da rota na semana')
    assert nao_rota(Cliente(5)) and not nao_rota(Cliente(5, rota_semana=True))
    (adimplente,) = interpretar_condicoes('adimplentes')
    assert adimplente(Cliente(5)) and not adimplente(Cliente(5, inadimplente=True))


def test_prospect_nao_satisfaz_filtros_de_recencia():
    for texto in ('recencia de positivacao em 30 dias', 'fora da recencia de positivacao em 30 dias',
                  'inatividade de 30 dias'):
        (p,) = interpretar_condicoes(texto)
        assert not p(Cliente(None))


def test_condicao_desconhecida_torna_a_regra_nao_verificavel():
    with pytest.raises(CondicaoNaoSuportada):
        interpretar_condicoes('ramo de atividade igual("FARMACIA")')
    regras = regras_do_texto('parametros "A":\n    do time("t")\n    quando ramo de atividade igual("FARMACIA")\n'
                             '    frequencia de 7 dias')
    assert not regras[0].verificavel
    assert decidir(regras, Cliente(10))[0] == '?'


@pytest.mark.parametrize('clausula, acao', [
    ('nao agendar', 'nao agendar'), ('frequencia de 21 dias', 'frequencia 21'),
    ('frequencia quinzenal()', 'frequencia 15'), ('frequencia semanal()', 'frequencia 7'),
    ('frequencia do vendedor ou de 35 dias', 'frequencia ?'), ('preferencia nas segundas', None),
])
def test_acoes(clausula, acao):
    assert interpretar_acao(clausula) == acao


def test_cliente_que_nao_cai_em_nenhuma_regra():
    regras = regras_do_texto('parametros "A":\n    do time("t")\n    quando recencia de positivacao em 30 dias\n'
                             '    frequencia de 7 dias')
    assert decidir(regras, Cliente(31))[0] == SEM_REGRA
