from __future__ import annotations

from pathlib import Path

import pytest

from transcrever_entrada import Caixa, agrupar_blocos, limpar_texto_ocr, montar_ramos, transcrever, unir_caixas


def mapa_mental():
    """Caixas como as de um mapa mental: título à esquerda, um ramo por linha, caixas com duas linhas de texto."""
    return [
        Caixa(100, 300, 240, 325, 'Regra Teste'),
        Caixa(500, 90, 640, 115, 'Clientes Ativos'),
        Caixa(760, 80, 1100, 105, 'Clientes que compraram nos'),
        Caixa(760, 110, 1000, 135, 'últimos 30 dias'),
        Caixa(1200, 95, 1270, 115, '14 dias'),
        Caixa(500, 300, 600, 325, 'Prospects'),
        Caixa(760, 300, 1080, 325, 'Clientes que nunca compraram'),
        Caixa(1200, 300, 1260, 325, '7 dias'),
        Caixa(500, 500, 800, 525, 'Não agendar inadimplentes'),
        Caixa(600, 700, 800, 715, 'Presented with xmind'),
    ]


def test_reconstroi_titulo_e_ramos():
    t = montar_ramos(agrupar_blocos(mapa_mental()))
    assert t.titulo == 'Regra Teste'
    assert t.ramos == [
        ['Clientes Ativos', 'Clientes que compraram nos últimos 30 dias', '14 dias'],
        ['Prospects', 'Clientes que nunca compraram', '7 dias'],
        ['Não agendar inadimplentes'],
    ]
    assert t.como_texto().splitlines()[1] == '1. Clientes Ativos → Clientes que compraram nos últimos 30 dias → 14 dias'


def test_linhas_de_ramos_diferentes_nao_se_juntam():
    caixas = [Caixa(500, 100, 700, 125, 'Ramo A'), Caixa(500, 200, 700, 225, 'Ramo B')]
    assert len(agrupar_blocos(caixas)) == 2


def test_sem_titulo_quando_nao_ha_no_isolado_a_esquerda():
    caixas = [Caixa(0, 0, 300, 20, 'Clientes ativos: 14 dias'), Caixa(0, 60, 300, 80, 'Prospects: 7 dias')]
    t = montar_ramos(agrupar_blocos(caixas))
    assert t.titulo == ''
    assert [r[0] for r in t.ramos] == ['Clientes ativos: 14 dias', 'Prospects: 7 dias']


def test_unir_caixas_acrescenta_so_o_que_faltou():
    base = [Caixa(0, 0, 100, 20, '14 dias')]
    extras = [Caixa(2, 1, 98, 21, '14 dias'), Caixa(0, 100, 100, 120, '7 dias')]
    assert [c.texto for c in unir_caixas(base, extras)] == ['14 dias', '7 dias']


@pytest.mark.parametrize('bruto, limpo', [('- 14 dias', '14 dias'), ('• Clientes ativos', 'Clientes ativos'),
                                          ('-7 dias', '7 dias'), ('Regra 02', 'Regra 02')])
def test_limpar_texto_ocr(bruto, limpo):
    assert limpar_texto_ocr(bruto) == limpo


def test_imagem_usa_o_ocr_injetado(tmp_path: Path):
    img = tmp_path / 'regra.png'
    img.write_bytes(b'')
    t = transcrever(img, ocr=lambda _: mapa_mental())
    assert t.origem == 'ocr' and t.titulo == 'Regra Teste' and len(t.ramos) == 3


def test_formato_nao_suportado(tmp_path: Path):
    f = tmp_path / 'regra.docx'
    f.write_bytes(b'')
    with pytest.raises(ValueError):
        transcrever(f)
