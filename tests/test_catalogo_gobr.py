from __future__ import annotations

import json
from pathlib import Path

import pytest

from catalogo_gobr import Catalogo, carregar_catalogo, molde, partes
from gerar_explicacoes_gobr import parse_blocks

RAIZ = Path(__file__).resolve().parents[1]
REGRA = ('parametros "Inativos":\n    da carteira("carteira fixa")\n'
         '    quando inativos para o vendedor e recencia de positivacao entre 10 dias e 90 dias\n'
         '    frequencia de 14 dias')


@pytest.fixture
def catalogo() -> Catalogo:
    c = Catalogo()
    c.adicionar_dsl(REGRA)
    c.adicionar_tabela('inatividade de <<N>> dias')
    c.adicionar_tabela('curva A com a empresa')
    return c


class TestMolde:
    def test_normaliza_acentos_numeros_textos_e_espacos(self):
        assert molde('quando  Inatividade de 90 dias') == 'quando inatividade de N dias'
        assert molde('do time ("Televendas")') == 'do time(S)'
        assert molde('quando ramo de atividade igual("A", "B")') == 'quando ramo de atividade igual(S)'
        assert molde('e media faturada no ano com a empresa maior que R$ 1.500,00') == \
            'e media faturada no ano com a empresa maior que r$ N'

    def test_partes_quebram_no_e_sem_o_prefixo(self):
        assert partes('quando inativos para o vendedor e inadimplentes') == ['inativos para o vendedor', 'inadimplentes']
        assert partes('e adimplentes') == ['adimplentes']


class TestConhece:
    def test_condicoes_das_regras_reais(self, catalogo):
        assert catalogo.problemas(['quando inativos para o vendedor']) == []
        # o intervalo é quebrado do mesmo jeito dos dois lados
        assert catalogo.problemas(['quando recencia de positivacao entre 30 dias e 60 dias']) == []

    def test_molde_do_manual_aceita_qualquer_valor(self, catalogo):
        assert catalogo.problemas(['quando inatividade de 180 dias']) == []

    def test_condicao_inventada_e_acusada_com_sugestao(self, catalogo):
        [p] = catalogo.problemas(['quando inativos para o gerente'])
        assert 'condição fora do manual e das regras reais' in p
        assert '"inativos para o vendedor"' in p

    def test_acoes_nao_sao_conferidas(self, catalogo):
        assert catalogo.problemas(['frequencia do vendedor ou de qualquer vendedor ou de 35 dias']) == []

    def test_molde_so_com_marcador_e_ignorado(self):
        c = Catalogo()
        c.adicionar_tabela('<<N>>')
        assert c.padroes == [] and c.problemas(['quando qualquer coisa']) != []


class TestFiltroComoNome:
    def test_filtro_usado_como_nome_da_fonte(self, catalogo):
        catalogo.condicoes.add('curva a com a empresa')
        [p] = catalogo.problemas(['da carteira("curva A com a empresa")'])
        assert 'é um filtro, não o nome de uma fonte' in p

    def test_nome_real_de_fonte_nao_e_acusado(self, catalogo):
        assert catalogo.problemas(['da carteira("carteira fixa")', 'da carteira("<nome da carteira>")']) == []

    def test_nome_que_tambem_e_fonte_real_nao_e_acusado(self, catalogo):
        catalogo.condicoes.add('inadimplentes')
        catalogo.nomes_de_fonte.add('inadimplentes')
        assert catalogo.problemas(['da segmentacao("inadimplentes")']) == []


def test_carregar_catalogo_dos_arquivos(tmp_path):
    explicadas = tmp_path / 'explicadas.jsonl'
    explicadas.write_text(json.dumps({'dsl_original': REGRA}) + '\n', encoding='utf-8')
    chunks = tmp_path / 'chunks.jsonl'
    texto = ('Manual > 6.1\n\n| Filtro | Descrição |\n|---|---|\n| `inatividade de <<N>> dias` | … |\n\n'
             '```gobr\nparametros "x":\n    da carteira("c")\n    quando cliente filial\n    nao agendar\n```')
    chunks.write_text(json.dumps({'texto': texto}) + '\n', encoding='utf-8')
    c = carregar_catalogo(explicadas, chunks)
    assert c.problemas(['quando inatividade de 30 dias', 'quando cliente filial', 'quando inadimplentes']) == [
        c.problemas(['quando inadimplentes'])[0]]
    sem_manual = carregar_catalogo(explicadas, tmp_path / 'nao_existe.jsonl')
    assert sem_manual.problemas(['quando cliente filial']) != []


def test_nenhuma_regra_real_e_acusada():
    c = carregar_catalogo(RAIZ / 'data/parametrizacoes_explicadas.jsonl', None)
    with (RAIZ / 'data/parametrizacoes_explicadas.jsonl').open(encoding='utf-8') as f:
        regras = [json.loads(l)['dsl_original'] for l in f if l.strip()]
    acusadas = [p for d in regras for b in parse_blocks(d) if b['type'] == 'parametros' for p in c.problemas(b['clauses'])]
    assert acusadas == []


@pytest.mark.integracao
@pytest.mark.skipif(not (RAIZ / 'index/manual/chunks.jsonl').exists(), reason='índice do manual não gerado')
def test_condicoes_dos_exemplos_do_manual_sao_reconhecidas_sem_conhece_los():
    """Estimativa de falso positivo: catálogo com as regras reais e as tabelas, sem os exemplos de código."""
    from catalogo_gobr import _CODIGO, _LINHA_TABELA
    textos = [json.loads(l)['texto'] for l in (RAIZ / 'index/manual/chunks.jsonl').read_text(encoding='utf-8').splitlines()
              if l.strip()]
    c = carregar_catalogo(RAIZ / 'data/parametrizacoes_explicadas.jsonl', None)
    for t in textos:
        for entrada in _LINHA_TABELA.findall(t):
            c.adicionar_tabela(entrada)
    clausulas = [cl for t in textos for cod in _CODIGO.findall(t) for b in parse_blocks(cod)
                 if b['type'] == 'parametros' for cl in b['clauses']]
    assert len(clausulas) >= 40
    assert c.problemas(clausulas) == []
