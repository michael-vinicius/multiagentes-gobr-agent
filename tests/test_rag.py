from __future__ import annotations

import io
import urllib.error
from types import SimpleNamespace
from typing import Dict, List

import pytest

import rag
from rag import (BETA_FALLBACK, BackendAnthropic, BackendOllama, Contexto, ErroGeracao, Exemplo, Gerador,
                 Recuperador, SaidaModelo, Trecho, criar_backend, extrair_blocos_gobr, extrair_citacoes,
                 formatar_contexto, montar_mensagem, responder, validar_dsl)

DSL_FILIAL = 'parametros "Não agendar filiais":\n    do time("televendas")\n    quando cliente filial\n    nao agendar'
DSL_FILIAL_OUTRO_NOME = DSL_FILIAL.replace('Não agendar filiais', 'Filiais fora da agenda')
DSL_SEMANAL = ('parametros "semanal":\n    da carteira("carteira fixa")\n    quando inatividade de 90 dias\n'
               '    frequencia semanal()')


class BuscadorFake:
    def __init__(self, resultados: List[Dict]):
        self.resultados = resultados
        self.chamadas: List[tuple] = []

    def buscar(self, consulta: str, k: int) -> List[Dict]:
        self.chamadas.append((consulta, k))
        return self.resultados[:k]


def exemplo(id_: str, dsl: str, score: float = 0.9, status: str = 'ok') -> Dict:
    return {'id': id_, 'nome_regra': dsl.splitlines()[0], 'score': score, 'status_validacao': status,
            'explicacao_detalhada': f'explicação de {id_}', 'dsl_original': dsl}


def trecho(secao: str, score: float = 0.85) -> Dict:
    return {'id': f'manual_{secao}', 'secao': secao, 'titulo': f'{secao} Título', 'paginas': [26, 27],
            'score': score, 'texto': f'Manual GoBR > {secao} Título\n\nconteúdo {secao}'}


def contexto(**kw) -> Contexto:
    base = dict(pergunta='não agendar filiais',
                exemplos=[Exemplo('E1', 'r1', 'Não agendar filiais', 0.9, 'explicação', DSL_FILIAL)],
                trechos=[Trecho('M1', 'manual_6.5', '6.5', '6.5 Filtros de localização', (26, 27), 0.88, 'texto')])
    base.update(kw)
    return Contexto(**base)


# ---------------------------------------------------------------- recuperação

class TestRecuperador:
    def test_numera_exemplos_e_trechos_e_repassa_a_pergunta_sem_espacos(self):
        ex = BuscadorFake([exemplo('r1', DSL_FILIAL), exemplo('r2', DSL_SEMANAL)])
        man = BuscadorFake([trecho('6.5'), trecho('7.3.4')])
        ctx = Recuperador(ex, man).recuperar('  não agendar filiais \n', k_exemplos=2, k_manual=2)

        assert [e.ref for e in ctx.exemplos] == ['E1', 'E2']
        assert [t.ref for t in ctx.trechos] == ['M1', 'M2']
        assert ctx.pergunta == 'não agendar filiais'
        assert man.chamadas == [('não agendar filiais', 2)]
        assert ctx.trechos[0].paginas == (26, 27)
        assert ctx.refs() == ['E1', 'E2', 'M1', 'M2']

    def test_remove_exemplos_com_o_mesmo_corpo_mesmo_com_nome_diferente(self):
        ex = BuscadorFake([exemplo('r1', DSL_FILIAL), exemplo('r2', DSL_FILIAL_OUTRO_NOME),
                           exemplo('r3', DSL_SEMANAL)])
        ctx = Recuperador(ex, BuscadorFake([])).recuperar('x', k_exemplos=2, k_manual=0)
        assert [e.id for e in ctx.exemplos] == ['r1', 'r3']

    def test_busca_candidatos_extras_para_compensar_as_duplicatas(self):
        ex = BuscadorFake([exemplo('r1', DSL_FILIAL)])
        Recuperador(ex, BuscadorFake([]), fator_candidatos=4).recuperar('x', k_exemplos=3, k_manual=0)
        assert ex.chamadas == [('x', 12)]

    def test_ignora_exemplos_marcados_para_revisao_ou_sem_dsl(self):
        ex = BuscadorFake([exemplo('r1', DSL_FILIAL, status='revisao_necessaria'),
                           {**exemplo('r2', DSL_SEMANAL), 'dsl_original': None},
                           exemplo('r3', DSL_SEMANAL)])
        ctx = Recuperador(ex, BuscadorFake([])).recuperar('x', k_exemplos=5, k_manual=0)
        assert [e.id for e in ctx.exemplos] == ['r3']

    def test_k_zero_nao_consulta_o_indice(self):
        ex, man = BuscadorFake([exemplo('r1', DSL_FILIAL)]), BuscadorFake([trecho('6.5')])
        ctx = Recuperador(ex, man).recuperar('x', k_exemplos=0, k_manual=0)
        assert ctx.exemplos == [] and ctx.trechos == []
        assert ex.chamadas == [] and man.chamadas == []

    @pytest.mark.parametrize('pergunta, k_ex, k_man', [('   ', 5, 4), ('x', -1, 4), ('x', 5, -1)])
    def test_entradas_invalidas(self, pergunta, k_ex, k_man):
        with pytest.raises(ValueError):
            Recuperador(BuscadorFake([]), BuscadorFake([])).recuperar(pergunta, k_ex, k_man)

    def test_fator_de_candidatos_invalido(self):
        with pytest.raises(ValueError):
            Recuperador(BuscadorFake([]), BuscadorFake([]), fator_candidatos=0)


def test_carregar_recuperador_sem_indice_do_manual_explica_como_gerar(tmp_path):
    with pytest.raises(FileNotFoundError, match='indexar_manual.py'):
        rag.carregar_recuperador(dir_manual=tmp_path)


# ---------------------------------------------------------------- prompt

class TestPrompt:
    def test_contexto_traz_referencias_dsl_e_paginas(self):
        txt = formatar_contexto(contexto())
        assert '<exemplo ref="E1"' in txt and '<trecho ref="M1"' in txt
        assert DSL_FILIAL in txt
        assert 'paginas="26, 27"' in txt

    def test_aspas_em_atributos_sao_escapadas(self):
        ctx = contexto(exemplos=[Exemplo('E1', 'r1', 'regra "A" & B', 0.9, 'expl', DSL_FILIAL)])
        assert 'nome="regra &quot;A&quot; &amp; B"' in formatar_contexto(ctx)

    def test_contexto_vazio_e_explicito(self):
        txt = formatar_contexto(contexto(exemplos=[], trechos=[]))
        assert '(nenhum exemplo recuperado)' in txt and '(nenhum trecho recuperado)' in txt

    def test_pergunta_vem_depois_do_contexto(self):
        msg = montar_mensagem(contexto(pergunta='PERGUNTA-X'))
        assert msg.index('</contexto>') < msg.index('PERGUNTA-X')
        assert msg.rstrip().endswith('</pedido>')


# ---------------------------------------------------------------- pós-checagens

class TestExtracao:
    def test_extrai_blocos_gobr_e_gorules(self):
        texto = f'Regra:\n```gobr\n{DSL_FILIAL}\n```\ne também\n```gorules\n{DSL_SEMANAL}\n```\n```python\nx=1\n```'
        assert extrair_blocos_gobr(texto) == [DSL_FILIAL, DSL_SEMANAL]

    def test_sem_bloco(self):
        assert extrair_blocos_gobr('não há sintaxe para isso') == []

    def test_citacoes_simples_agrupadas_e_sem_repeticao(self):
        texto = 'usa [M2] e [E1, M3]; de novo [M2] e [E4;M1]. Ignora [X1], [1] e [E].'
        assert extrair_citacoes(texto) == ['M2', 'E1', 'M3', 'E4', 'M1']


class TestValidacaoDsl:
    def test_bloco_correto(self):
        [v] = validar_dsl(DSL_FILIAL)
        assert v['status'] == 'ok' and v['bloco'] == 'Não agendar filiais' and v['problemas'] == []

    def test_parenteses_desbalanceados(self):
        [v] = validar_dsl(DSL_SEMANAL.replace('frequencia semanal()', 'frequencia semanal('))
        assert v['status'] == 'revisao_necessaria'
        assert any('parênteses' in p for p in v['problemas'])

    def test_sem_acao(self):
        [v] = validar_dsl('parametros "x":\n    da carteira("c")\n    quando inativos para o vendedor')
        assert 'nenhuma ação de parametrização reconhecida' in v['problemas']

    def test_sem_fonte_de_clientes(self):
        [v] = validar_dsl('parametros "x":\n    quando inadimplentes\n    nao agendar')
        assert v['status'] == 'revisao_necessaria'
        assert v['problemas'] == ['nenhuma fonte de clientes (do time / da carteira / da segmentacao)']

    def test_clausula_desconhecida(self):
        [v] = validar_dsl(DSL_FILIAL + '\n    visitar com carinho')
        assert v['clausulas_nao_classificadas'] == ['visitar com carinho']

    def test_arquivo_completo_valida_so_os_parametros(self):
        dsl = f'version 1.0\n\ntime "t":\n    vendedores todostelevendas ativados\n\n{DSL_FILIAL}\n\n{DSL_SEMANAL}'
        assert [(v['bloco'], v['status']) for v in validar_dsl(dsl)] == [('Não agendar filiais', 'ok'),
                                                                         ('semanal', 'ok')]

    def test_sem_bloco_parametros(self):
        [v] = validar_dsl('time "t":\n    vendedores todostelevendas ativados')
        assert v['status'] == 'sem_bloco_parametros'


# ---------------------------------------------------------------- geração

RESPOSTA_OK = (f'Não agenda as filiais do televendas [E1, M1].\n\n```gobr\n{DSL_FILIAL}\n```\n\n'
               'Pontos de atenção: confirme o nome do time [M9].')


class BackendFake:
    def __init__(self, texto: str = RESPOSTA_OK, stop_reason: str = 'stop'):
        self.saida = SaidaModelo(texto, 'modelo-fake', stop_reason, {'input_tokens': 1200, 'output_tokens': 300})
        self.chamadas: List[tuple] = []

    def completar(self, system: str, mensagem: str) -> SaidaModelo:
        self.chamadas.append((system, mensagem))
        return self.saida


class TestGerador:
    def test_envia_system_prompt_e_mensagem_montada(self):
        backend = BackendFake()
        Gerador(backend).gerar(contexto())
        assert backend.chamadas == [(rag.SYSTEM_PROMPT, montar_mensagem(contexto()))]

    def test_interpreta_a_resposta(self):
        resp = Gerador(BackendFake()).gerar(contexto())
        assert resp.blocos_gobr == [DSL_FILIAL]
        assert resp.citacoes == ['E1', 'M1', 'M9']
        assert resp.citacoes_invalidas == ['M9']
        assert resp.dsl_valida
        assert resp.uso == {'input_tokens': 1200, 'output_tokens': 300}
        assert resp.modelo == 'modelo-fake' and resp.stop_reason == 'stop'

    def test_resposta_sem_dsl_nao_e_valida(self):
        resp = Gerador(BackendFake('O manual não tem cláusula para isso [M1].')).gerar(contexto())
        assert resp.blocos_gobr == [] and resp.validacao == [] and not resp.dsl_valida

    def test_dsl_com_problema_nao_e_valida(self):
        texto = f'```gobr\n{DSL_FILIAL}\n    visitar com carinho\n```'
        assert not Gerador(BackendFake(texto)).gerar(contexto()).dsl_valida

    def test_resposta_vazia(self):
        with pytest.raises(ErroGeracao, match='sem texto'):
            Gerador(BackendFake('  \n')).gerar(contexto())


def transporte_fake(resposta: Dict):
    chamadas: List[tuple] = []

    def enviar(url, payload, timeout):
        chamadas.append((url, payload, timeout))
        return resposta
    return enviar, chamadas


OLLAMA_OK = {'model': 'qwen2.5:7b', 'message': {'role': 'assistant', 'content': 'resposta'}, 'done_reason': 'stop',
             'prompt_eval_count': 3000, 'eval_count': 400}


class TestBackendOllama:
    def test_monta_a_requisicao(self):
        enviar, chamadas = transporte_fake(OLLAMA_OK)
        BackendOllama('m', url='http://host:1/', num_ctx=8192, max_tokens=500, timeout=7,
                      transporte=enviar).completar('SYS', 'MSG')
        [(url, payload, timeout)] = chamadas
        assert url == 'http://host:1/api/chat' and timeout == 7
        assert payload['model'] == 'm' and payload['stream'] is False
        assert payload['messages'] == [{'role': 'system', 'content': 'SYS'}, {'role': 'user', 'content': 'MSG'}]
        assert payload['options'] == {'num_ctx': 8192, 'num_predict': 500, 'temperature': 0}

    def test_interpreta_a_resposta(self):
        saida = BackendOllama(transporte=transporte_fake(OLLAMA_OK)[0]).completar('s', 'm')
        assert saida == SaidaModelo('resposta', 'qwen2.5:7b', 'stop', {'input_tokens': 3000, 'output_tokens': 400})

    def test_prompt_maior_que_a_janela(self):
        enviar = transporte_fake({**OLLAMA_OK, 'prompt_eval_count': 8000, 'eval_count': 192})[0]
        with pytest.raises(ErroGeracao, match='num_ctx=8192'):
            BackendOllama(num_ctx=8192, transporte=enviar).completar('s', 'm')

    def test_resposta_truncada(self):
        with pytest.raises(ErroGeracao, match='truncada'):
            BackendOllama(transporte=transporte_fake({**OLLAMA_OK, 'done_reason': 'length'})[0]).completar('s', 'm')

    def test_servidor_fora_do_ar(self):
        def enviar(*_):
            raise urllib.error.URLError('connection refused')
        with pytest.raises(ErroGeracao, match='está rodando'):
            BackendOllama(transporte=enviar).completar('s', 'm')

    def test_modelo_nao_baixado(self):
        def enviar(url, *_):
            raise urllib.error.HTTPError(url, 404, 'Not Found', {}, io.BytesIO(b'{"error":"model not found"}'))
        with pytest.raises(ErroGeracao, match='404.*model not found'):
            BackendOllama(transporte=enviar).completar('s', 'm')


def mensagem(texto: str = '', stop_reason: str = 'end_turn', blocos=None, stop_details=None):
    content = blocos if blocos is not None else [SimpleNamespace(type='thinking', thinking=''),
                                                 SimpleNamespace(type='text', text=texto)]
    return SimpleNamespace(content=content, stop_reason=stop_reason, stop_details=stop_details,
                           model='claude-opus-5-5', usage=SimpleNamespace(input_tokens=1200, output_tokens=300))


class ClienteFake:
    def __init__(self, resposta=None, erro: Exception = None):
        self.chamadas: List[Dict] = []
        self.beta = SimpleNamespace(messages=SimpleNamespace(create=self._create))
        self._resposta, self._erro = resposta, erro

    def _create(self, **kw):
        self.chamadas.append(kw)
        if self._erro:
            raise self._erro
        return self._resposta


class TestBackendAnthropic:
    def test_monta_a_requisicao(self):
        cliente = ClienteFake(mensagem('ok'))
        BackendAnthropic(cliente, modelo='m', esforco='low', max_tokens=123).completar('SYS', 'MSG')
        [kw] = cliente.chamadas
        assert kw['model'] == 'm' and kw['max_tokens'] == 123
        assert kw['output_config'] == {'effort': 'low'}
        assert kw['betas'] == [BETA_FALLBACK] and kw['fallbacks'] == 'default'
        assert kw['system'] == 'SYS' and kw['messages'] == [{'role': 'user', 'content': 'MSG'}]
        assert 'temperature' not in kw

    def test_junta_os_blocos_de_texto_e_ignora_os_demais(self):
        blocos = [SimpleNamespace(type='fallback'), SimpleNamespace(type='text', text='parte 1 '),
                  SimpleNamespace(type='text', text='parte 2')]
        saida = BackendAnthropic(ClienteFake(mensagem(blocos=blocos))).completar('s', 'm')
        assert saida == SaidaModelo('parte 1 parte 2', 'claude-opus-5-5', 'end_turn',
                                    {'input_tokens': 1200, 'output_tokens': 300})

    def test_recusa(self):
        msg = mensagem('', stop_reason='refusal', stop_details=SimpleNamespace(category='cyber'))
        with pytest.raises(ErroGeracao, match='cyber'):
            BackendAnthropic(ClienteFake(msg)).completar('s', 'm')

    def test_truncada(self):
        with pytest.raises(ErroGeracao, match='truncada'):
            BackendAnthropic(ClienteFake(mensagem('```gobr', stop_reason='max_tokens'))).completar('s', 'm')

    def test_credencial_invalida_vira_erro_de_geracao(self):
        anthropic = pytest.importorskip('anthropic')
        httpx = pytest.importorskip('httpx2')
        req = httpx.Request('POST', 'https://api.anthropic.com/v1/messages')
        erro = anthropic.AuthenticationError('invalid', response=httpx.Response(401, request=req), body=None)
        with pytest.raises(ErroGeracao, match='ANTHROPIC_API_KEY'):
            BackendAnthropic(ClienteFake(erro=erro)).completar('s', 'm')


def test_criar_backend():
    assert isinstance(criar_backend('ollama'), BackendOllama)
    assert criar_backend('ollama').modelo == rag.MODELO_LOCAL_PADRAO
    assert criar_backend('ollama', 'llama3.1:8b').modelo == 'llama3.1:8b'
    with pytest.raises(ValueError):
        criar_backend('openai')


def test_responder_liga_recuperacao_e_geracao():
    rec = Recuperador(BuscadorFake([exemplo('r1', DSL_FILIAL)]), BuscadorFake([trecho('6.5')]))
    backend = BackendFake()
    ctx, resp = responder('não agendar filiais', rec, Gerador(backend), k_exemplos=1, k_manual=1)
    assert ctx.refs() == ['E1', 'M1']
    assert resp.citacoes_invalidas == ['M9']
    assert 'não agendar filiais' in backend.chamadas[0][1]


def recuperador_fake() -> Recuperador:
    return Recuperador(BuscadorFake([exemplo('r1', DSL_FILIAL)]), BuscadorFake([trecho('6.5')]))


def test_cli_so_contexto_nao_chama_o_modelo(monkeypatch, capsys):
    monkeypatch.setattr(rag, 'carregar_recuperador', lambda *a, **kw: recuperador_fake())
    monkeypatch.setattr(rag, 'criar_backend', lambda *a, **kw: pytest.fail('o modelo não deveria ser chamado'))
    assert rag.main(['não agendar filiais', '--so-contexto']) == 0
    out = capsys.readouterr().out
    assert '[system]' in out and '<exemplo ref="E1"' in out and '<trecho ref="M1"' in out


def test_cli_erro_de_geracao_retorna_codigo_1(monkeypatch, capsys):
    class BackendQueFalha:
        def completar(self, *_):
            raise ErroGeracao('sem conexão com o Ollama')
    monkeypatch.setattr(rag, 'carregar_recuperador', lambda *a, **kw: recuperador_fake())
    monkeypatch.setattr(rag, 'criar_backend', lambda *a, **kw: BackendQueFalha())
    assert rag.main(['não agendar filiais']) == 1
    assert 'sem conexão com o Ollama' in capsys.readouterr().out
