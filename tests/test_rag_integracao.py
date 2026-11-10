"""Recuperação com os índices reais (sem chamar a API). Pulado quando o índice local do manual não existe."""
from __future__ import annotations

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
    return rag.carregar_recuperador(RAIZ / 'index', RAIZ / 'data/parametrizacoes_explicadas.jsonl',
                                    RAIZ / 'index/manual')


FILIAIS = 'não agendar clientes que são filiais'
CHOQUE = 'evitar que televendas e campo atendam o mesmo cliente no mesmo dia'
INADIMPLENTES = 'clientes com pendências financeiras não devem ser agendados'


@pytest.mark.parametrize('pergunta, secoes', [(FILIAIS, {'6.5'}), (CHOQUE, {'7.3.8'}), (INADIMPLENTES, {'6.3'})])
def test_recupera_a_secao_do_manual_com_a_resposta(recuperador, pergunta, secoes):
    ctx = recuperador.recuperar(pergunta, k_exemplos=5, k_manual=4)
    assert secoes & {t.secao for t in ctx.trechos}, [t.secao for t in ctx.trechos]


@pytest.mark.parametrize('pergunta, clausula', [
    (FILIAIS, 'cliente filial'),
    (INADIMPLENTES, 'inadimplentes'),
    # Só 13 das 1700 regras usam `sem choque`, e no texto indexado delas a frequência e a preferência vêm antes;
    # nenhuma aparece no top-60. Limitação do índice de explicações (etapa 2): o manual cobre o caso (teste acima).
    # strict: se o índice melhorar, o teste passa a falhar e este registro deve ser removido.
    pytest.param(CHOQUE, 'sem choque', marks=pytest.mark.xfail(strict=True, reason='limitação do índice da etapa 2')),
])
def test_recupera_exemplo_com_a_clausula_esperada(recuperador, pergunta, clausula):
    ctx = recuperador.recuperar(pergunta, k_exemplos=5, k_manual=0)
    assert any(clausula in e.dsl for e in ctx.exemplos), [e.id for e in ctx.exemplos]


def test_exemplos_sem_duplicatas_e_ordenados(recuperador):
    ctx = recuperador.recuperar('clientes inativos há 90 dias com frequência semanal', k_exemplos=8, k_manual=2)
    corpos = [rag._corpo_dsl(e.dsl) for e in ctx.exemplos]
    assert len(ctx.exemplos) == 8 and len(set(corpos)) == 8
    scores = [e.score for e in ctx.exemplos]
    assert scores == sorted(scores, reverse=True)


def test_todos_os_exemplos_do_dataset_passam_na_validacao_estrutural(recuperador):
    # garante que o validador usado na resposta concorda com o dataset de referência
    completos = recuperador.exemplos.completos.values()
    falhas = [r['id'] for r in completos
              if r['status_validacao'] == 'ok' and not all(v['status'] == 'ok' for v in rag.validar_dsl(r['dsl_original']))]
    assert falhas == []
