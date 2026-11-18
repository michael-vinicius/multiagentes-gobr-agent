from __future__ import annotations

import json
from types import SimpleNamespace
from typing import List


from agente import Servicos, conversar, criar_grafo, normalizar_bloco, verificar_semantica
from especificacao import BlocoPlano
from rag import Contexto

ESPEC = {"titulo": "Regra Teste", "equipe": "televendas", "itens": [
    {"ramo": 1, "nome": "Ativos", "acao": "frequencia", "frequencia_dias": 14, "comprou_nos_ultimos_dias": 30,
     "sem_comprar_ha_mais_de_dias": None, "filtros": [], "exceto": [], "outras_condicoes": []},
    {"ramo": 2, "nome": "Inativos", "acao": "frequencia", "frequencia_dias": 28, "comprou_nos_ultimos_dias": None,
     "sem_comprar_ha_mais_de_dias": 30, "filtros": [], "exceto": [], "outras_condicoes": []},
    {"ramo": 3, "nome": "Prospects", "acao": "frequencia", "frequencia_dias": 7, "comprou_nos_ultimos_dias": None,
     "sem_comprar_ha_mais_de_dias": None, "filtros": ["prospect"], "exceto": [], "outras_condicoes": []}]}
DESCRICAO = ('Título: Regra Teste\n1. Ativos → compraram nos últimos 30 dias → 14 dias\n'
             '2. Inativos → sem comprar há mais de 30 dias → 28 dias\n3. Prospects → nunca compraram → 7 dias')


class BackendFake:
    def __init__(self, respostas: List[str]):
        self.respostas = list(respostas)

    def completar(self, system, mensagens):
        return SimpleNamespace(texto=self.respostas.pop(0))


class RecuperadorFake:
    def recuperar(self, pergunta, k_exemplos, k_manual):
        return Contexto(pergunta, [], [])


class GeradorFake:
    """Escreve o bloco a partir do pedido; com `erros`, as primeiras respostas vêm erradas de propósito."""

    def __init__(self, erros: int = 0):
        self.erros = erros
        self.pedidos: List[str] = []

    def gerar(self, ctx):
        self.pedidos.append(ctx.pergunta)
        p = ctx.pergunta
        if 'não devem ser agendados' in p and 'Receita' in p:
            cond, acao = 'quando status na receita federal definido como baixada', 'nao agendar'
        elif 'prospects' in p:
            cond, acao = 'quando no ciclo de vida prospect com a empresa', 'frequencia de 7 dias'
        elif 'últimos 30 dias' in p:
            cond, acao = 'quando recencia de positivacao em 30 dias', 'frequencia de 14 dias'
        else:
            cond, acao = 'quando fora da recencia de positivacao em 30 dias', 'frequencia de 28 dias'
        if self.erros > 0:
            self.erros -= 1
            cond = 'quando recencia de positivacao em 10 dias'  # faixa errada
        bloco = f'parametros "x":\n    da carteira("<nome da carteira>")\n    {cond}\n    {acao}'
        return SimpleNamespace(blocos_gobr=[bloco], citacoes=['E1'], validacao=[{'problemas': []}])


def grafo(gerador=None):
    servicos = Servicos(BackendFake([json.dumps(ESPEC)]), RecuperadorFake(), gerador or GeradorFake())
    return criar_grafo(servicos), servicos


def test_conversa_completa_com_sugestoes():
    g, servicos = grafo()
    saida: List[str] = []
    r = conversar(g, DESCRICAO, ['ok', 'fim'], saida=saida.append)
    texto = '\n'.join(saida)
    assert 'Antes de escrever as regras, preciso decidir' in texto
    assert 'baixados na Receita' in texto
    arquivo = r['arquivo_gobr']
    assert arquivo.startswith('version 1.0') and 'time "televendas"' in arquivo
    assert arquivo.index('Receita Federal') < arquivo.index('Prospects') < arquivo.index('Ativos') < arquivo.index('Inativos')
    assert 'da carteira' not in arquivo  # fonte normalizada para o time
    assert r['relatorio']['semantica']['concordancia'] == 1.0
    assert r['relatorio']['fontes'] == {'modelo': 4, 'molde': 0}


def test_bloco_errado_recebe_as_divergencias_e_e_corrigido():
    gerador = GeradorFake(erros=1)
    g, _ = grafo(gerador)
    r = conversar(g, DESCRICAO, ['ok', 'fim'], saida=lambda *_: None)
    assert any('pegava os clientes errados' in p for p in gerador.pedidos)
    assert r['relatorio']['semantica']['concordancia'] == 1.0
    assert r['relatorio']['corrigidos'] == 1 and r['relatorio']['fontes']['molde'] == 0


def test_bloco_que_continua_errado_usa_o_molde():
    g, _ = grafo(GeradorFake(erros=2))
    r = conversar(g, DESCRICAO, ['ok', 'fim'], saida=lambda *_: None)
    assert r['relatorio']['fontes']['molde'] == 1
    assert r['relatorio']['semantica']['concordancia'] == 1.0


def test_respostas_por_numero_mudam_o_plano():
    g, _ = grafo()
    # 1ª pergunta: baixados (b = não); 2ª: inadimplentes (b = não agendar)
    r = conversar(g, DESCRICAO, ['1b, 2b', 'fim'], saida=lambda *_: None)
    assert 'Receita Federal' not in r['arquivo_gobr'] and 'inadimplentes' in r['arquivo_gobr']


def test_ajuste_depois_da_resposta():
    espec2 = json.loads(json.dumps(ESPEC))
    espec2['itens'][2]['frequencia_dias'] = 14
    servicos = Servicos(BackendFake([json.dumps(ESPEC), json.dumps(espec2)]), RecuperadorFake(), GeradorFake())
    g = criar_grafo(servicos)

    class Gerador14(GeradorFake):
        def gerar(self, ctx):
            r = super().gerar(ctx)
            if 'prospects' in ctx.pergunta and '14 dias' in ctx.pergunta:
                r.blocos_gobr = [r.blocos_gobr[0].replace('7 dias', '14 dias')]
            return r
    servicos.gerador = Gerador14()
    r = conversar(g, DESCRICAO, ['ok', 'prospects a cada 14 dias', 'ok', 'fim'], saida=lambda *_: None)
    assert 'quando no ciclo de vida prospect com a empresa\n    frequencia de 14 dias' in r['arquivo_gobr']


def test_normalizar_bloco():
    gobr = ('parametros "outro nome":\n    da carteira("<nome>")\n    quando inadimplentes\n    nao agendar\n\n'
            'parametros "segundo":\n    do time("t")\n    quando prospects\n    nao agendar')
    assert normalizar_bloco(gobr, 'Bloqueio', 'televendas') == \
        'parametros "Bloqueio":\n    do time("televendas")\n    quando inadimplentes\n    nao agendar'
    assert normalizar_bloco('', 'x', 't') == ''


def test_clausula_desconhecida_em_bloco_com_molde_e_divergencia():
    # regressão: o modelo escreveu "unica compra com o vendedor" para prospects e o bloco foi aceito sem verificação
    plano = [BlocoPlano('Prospect', 'agendamento', 'frequencia', 7, filtros=['prospect'])]
    cand = 'parametros "Prospect":\n    do time("t")\n    quando unica compra com o vendedor\n    frequencia de 7 dias'
    status, detalhe = verificar_semantica([], cand, plano, 't')
    assert status == 'divergente' and 'unica compra com o vendedor' in detalhe


def test_bloco_sem_molde_nao_contamina_os_seguintes():
    plano = [BlocoPlano('Curva A', 'agendamento', 'frequencia', 7, outras_condicoes=['curva A com a empresa']),
             BlocoPlano('Ativos', 'agendamento', 'frequencia', 14, comprou_nos_ultimos_dias=60)]
    curva = 'parametros "Curva A":\n    do time("t")\n    quando curva A com a empresa\n    frequencia de 7 dias'
    assert verificar_semantica([], curva, plano[:1], 't')[0] == 'nao_verificavel'  # sem molde
    ativos = 'parametros "Ativos":\n    do time("t")\n    quando recencia de positivacao em 60 dias\n    frequencia de 14 dias'
    # o bloco aceito da curva A entra na referência: o 2º bloco é julgado só pelo que ele muda
    assert verificar_semantica([curva], ativos, plano, 't')[0] == 'ok'
    assert verificar_semantica([curva], ativos.replace('60 dias', '50 dias'), plano, 't')[0] == 'divergente'
    # bloco anterior que o simulador não interpreta: não dá para saber quem chega até aqui
    ramo = curva.replace('curva A com a empresa', 'ramo de atividade igual("X")')
    assert verificar_semantica([ramo], ativos, plano, 't')[0] == 'nao_verificavel'


def test_verificacao_considera_a_ordem():
    plano = [BlocoPlano('A', 'agendamento', 'frequencia', 14, comprou_nos_ultimos_dias=60),
             BlocoPlano('B', 'agendamento', 'frequencia', 7, comprou_nos_ultimos_dias=90, sem_comprar_ha_mais_de_dias=60)]
    aceitos = 'parametros "A":\n    do time("t")\n    quando recencia de positivacao em 60 dias\n    frequencia de 14 dias'
    # sem o "fora da recência em 60", o bloco B é equivalente porque vem depois do A
    cand = 'parametros "B":\n    do time("t")\n    quando recencia de positivacao em 90 dias\n    frequencia de 7 dias'
    assert verificar_semantica(aceitos, cand, plano, 't')[0] == 'ok'
    errado = cand.replace('90 dias', '80 dias')
    status, detalhe = verificar_semantica(aceitos, errado, plano, 't')
    assert status == 'divergente' and '81–90' in detalhe
