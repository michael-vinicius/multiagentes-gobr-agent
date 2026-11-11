from __future__ import annotations

import pytest

from avaliar_rag import CASOS, CASOS_AJUSTE, CASOS_TESTE, avaliar_caso, faltando
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


def test_palavra_inteira_adimplentes_nao_casa_em_inadimplentes():
    assert faltando('quando inadimplentes', [('adimplentes',)]) == ['adimplentes']
    assert faltando('quando adimplentes', [('adimplentes',)]) == []


def test_parenteses_no_fim_da_alternativa():
    assert faltando('frequencia quinzenal()', [('frequencia quinzenal()',)]) == []


def test_conjuntos_de_ajuste_e_teste_sao_disjuntos():
    assert not {p for p, _ in CASOS_AJUSTE} & {p for p, _ in CASOS_TESTE}
    assert len(CASOS) == len(CASOS_AJUSTE) + len(CASOS_TESTE)


def test_clausulas_do_gabarito_existem_nas_regras_reais_ou_no_manual():
    # protege o gabarito contra sintaxe inventada; quando o manual não está disponível, usa só as regras reais
    import json
    from pathlib import Path
    from avaliar_rag import _norm, _sem_aspas
    raiz = Path(__file__).resolve().parents[1]
    corpus = [r['dsl_original'] for r in map(json.loads, (raiz / 'data/parametrizacoes_explicadas.jsonl')
                                             .read_text(encoding='utf-8').splitlines())]
    manual = raiz / 'index/manual/chunks.jsonl'
    if manual.exists():
        corpus += [json.loads(l)['texto'] for l in manual.read_text(encoding='utf-8').splitlines()]
    texto = _norm(_sem_aspas('\n'.join(corpus)))
    casos = CASOS if manual.exists() else CASOS_TESTE  # parte do gabarito de ajuste só existe no manual
    for pergunta, clausulas in casos:
        assert faltando(texto, clausulas, forma=True) == [], pergunta
    # cada alternativa individual também precisa existir (uma alternativa inventada passaria despercebida)
    for pergunta, clausulas in casos:
        for grupo in clausulas:
            for alt in grupo:
                assert faltando(texto, [(alt,)], forma=True) == [], (pergunta, alt)


def test_cobertura_por_forma_ignora_os_numeros():
    assert faltando('frequencia de 30 dias', [('frequencia de 14 dias',)]) == ['frequencia de 14 dias']
    assert faltando('frequencia de 30 dias', [('frequencia de 14 dias',)], forma=True) == []
    assert faltando('| `inatividade de <<N>> dias` |', [('inatividade de 90 dias',)], forma=True) == []
    assert faltando('frequencia semanal()', [('frequencia de 14 dias',)], forma=True) == ['frequencia de 14 dias']


def test_reavaliar_aplica_gabarito_e_validador_atuais_sem_gerar_de_novo():
    from avaliar_rag import reavaliar
    from catalogo_gobr import Catalogo
    pergunta, _ = CASOS_AJUSTE[0]  # filiais: do time + cliente filial + nao agendar
    salvo = avaliar_caso(recuperador(), Gerador(BackendFake(RESPOSTA)), pergunta, CASOS_AJUSTE[0][1], 1, 1)
    salvo.pop('conjunto', None)
    assert salvo['aprovado']
    catalogo = Catalogo()  # catálogo vazio: a condição "cliente filial" passa a ser desconhecida
    [r] = reavaliar([salvo], catalogo)
    assert r['conjunto'] == 'ajuste' and not r['dsl_valida'] and not r['aprovado']
    assert r['contexto_cobre'] == salvo['contexto_cobre']
    [r] = reavaliar([salvo], None)
    assert r['aprovado']


def test_reavaliar_mantem_casos_com_erro():
    from avaliar_rag import reavaliar
    pergunta, _ = CASOS_TESTE[0]
    [r] = reavaliar([{'pergunta': pergunta, 'erro': 'sem conexão', 'aprovado': False}], None)
    assert r['conjunto'] == 'teste' and not r['aprovado']
