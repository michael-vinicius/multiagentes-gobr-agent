"""Recuperação com os índices reais (sem chamar modelo de linguagem). Pulado quando o índice do manual não existe."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import rag

RAIZ = Path(__file__).resolve().parents[1]

pytestmark = [
    pytest.mark.integracao,
    pytest.mark.skipif(not (RAIZ / 'index/manual/manifesto.json').exists(),
                       reason='índice do manual não gerado (python src/indexar_manual.py <pdf>)'),
]


@pytest.fixture(scope='module')
def recuperador():
    """Busca híbrida (padrão do fluxo)."""
    return rag.carregar_recuperador(RAIZ / 'index', RAIZ / 'data/parametrizacoes_explicadas.jsonl',
                                    RAIZ / 'index/manual')


@pytest.fixture(scope='module')
def recuperador_vetorial(recuperador):
    # reaproveita os índices já carregados (o modelo do manual tem 2,2 GB) em vez de carregá-los de novo
    return rag.Recuperador(recuperador.exemplos.vetorial.__self__, recuperador.manual.vetorial.__self__)


FILIAIS = 'não agendar clientes que são filiais'
CHOQUE = 'evitar que televendas e campo atendam o mesmo cliente no mesmo dia'
INADIMPLENTES = 'clientes com pendências financeiras não devem ser agendados'


@pytest.mark.parametrize('pergunta, secoes', [(FILIAIS, {'6.5'}), (CHOQUE, {'7.3.8'}), (INADIMPLENTES, {'6.3'})])
def test_recupera_a_secao_do_manual_com_a_resposta(recuperador, pergunta, secoes):
    ctx = recuperador.recuperar(pergunta, k_exemplos=5, k_manual=4)
    assert secoes & {t.secao for t in ctx.trechos}, [t.secao for t in ctx.trechos]


@pytest.mark.parametrize('pergunta, clausula', [
    (FILIAIS, 'cliente filial'), (INADIMPLENTES, 'inadimplentes'), (CHOQUE, 'sem choque'),
])
def test_recupera_exemplo_com_a_clausula_esperada(recuperador, pergunta, clausula):
    ctx = recuperador.recuperar(pergunta, k_exemplos=5, k_manual=0)
    assert any(clausula in e.dsl for e in ctx.exemplos), [e.id for e in ctx.exemplos]


# Só 13 das 1700 regras usam `sem choque`, e no texto indexado delas a frequência e a preferência vêm antes:
# a busca só vetorial não traz nenhuma no top-60 (limitação do índice da etapa 2). O BM25 da busca híbrida acha
# a palavra "choque". strict: se a busca vetorial passar a achar, este registro deve ser revisto.
@pytest.mark.xfail(strict=True, reason='limitação do índice vetorial da etapa 2, resolvida pela busca híbrida')
def test_busca_so_vetorial_nao_acha_sem_choque(recuperador_vetorial):
    ctx = recuperador_vetorial.recuperar(CHOQUE, k_exemplos=5, k_manual=0)
    assert any('sem choque' in e.dsl for e in ctx.exemplos)


@pytest.mark.parametrize('nome', ['recuperador', 'recuperador_vetorial'])
def test_exemplos_sem_duplicatas(request, nome):
    ctx = request.getfixturevalue(nome).recuperar('clientes inativos há 90 dias com frequência semanal',
                                                  k_exemplos=8, k_manual=2)
    corpos = [rag._corpo_dsl(e.dsl) for e in ctx.exemplos]
    assert len(ctx.exemplos) == 8 and len(set(corpos)) == 8
    assert [e.ref for e in ctx.exemplos] == [f'E{i}' for i in range(1, 9)]


def test_busca_vetorial_ordena_pela_similaridade(recuperador_vetorial):
    ctx = recuperador_vetorial.recuperar('clientes inativos há 90 dias com frequência semanal', k_exemplos=8, k_manual=4)
    for itens in (ctx.exemplos, ctx.trechos):
        scores = [i.score for i in itens]
        assert scores == sorted(scores, reverse=True)


def test_busca_hibrida_mantem_o_cosseno_no_score(recuperador, recuperador_vetorial):
    pergunta = 'clientes inativos há 90 dias com frequência semanal'
    vet = {e.id: e.score for e in recuperador_vetorial.recuperar(pergunta, 5, 0).exemplos}
    hib = {e.id: e.score for e in recuperador.recuperar(pergunta, 5, 0).exemplos}
    assert all(hib[i] == vet[i] for i in hib.keys() & vet.keys())
    assert all(0 < s <= 1 for s in hib.values())


def test_todos_os_exemplos_do_dataset_passam_na_validacao():
    # o validador usado na resposta, com o catálogo, precisa concordar com o dataset de referência
    from catalogo_gobr import carregar_catalogo
    catalogo = carregar_catalogo(RAIZ / 'data/parametrizacoes_explicadas.jsonl', RAIZ / 'index/manual/chunks.jsonl')
    with (RAIZ / 'data/parametrizacoes_explicadas.jsonl').open(encoding='utf-8') as f:
        registros = [json.loads(l) for l in f if l.strip()]
    falhas = [r['id'] for r in registros if r['status_validacao'] == 'ok'
              and not all(v['status'] == 'ok' for v in rag.validar_dsl(r['dsl_original'], catalogo))]
    assert len(registros) == 1700 and falhas == []
