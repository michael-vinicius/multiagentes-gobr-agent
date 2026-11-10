from __future__ import annotations

from typing import Dict, List

import pytest

from busca_hibrida import BM25, BuscaHibrida, fundir_rrf, tokenizar


class TestTokenizar:
    def test_minusculas_sem_acento_e_sem_plural(self):
        assert tokenizar('Inativos PARA o Vendedor: Frequência') == ['inativo', 'vendedor', 'frequencia']

    def test_mantem_sem_e_nao_que_fazem_parte_de_clausulas(self):
        assert tokenizar('clientes sem venda e não agendar') == ['sem', 'venda', 'nao', 'agendar']

    def test_palavras_curtas_nao_perdem_o_s(self):
        assert tokenizar('mes vez gas') == ['mes', 'vez', 'gas']


class TestBM25:
    TEXTOS = ['quando sem venda frequencia semanal', 'quando inadimplentes nao agendar',
              'quando ativos para o vendedor frequencia de 21 dias', 'preferencia nos dias uteis']

    def test_documento_com_o_termo_raro_vem_primeiro(self):
        s = BM25(self.TEXTOS).pontuar('clientes sem vendas')
        assert max(range(4), key=s.__getitem__) == 0

    def test_termo_desconhecido_pontua_zero(self):
        assert BM25(self.TEXTOS).pontuar('palavra inexistente') == [0.0] * 4

    def test_termo_comum_vale_menos_que_termo_raro(self):
        bm = BM25(self.TEXTOS)
        assert bm.idf['quando'] < bm.idf['inadimplente']

    def test_lista_vazia(self):
        assert BM25([]).pontuar('x') == []


class TestRRF:
    def test_aparece_bem_nas_duas_listas_vence(self):
        assert fundir_rrf([[1, 2, 3], [3, 1, 4]])[:2] == [1, 3]

    def test_item_de_uma_lista_so_tambem_entra(self):
        assert set(fundir_rrf([[1], [2]])) == {1, 2}

    def test_empate_e_desfeito_pelo_indice(self):
        assert fundir_rrf([[2], [1]]) == [1, 2]


DOCS = [{'id': f'd{i}', 'nome': n} for i, n in enumerate(['frequencia semanal', 'sem venda', 'inadimplentes', 'curva A'])]
TEXTOS = ['frequencia semanal para ativos', 'quando sem venda', 'quando inadimplentes nao agendar',
          'quando curva A com a empresa']


def vetorial_fake(ordem: List[int]):
    chamadas: List[tuple] = []

    def buscar(consulta: str, k: int) -> List[Dict]:
        chamadas.append((consulta, k))
        return [{**DOCS[i], 'score': round(0.9 - 0.1 * pos, 2)} for pos, i in enumerate(ordem)][:k]
    return buscar, chamadas


class TestBuscaHibrida:
    def test_documento_achado_so_pelas_palavras_entra_no_resultado(self):
        # o vetor coloca "sem venda" em último; o BM25 o coloca em primeiro
        buscar, _ = vetorial_fake([0, 2, 3, 1])
        res = BuscaHibrida(buscar, DOCS, TEXTOS, profundidade=2).buscar('clientes sem venda', 2)
        assert 'd1' in [r['id'] for r in res]

    def test_score_continua_sendo_o_cosseno(self):
        buscar, chamadas = vetorial_fake([0, 2, 3, 1])
        res = BuscaHibrida(buscar, DOCS, TEXTOS).buscar('sem venda', 4)
        assert {r['id']: r['score'] for r in res} == {'d0': 0.9, 'd2': 0.8, 'd3': 0.7, 'd1': 0.6}
        assert chamadas == [('sem venda', 4)]  # pede todos para ter o cosseno de cada um

    def test_resultado_mantem_os_campos_do_documento(self):
        buscar, _ = vetorial_fake([0, 1, 2, 3])
        [r] = BuscaHibrida(buscar, DOCS, TEXTOS).buscar('curva A', 1)
        assert set(r) == {'id', 'nome', 'score'}

    def test_k_zero(self):
        buscar, chamadas = vetorial_fake([0, 1, 2, 3])
        assert BuscaHibrida(buscar, DOCS, TEXTOS).buscar('x', 0) == [] and chamadas == []

    def test_tamanhos_diferentes(self):
        with pytest.raises(ValueError):
            BuscaHibrida(vetorial_fake([0])[0], DOCS, TEXTOS[:2])
