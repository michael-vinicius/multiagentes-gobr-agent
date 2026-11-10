from __future__ import annotations

import pytest

from avaliar_rag import CASOS, avaliar_caso, faltando
from rag import ErroGeracao, Gerador, Recuperador
from test_rag import DSL_FILIAL, BackendFake, BuscadorFake, exemplo, trecho

RESPOSTA = f'Não agenda as filiais [E1, M1].\n\n```gobr\n{DSL_FILIAL}\n```'
CLAUSULAS = [('cliente filial', 'e o cliente filial'), ('nao agendar',)]


def recuperador(dsl: str = DSL_FILIAL) -> Recuperador:
    return Recuperador(BuscadorFake([exemplo('r1', dsl)]), BuscadorFake([trecho('6.5')]))


def avaliar(texto: str, clausulas=CLAUSULAS, rec: Recuperador = None):
    return avaliar_caso(rec or recuperador(), Gerador(BackendFake(texto)), 'pergunta', clausulas, 1, 1)


def test_resposta_correta_e_aprovada():
    r = avaliar(RESPOSTA)
    assert r['aprovado'] and r['contexto_cobre'] and r['clausulas_faltando'] == []


class TestFaltando:
    def test_sem_acento_maiusculas_ou_espacos_extras(self):
        assert faltando('quando Cliente   Filial\n    Não agendar', CLAUSULAS) == []

    def test_basta_uma_alternativa_do_grupo(self):
        assert faltando('quando e o cliente filial', [('cliente principal', 'e o cliente filial')]) == []

    def test_grupo_ausente_e_identificado_pela_primeira_forma(self):
        assert faltando('nao agendar', CLAUSULAS) == ['cliente filial']


def test_texto_entre_aspas_nao_conta_como_clausula():
    dsl = 'parametros "x":\n    da carteira("curva A com a empresa")\n    frequencia semanal()'
    r = avaliar(f'[E1]\n```gobr\n{dsl}\n```', clausulas=[('curva a com a empresa',)])
    assert r['clausulas_faltando'] == ['curva a com a empresa'] and not r['aprovado']


@pytest.mark.parametrize('texto, motivo', [
    (RESPOSTA.replace(' [E1, M1]', ''), 'citou_fontes'),
    (RESPOSTA.replace('[E1, M1]', '[E7]'), 'citacoes_invalidas'),
    (RESPOSTA.replace('    do time("televendas")\n', ''), 'dsl_valida'),
    ('Não há cláusula para isso [M1].', 'tem_dsl'),
])
def test_reprova(texto, motivo):
    r = avaliar(texto)
    assert not r['aprovado']
    assert bool(r[motivo]) == (motivo == 'citacoes_invalidas')


def test_clausula_faltando_reprova():
    r = avaliar(RESPOSTA, clausulas=[('cliente filial',), ('frequencia semanal()',)])
    assert not r['aprovado'] and r['clausulas_faltando'] == ['frequencia semanal()']


def test_cobertura_do_contexto_separa_falha_de_busca_de_falha_de_geracao():
    dsl_sem_filial = DSL_FILIAL.replace('cliente filial', 'inadimplentes')
    r = avaliar(RESPOSTA, rec=recuperador(dsl_sem_filial))
    # a regra gerada está certa, mas a cláusula não estava no contexto: o mérito não é da busca
    assert r['aprovado'] and not r['contexto_cobre'] and r['fora_do_contexto'] == ['cliente filial']


def test_erro_de_geracao_e_registrado():
    class BackendQueFalha:
        def completar(self, *_):
            raise ErroGeracao('sem conexão')
    r = avaliar_caso(recuperador(), Gerador(BackendQueFalha()), 'p', CLAUSULAS, 1, 1)
    assert r['erro'] == 'sem conexão' and not r['aprovado']


def test_casos_bem_formados():
    assert len({p for p, _ in CASOS}) == len(CASOS)
    assert all(clausulas and all(grupo for grupo in clausulas) for _, clausulas in CASOS)
