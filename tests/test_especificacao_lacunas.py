from __future__ import annotations

from types import SimpleNamespace

import pytest

from especificacao import (BlocoPlano, Especificacao, Item, classificar_filtros, conferir_especificacao,
                           conferir_filtros, interpretar, molde, montar_arquivo, numerar_descricao,
                           ramos_da_descricao)
from lacunas import Decisao, aplicar_sugestoes, interpretar_respostas, planejar, revisar
from rag import validar_dsl
from simulador_gobr import Cliente, decidir, regras_do_texto

DESCRICAO = '''Título: Regra Teste
1. Ativos → Clientes com compra nos últimos 30 dias → 14 dias → Somente clientes fora da rota da semana
2. Risco → Compraram nos últimos 60 dias mas estão a 30 dias sem comprar → 7 dias → Somente clientes fora da rota da semana
3. Inativos → Compraram nos últimos 120 dias mas estão a 60 dias sem comprar → 21 dias → Somente clientes fora da rota da semana
4. Prospects → Ciclo de vida prospect → 14 dias → Somente clientes fora da rota da semana
5. Não agendar inadimplentes
6. Capacidade: 30 clientes por dia (televendas)'''


def espec() -> Especificacao:
    r = ramos_da_descricao(DESCRICAO)
    return Especificacao('Regra Teste', 'televendas', '', [
        Item('Ativos', 'frequencia', 1, 14, 30, None, [], ['rota_semana'], [], r[1]),
        Item('Risco', 'frequencia', 2, 7, 60, 30, [], ['rota_semana'], [], r[2]),
        Item('Inativos', 'frequencia', 3, 21, 120, 60, [], ['rota_semana'], [], r[3]),
        Item('Prospects', 'frequencia', 4, 14, None, None, ['prospect'], ['rota_semana'], [], r[4]),
        Item('Não agendar inadimplentes', 'nao_agendar', 5, None, None, None, ['inadimplente'], [], [], r[5]),
        Item('Capacidade', 'fora_do_escopo', 6, None, None, None, [], [], [], r[6]),
    ])


def test_numerar_descricao_livre():
    assert numerar_descricao('Ativos a cada 14 dias\n\n- Prospects a cada 7 dias') == \
        '1. Ativos a cada 14 dias\n2. Prospects a cada 7 dias'
    assert numerar_descricao(DESCRICAO) == DESCRICAO


def test_conferencia_descarta_numero_inventado_e_corrige_faixa_invertida():
    e = Especificacao('t', 'nao_informado', '', [
        Item('A', 'frequencia', 1, 10, 30, None),  # 10 não está no texto
        Item('B', 'frequencia', 2, 7, 30, 60),  # faixa invertida
    ])
    ramos = {1: 'A → compraram nos últimos 30 dias → 14 dias', 2: 'B → entre 30 e 60 dias → 7 dias',
             3: 'C → algo que o modelo ignorou'}
    conferir_especificacao(e, ramos, 'atendimento por televendas')
    a, b = e.itens
    assert a.frequencia_dias is None and b.comprou_nos_ultimos_dias == 60 and b.sem_comprar_ha_mais_de_dias == 30
    assert e.equipe == 'televendas'
    assert any('10' in av for av in e.avisos) and any('invertida' in av for av in e.avisos)
    assert any('ramo 3' in av for av in e.avisos)


@pytest.mark.parametrize('texto, esperado', [
    ('Ativos → compra nos últimos 60 dias → 14 dias → Somente clientes que não estão na rota da semana',
     {'rota_semana': 'exclui'}),
    ('Não agendar inadimplentes', {'inadimplente': 'inclui'}),
    ('Não agendar clientes em rota. Não conflitar com a regra do externo → Todos os clientes que esta na rota',
     {'rota_semana': 'inclui'}),
    ('Prospects → Clientes com ciclo de vida em prospects na empresa → 14 dias → Exceto inadimplentes',
     {'prospect': 'inclui', 'inadimplente': 'exclui'}),
    ('Não agendar → Clientes baixados na receita', {'baixado_receita': 'inclui'}),
    ('Inativo → Clientes sem pedidos a mais 90 dias → 28 dias', {}),
])
def test_classificar_filtros(texto, esperado):
    assert classificar_filtros(texto) == esperado


def test_conferencia_corrige_filtro_negado_que_o_modelo_tornou_positivo():
    it = Item('Prospects', 'frequencia', 6, 14, None, None, ['rota_semana'], [], ['clientes na rota da semana'])
    avisos = []
    conferir_filtros(it, 'Prospects → Clientes com ciclo de vida em prospects na empresa → 14 dias → Somente '
                         'clientes que não estão na rota da semana', avisos)
    assert it.filtros == ['prospect'] and it.exceto == ['rota_semana'] and it.outras_condicoes == []
    assert len(avisos) == 3


def test_interpretar_com_backend_dublê():
    resposta = ('{"titulo": "Regra Teste", "equipe": "televendas", "itens": [{"ramo": 1, "nome": "Ativos", '
                '"acao": "frequencia", "frequencia_dias": 14, "comprou_nos_ultimos_dias": 30, '
                '"sem_comprar_ha_mais_de_dias": null, "filtros": [], "exceto": ["rota_semana"], '
                '"outras_condicoes": []}]}')
    backend = SimpleNamespace(completar=lambda system, msgs: SimpleNamespace(texto=resposta))
    e = interpretar(backend, '1. Ativos → Clientes com compra nos últimos 30 dias → 14 dias → Somente clientes '
                             'que não estão na rota da semana')
    assert e.itens[0].frequencia_dias == 14 and e.itens[0].exceto == ['rota_semana']
    assert e.itens[0].texto_original.startswith('Ativos')


def test_revisao_aponta_os_pontos_falhos():
    rev = revisar(espec(), {})
    ids = [p.id for p in rev.perguntas]
    assert 'excecao:rota_semana' in ids  # exceção repetida em todas as regras
    assert 'baixados' in ids  # bloqueio comum ausente
    assert 'acima:120' in ids  # clientes com mais de 120 dias ficam sem regra
    assert 'inadimplentes' not in ids  # a descrição já trata
    assert 'equipe' not in ids
    assert any('Capacidade' in a for a in rev.avisos)  # fora do escopo


def test_revisao_acusa_buraco_e_sobreposicao_e_frequencia_ausente():
    e = Especificacao('t', 'televendas', '', [
        Item('A', 'frequencia', 1, 14, 30, None), Item('B', 'frequencia', 2, 7, None, 45),
        Item('C', 'frequencia', 3, None, 20, None, ['prospect'])])
    ids = [p.id for p in revisar(e, {}).perguntas]
    assert 'buraco:30:45' in ids and 'frequencia:2' in ids
    e2 = Especificacao('t', 'televendas', '', [Item('A', 'frequencia', 1, 14, 60, None),
                                              Item('B', 'frequencia', 2, 7, 90, 30)])
    assert any(i.startswith('sobreposicao:') for i in [p.id for p in revisar(e2, {}).perguntas])


def test_pergunta_respondida_nao_volta():
    assert 'baixados' not in [p.id for p in revisar(espec(), {'baixados': Decisao(opcao=1)}).perguntas]


def test_interpretar_respostas():
    perguntas = revisar(espec(), {}).perguntas
    dec, aceite = interpretar_respostas('1a, 2b', perguntas)
    assert dec[perguntas[0].id].opcao == 0 and dec[perguntas[1].id].opcao == 1 and not aceite
    _, aceite = interpretar_respostas('ok, pode seguir', perguntas)
    assert aceite
    acima = next(n for n, p in enumerate(perguntas, 1) if p.id.startswith('acima:'))
    dec, _ = interpretar_respostas(f'{acima}: 35 dias', perguntas)
    assert dec[perguntas[acima - 1].id].numero == 35


def plano_com_sugestoes():
    e = espec()
    decisoes = {}
    aplicar_sugestoes(revisar(e, decisoes).perguntas, decisoes)
    return planejar(e, decisoes)


def test_plano_ordena_bloqueios_faixas_e_regra_final():
    blocos, nome_time, vendedores, _ = plano_com_sugestoes()
    assert (nome_time, vendedores) == ('televendas', 'todostelevendas')
    secoes = [b.secao for b in blocos]
    assert secoes == sorted(secoes, key=['bloqueio', 'agendamento', 'fallback'].index)
    assert [b.filtros for b in blocos if b.secao == 'bloqueio'] == [['baixado_receita'], ['inadimplente'],
                                                                     ['rota_semana']]
    faixas = [b.comprou_nos_ultimos_dias for b in blocos if b.comprou_nos_ultimos_dias]
    assert faixas == sorted(faixas)
    assert blocos[-1].secao == 'fallback' and blocos[-1].acao == 'nao_agendar'
    assert not any(b.nao_filtros for b in blocos)  # a exceção virou bloqueio


def test_arquivo_montado_e_valido_e_decide_como_a_descricao():
    blocos, nome_time, vendedores, _ = plano_com_sugestoes()
    arquivo = montar_arquivo('Regra Teste', nome_time, vendedores, [molde(b, nome_time) for b in blocos],
                             [b.secao for b in blocos])
    assert arquivo.startswith('version 1.0')
    assert all(v['status'] == 'ok' for v in validar_dsl(arquivo))
    regras = regras_do_texto(arquivo)
    casos = {Cliente(10): 'frequencia 14', Cliente(45): 'frequencia 7', Cliente(100): 'frequencia 21',
             Cliente(121): 'nao agendar', Cliente(None): 'frequencia 14', Cliente(10, rota_semana=True): 'nao agendar',
             Cliente(10, inadimplente=True): 'nao agendar', Cliente(10, baixado=True): 'nao agendar'}
    for cliente, esperado in casos.items():
        assert decidir(regras, cliente)[0] == esperado, cliente


def test_molde_sem_forma_conhecida_fica_para_o_modelo():
    assert molde(BlocoPlano('X', 'agendamento', 'frequencia', 7, outras_condicoes=['curva A']), 't') is None
    assert molde(BlocoPlano('X', 'agendamento', 'frequencia', 7, nao_filtros=['rota_semana']), 't') is None
    assert 'adimplentes' in molde(BlocoPlano('X', 'agendamento', 'frequencia', 7, nao_filtros=['inadimplente']), 't')


def test_exclusao_mantida_como_excecao_de_cada_regra():
    e = espec()
    decisoes = {'excecao:rota_semana': Decisao(opcao=1)}
    aplicar_sugestoes(revisar(e, decisoes).perguntas, decisoes)
    blocos, *_ = planejar(e, decisoes)
    assert not any('rota_semana' in b.filtros for b in blocos)
    assert all(b.nao_filtros == ['rota_semana'] for b in blocos if b.acao == 'frequencia' and b.secao != 'fallback')


def test_frequencia_respondida_entra_no_plano():
    e = Especificacao('t', 'televendas', '', [Item('A', 'frequencia', 1, None, 30, None),
                                             Item('B', 'frequencia', 2, 7, None, 30)])
    blocos, *_ = planejar(e, {'frequencia:0': Decisao(numero=10), 'baixados': Decisao(opcao=1),
                              'inadimplentes': Decisao(opcao=0), 'prospects': Decisao(opcao=0)})
    assert [(b.nome, b.frequencia_dias) for b in blocos] == [('A', 10), ('B', 7)]


def test_nomes_repetidos_ficam_unicos():
    e = Especificacao('t', 'televendas', '', [Item('Ativos', 'frequencia', 1, 14, 30, None),
                                             Item('Ativos', 'frequencia', 2, 7, None, 30)])
    blocos, *_ = planejar(e, {'baixados': Decisao(opcao=1), 'inadimplentes': Decisao(opcao=0),
                              'prospects': Decisao(opcao=0)})
    assert [b.nome for b in blocos] == ['Ativos', 'Ativos (2)']
