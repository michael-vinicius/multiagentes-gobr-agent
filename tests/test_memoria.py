"""Etapa 6: memória de curto prazo (sessão), de longo prazo (entre sessões) e gestão do contexto."""
from __future__ import annotations

import json
import sqlite3
from typing import List

import pytest
from langgraph.store.memory import InMemoryStore

from agente import Servicos, conversar, criar_grafo, intencao_direta, pendencias
from especificacao import Especificacao, Item
from lacunas import revisar
from memoria import (OPCOES_PREFERENCIA, MemoriaLonga, aplicar_lembradas, chave_empresa, estimar_tokens,
                     filtrar_turno, montar_historico, preferencia_do_texto)
from test_agente import DESCRICAO, ESPEC, BackendFake, GeradorFake, RecuperadorFake

ESPEC_14 = json.loads(json.dumps(ESPEC))
ESPEC_14['itens'][2]['frequencia_dias'] = 14  # prospects a cada 14 dias


class Gerador14(GeradorFake):
    """Escreve 14 dias para prospects quando o pedido diz 14 dias."""

    def gerar(self, ctx):
        r = super().gerar(ctx)
        if 'prospects' in ctx.pergunta and '14 dias' in ctx.pergunta:
            r.blocos_gobr = [r.blocos_gobr[0].replace('7 dias', '14 dias')]
        return r


def servicos(respostas_modelo: List[str], memoria=None, gerador=None, **kw) -> Servicos:
    return Servicos(BackendFake(respostas_modelo), RecuperadorFake(), gerador or Gerador14(), memoria=memoria, **kw)


def calado(*_):
    return None


# ---------------------------------------------------------------- memória de longo prazo (unidade)

def test_chave_empresa():
    assert chave_empresa('Regra Maxlub') == 'maxlub'
    assert chave_empresa('V1 Vidros - Regra Comercial') == 'v1-vidros'
    assert chave_empresa('Regra Infinitto Design') == 'infinitto-design'


def test_memoria_longa_lembra_acha_descreve_e_esquece():
    mem = MemoriaLonga(InMemoryStore(), 'Ana')
    mem.lembrar_empresa('infinitto-design', {'titulo': 'Regra Infinitto Design', 'data': '01/01/2026 10:00',
                                             'versao': {'blocos': [{}, {}], 'decisoes': {'equipe': {'opcao': 0}}}})
    assert mem.achar_empresa('Infinitto Design: prospects a cada 7 dias')[0] == 'infinitto-design'
    assert mem.achar_empresa('Regra Maxlub') is None
    assert mem.lembrar_preferencia('inadimplentes', 1, 'teste') == 'não agendar inadimplentes'
    mem.lembrar_nota('o cliente prefere nomes curtos nas regras')
    texto = mem.descrever()
    assert 'Infinitto' in texto and 'não agendar inadimplentes' in texto and 'nomes curtos' in texto
    assert mem.esquecer('inadimplentes') == ['a preferência "não agendar inadimplentes"']
    assert mem.preferencias() == {}
    assert len(mem.esquecer('tudo')) == 2 and 'Ainda não guardei' in mem.descrever()


def test_preferencias_sao_por_analista():
    store = InMemoryStore()
    MemoriaLonga(store, 'Ana').lembrar_preferencia('baixados', 0)
    assert MemoriaLonga(store, 'Bruno').preferencias() == {}
    assert 'baixados' in MemoriaLonga(store, 'ana').preferencias()


@pytest.mark.parametrize('texto, esperado', [
    ('lembre que inadimplentes devem sempre ser bloqueados', ('inadimplentes', 1)),
    ('pode agendar inadimplentes normalmente', ('inadimplentes', 0)),
    ('não agendar baixados na Receita', ('baixados', 0)),
    ('nossas regras são sempre da equipe de campo', ('equipe', 1)),
    ('o cliente gosta de nomes curtos', None),
])
def test_preferencia_do_texto(texto, esperado):
    assert preferencia_do_texto(texto) == esperado


def test_opcoes_de_preferencia_alinhadas_com_a_revisao():
    # as opções lembradas são índices: precisam estar na mesma ordem das opções das perguntas da revisão
    esp = Especificacao('t', 'nao_informado', '', [
        Item('Ativos', 'frequencia', 1, 14, 30, None), Item('Inativos', 'frequencia', 2, 28, None, 30)])
    perguntas = {p.id: p for p in revisar(esp, {}).perguntas}
    chaves = {'equipe': ['televendas', 'campo', 'todos'], 'baixados': ['não agendar', 'não'],
              'inadimplentes': ['agendar normalmente', 'não agendar'], 'prospects': ['sem regra', 'não agendar',
                                                                                     'frequência']}
    for pid, opcoes in OPCOES_PREFERENCIA.items():
        p = perguntas[pid] if pid != 'prospects' else None
        if p is None:
            continue
        assert len(p.opcoes) == len(opcoes)
        for opcao, chave in zip(p.opcoes, chaves[pid]):
            assert chave in opcao


def test_lembradas_viram_sugestao_com_motivo_e_a_pergunta_continua():
    esp = Especificacao('t', 'televendas', '', [Item('Ativos', 'frequencia', 1, 14, 30, None)])
    perguntas = revisar(esp, {}).perguntas
    alterados = aplicar_lembradas(perguntas, {'inadimplentes': {'opcao': 1, 'data': '02/02/2026 09:00',
                                                                'origem': 'escolhida em "Regra X"'}})
    p = next(p for p in perguntas if p.id == 'inadimplentes')
    assert alterados == ['inadimplentes'] and p.sugestao == 1
    assert 'lembrado' in p.motivo and '02/02/2026' in p.motivo and 'Regra X' in p.motivo


# ---------------------------------------------------------------- contexto (unidade)

def _historico(n: int) -> List[dict]:
    h = [{'papel': 'analista', 'texto': 'Título: Regra Teste\n1. Ativos → 30 dias → 14 dias'}]
    for i in range(n):
        h.append({'papel': 'agente', 'texto': f'Resposta {i}. ' + 'explicação longa ' * 40 +
                  '\n```gobr\nparametros "x":\n    do time("t")\n    nao agendar\n```'})
        h.append({'papel': 'analista', 'texto': f'pedido número {i}: mude a regra {i}'})
    return h


def test_compactacao_respeita_o_orcamento_e_guarda_cabeca_cauda_e_pedidos():
    h = _historico(30)
    sem = montar_historico(h, 1500, compactar=False)
    com = montar_historico(h, 1500, compactar=True)
    assert sem.tokens > 5000 and com.tokens <= 1500
    assert com.mensagens[0]['role'] == 'user' and 'Regra Teste' in com.mensagens[0]['content']  # cabeça
    assert 'pedido número 29' in com.mensagens[-1]['content']  # cauda
    assert com.compactados > 0 and 'pedido número' in com.resumo  # o meio vira um resumo dos pedidos
    assert all(a['role'] != b['role'] for a, b in zip(com.mensagens, com.mensagens[1:]))  # alterna user/assistant


def test_filtragem_tira_o_arquivo_das_versoes_antigas():
    t = filtrar_turno('Regras:\n```gobr\nparametros "a":\n    nao agendar\n```\nfim')
    assert 'parametros' not in t and 'arquivo GoBR' in t
    assert estimar_tokens('a' * 300) == 100


# ---------------------------------------------------------------- intenção

@pytest.mark.parametrize('texto, intencao', [
    ('fim', 'fim'), ('obrigado!', 'fim'), ('volta como estava', 'desfazer'), ('desfaz isso', 'desfazer'),
    ('compara as versões', 'comparar'), ('o que mudou?', 'comparar'),
    ('o que muda se os inativos forem atendidos a cada 21 dias?', 'simulacao'),
    ('por que o bloqueio de rota vem antes das regras de frequência?', 'pergunta'),
    ('muda a de risco para 10 dias', 'ajuste'), ('prospects a cada 14 dias', 'ajuste'),
    ('lembre que inadimplentes devem ser bloqueados', 'lembrar'), ('o que você lembra?', 'memoria'),
    ('esqueça a Maxlub', 'esquecer'), ('aplica', 'aplicar'),
    ('faz a mesma coisa para os inativos', None),  # depende da conversa: vai para o modelo
])
def test_intencao_direta(texto, intencao):
    r = intencao_direta(texto)
    assert (r[0] if r else None) == intencao
    if intencao == 'simulacao':
        assert r[1] == 'os inativos forem atendidos a cada 21 dias'


# ---------------------------------------------------------------- curto prazo no grafo

def test_desfazer_comparar_e_reaproveitar_blocos():
    s = servicos([json.dumps(ESPEC), json.dumps(ESPEC_14)])
    g = criar_grafo(s)
    r = conversar(g, DESCRICAO, ['ok', 'prospects a cada 14 dias', 'compara', 'volta como estava', 'fim'],
                  saida=calado)
    assert [v['pedido'] for v in r['versoes']] == ['versão inicial', 'prospects a cada 14 dias',
                                                    'desfazer (volta à versão 0)']
    assert 'prospect com a empresa\n    frequencia de 7 dias' in r['arquivo_gobr']  # voltou aos 7 dias
    comparacao = next(m for m in r['mensagens'] if m.startswith('Versão 0'))
    assert 'regra alterada: "Prospects"' in comparacao and 'mudam de decisão' in comparacao
    # o ajuste só redigiu o bloco que mudou; os outros 3 vieram da versão anterior (e foram verificados de novo)
    assert len(s.gerador.pedidos) == 5 and r['versoes'][1]['relatorio']['reaproveitados'] == 3


def test_pergunta_usa_o_historico_compactado_e_o_arquivo():
    class BackendGravador(BackendFake):
        def completar(self, system, mensagens):
            self.visto = (system, mensagens)
            return super().completar(system, mensagens)

    s = Servicos(BackendGravador([json.dumps(ESPEC), 'Porque a 1ª regra que pega o cliente vale (manual 7.6).']),
                 RecuperadorFake(), Gerador14())
    r = conversar(criar_grafo(s), DESCRICAO, ['ok', 'por que o bloqueio vem primeiro?', 'fim'], saida=calado)
    assert any('manual 7.6' in m for m in r['mensagens'])
    system, mensagens = s.backend.visto
    assert 'parametros "Ativos"' in system  # o arquivo atual entra uma vez, nas instruções
    assert mensagens[-1]['content'].endswith('por que o bloqueio vem primeiro?')
    assert not any('```gobr' in m['content'] for m in mensagens)  # o arquivo das versões antigas sai do histórico


def test_simulacao_nao_aplica_e_aplica_depois():
    s = servicos([json.dumps(ESPEC), json.dumps(ESPEC_14)])
    r = conversar(criar_grafo(s), DESCRICAO,
                  ['ok', 'o que muda se os prospects forem atendidos a cada 14 dias?', 'aplica', 'fim'], saida=calado)
    sim = next(m for m in r['mensagens'] if m.startswith('Simulei'))
    assert 'mudariam de decisão' in sim and 'hoje "frequencia 7", com a mudança "frequencia 14"' in sim
    assert len(r['versoes']) == 2 and 'frequencia de 14 dias' in r['arquivo_gobr']


def test_referencia_vai_ao_modelo_com_o_historico():
    reescrito = json.dumps({'intencao': 'ajuste', 'pedido': 'Prospects a cada 14 dias'})
    s = servicos([json.dumps(ESPEC), reescrito, json.dumps(ESPEC_14)])
    r = conversar(criar_grafo(s), DESCRICAO, ['ok', 'faz a mesma coisa que os ativos para os prospects', 'fim'],
                  saida=calado)
    assert r['versoes'][-1]['pedido'] == 'Prospects a cada 14 dias' and 'frequencia de 14 dias' in r['arquivo_gobr']


def test_sessao_retomada_de_um_sqlite_sem_refazer_a_interpretacao(tmp_path):
    from langgraph.checkpoint.sqlite import SqliteSaver
    banco = tmp_path / 'sessoes.sqlite'
    g1 = criar_grafo(servicos([json.dumps(ESPEC)]), SqliteSaver(sqlite3.connect(str(banco), check_same_thread=False)))
    g1.invoke({'entrada': DESCRICAO}, {'configurable': {'thread_id': 's1'}})  # para na 1ª pergunta
    del g1  # "fecha o programa"
    # novo processo: o modelo dublê não tem mais respostas; se a interpretação rodasse de novo, quebraria
    g2 = criar_grafo(servicos([]), SqliteSaver(sqlite3.connect(str(banco), check_same_thread=False)))
    assert pendencias(g2, 's1')[0].value['tipo'] == 'perguntas'
    saida: List[str] = []
    r = conversar(g2, None, ['ok', 'fim'], thread='s1', saida=saida.append)
    assert 'retomando a sessão' in saida[0] and r['arquivo_gobr'].startswith('version 1.0')


# ---------------------------------------------------------------- longo prazo no grafo

def test_empresa_lembrada_parte_do_arquivo_anterior_sem_refazer_perguntas():
    mem = MemoriaLonga(InMemoryStore(), 'ana')
    s1 = servicos([json.dumps(ESPEC)], memoria=mem)
    conversar(criar_grafo(s1), DESCRICAO, ['1b, 2b', 'fim', 'sim'], thread='a', saida=calado)
    assert mem.empresa('teste') is not None
    s2 = servicos([json.dumps(ESPEC_14)], memoria=mem)
    saida: List[str] = []
    r = conversar(criar_grafo(s2), 'Teste: prospects a cada 14 dias', ['a', 'fim', 'não'], thread='b',
                  saida=saida.append)
    texto = '\n'.join(saida)
    assert 'Já parametrizei "Regra Teste"' in texto and 'preciso decidir' not in texto  # nada perguntado de novo
    assert 'frequencia de 14 dias' in r['arquivo_gobr'] and 'inadimplentes' in r['arquivo_gobr']  # decisão lembrada
    assert len(s2.gerador.pedidos) == 1  # só o bloco de prospects foi redigido


def test_preferencia_passa_para_outra_empresa_como_sugestao():
    mem = MemoriaLonga(InMemoryStore(), 'ana')
    # sessão 1: o analista escolhe bloquear inadimplentes (2b) e confirma guardar tudo
    conversar(criar_grafo(servicos([json.dumps(ESPEC)], memoria=mem)), DESCRICAO, ['2b', 'fim', 'sim'],
              thread='a', saida=calado)
    assert mem.preferencias()['inadimplentes']['opcao'] == 1
    # sessão 2: outra empresa; "ok" aceita a sugestão, que agora vem da memória
    outra = json.loads(json.dumps(ESPEC))
    outra['titulo'] = 'Regra Outra Distribuidora'
    saida: List[str] = []
    r = conversar(criar_grafo(servicos([json.dumps(outra)], memoria=mem)),
                  DESCRICAO.replace('Regra Teste', 'Regra Outra Distribuidora'), ['ok', 'fim', 'não'], thread='b',
                  saida=saida.append)
    texto = '\n'.join(saida)
    assert 'não agendar inadimplentes  ← sugestão' in texto and 'lembrado: você escolheu' in texto
    assert 'quando inadimplentes' in r['arquivo_gobr']


def test_lembrar_o_que_lembra_e_esquecer_na_conversa():
    mem = MemoriaLonga(InMemoryStore(), 'ana')
    r = conversar(criar_grafo(servicos([json.dumps(ESPEC)], memoria=mem)), DESCRICAO,
                  ['ok', 'lembre que inadimplentes devem sempre ser bloqueados', 'o que você lembra?',
                   'esqueça inadimplentes', 'fim', 'não'], saida=calado)
    msgs = '\n'.join(r['mensagens'])
    assert 'Guardei a preferência: não agendar inadimplentes' in msgs
    assert 'preferência: não agendar inadimplentes' in msgs and 'Esqueci a preferência' in msgs
    assert mem.preferencias() == {} and mem.empresa('teste') is None  # "não" no fim: nada guardado


def test_sem_memoria_mantem_o_comportamento_da_etapa_5():
    s = servicos([json.dumps(ESPEC), json.dumps(ESPEC_14)], conversa=False)
    r = conversar(criar_grafo(s), DESCRICAO, ['ok', 'prospects a cada 14 dias', 'ok', 'fim'], saida=calado)
    assert 'frequencia de 14 dias' in r['arquivo_gobr']


# ---------------------------------------------------------------- avaliador

def test_auxiliares_do_avaliador():
    from avaliar_memoria import aplicar_trocas, responder_perguntas, resposta_ao_turno
    gobr = 'parametros "A":\n    frequencia de 7 dias\n\nparametros "B":\n    frequencia de 7 dias\n'
    assert aplicar_trocas(gobr, [['B', '7 dias', '10 dias']]) == gobr.replace('B":\n    frequencia de 7', 'B":\n    frequencia de 10')
    with pytest.raises(ValueError):
        aplicar_trocas(gobr, [['C', '7 dias', '10 dias']])
    pedido = {'perguntas': [{'id': 'equipe'}, {'id': 'inadimplentes'}]}
    assert responder_perguntas(pedido, {'inadimplentes': 'b'}) == '2b; o resto com as sugestões'
    assert responder_perguntas(pedido, {}) == 'ok'
    dialogo = [{'agente': 'arquivo', 'analista': 'por que X?'}, {'agente': 'porque Y', 'analista': 'fim'}]
    assert resposta_ao_turno(dialogo, 'por que') == 'porque Y'


def test_pergunta_sobre_ordem_e_verificada_no_simulador():
    from agente import fato_de_ordem
    arquivo = ('parametros "Bloqueio de rota":\n    do time("t")\n    quando data da rota na semana\n    nao agendar\n\n'
               'parametros "Prospects":\n    do time("t")\n    quando no ciclo de vida prospect com a empresa\n'
               '    frequencia de 7 dias\n\n'
               'parametros "Ativos":\n    do time("t")\n    quando recencia de positivacao em 60 dias\n'
               '    frequencia de 14 dias\n')
    sem_efeito = fato_de_ordem(arquivo, 'por que os prospects vêm antes dos ativos?')
    assert 'nenhum dos' in sem_efeito and 'não se sobrepõem' in sem_efeito
    com_efeito = fato_de_ordem(arquivo, 'por que o bloqueio de rota vem antes das regras de frequência?')
    assert 'mudariam de decisão' in com_efeito and 'com a ordem atual "nao agendar"' in com_efeito
    assert fato_de_ordem(arquivo, 'como o GoBR decide qual regra vale?') is None


def test_resumo_do_trecho_compactado_guarda_o_comeco_e_marca_o_arquivo():
    from memoria import resumir_trecho
    trecho = [{'role': 'user', 'content': 'ok'},
              {'role': 'assistant', 'content': 'Regras em GoBR:\n[arquivo]'}]
    for i in range(40):
        trecho += [{'role': 'user', 'content': f'pergunta {i}: por que a regra {i} vem antes da regra {i + 1}?'},
                   {'role': 'assistant', 'content': 'resposta'}]
    r = resumir_trecho(trecho, 300)
    assert estimar_tokens(r) <= 300
    assert r.index('[arquivo gerado ou alterado]') < r.index('pergunta 0:')  # a ordem dos eventos fica
    assert 'pergunta 0:' in r and 'pergunta 39:' in r and 'itens omitidos' in r  # começo e fim ficam, o meio sai
    assert '"ok"' not in r  # resposta trivial às perguntas da revisão não é pedido


def test_teto_do_historico_so_vale_com_compactacao():
    from agente import _orcamento_historico
    from memoria import ORCAMENTO_HISTORICO
    s = servicos([])
    s.backend.num_ctx = 8192
    assert _orcamento_historico(s, 'x' * 300, 900) == ORCAMENTO_HISTORICO
    s.compactar = False
    assert _orcamento_historico(s, 'x' * 300, 900) == 8192 - 100 - 900 - 200
