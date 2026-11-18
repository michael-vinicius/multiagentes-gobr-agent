"""Transcreve a descrição das regras de negócio enviada como imagem ou PDF, sem modelo pago.

O analista costuma mandar um mapa mental (xmind, por exemplo) com um ramo por regra:

    Regra Maxlub ─┬─ Clientes Ativos ── Clientes com compra entre 0 e 60 dias ── 14 dias ── Somente clientes …
                  ├─ Risco de Inatividade ── …

Duas fontes de texto, ambas locais e gratuitas:
- PDF com camada de texto: as palavras e posições vêm do próprio PDF (pdfplumber), sem erro de leitura;
- imagem (PNG, JPG…) ou PDF escaneado: OCR com o RapidOCR (modelos PP-OCRv5 para alfabeto latino, via onnxruntime).

As duas produzem caixas de texto com posição. A reconstrução do layout junta as linhas de uma mesma caixa, separa
o título (o nó mais à esquerda) e monta uma linha por ramo, da esquerda para a direita. O resultado é um texto que o
modelo de linguagem local (que não lê imagens) consegue interpretar, e que o analista confere antes de seguir.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from statistics import median
from typing import Callable, Iterable, List, Optional, Sequence

EXTENSOES_IMAGEM = {'.png', '.jpg', '.jpeg', '.bmp', '.webp', '.tif', '.tiff'}
# marcas d'água de ferramentas de mapa mental, que não fazem parte da regra
_MARCAS_DAGUA = re.compile(r'^(presented with|made with|created with)\b', re.I)


@dataclass(frozen=True)
class Caixa:
    """Um trecho de texto e sua posição na página (origem no canto superior esquerdo)."""
    x0: float
    y0: float
    x1: float
    y1: float
    texto: str

    @property
    def altura(self) -> float:
        return self.y1 - self.y0

    @property
    def centro_y(self) -> float:
        return (self.y0 + self.y1) / 2


@dataclass
class Bloco:
    """Uma caixa do mapa mental: uma ou mais linhas de texto empilhadas."""
    linhas: List[Caixa] = field(default_factory=list)

    @property
    def x0(self) -> float:
        return min(c.x0 for c in self.linhas)

    @property
    def x1(self) -> float:
        return max(c.x1 for c in self.linhas)

    @property
    def y0(self) -> float:
        return min(c.y0 for c in self.linhas)

    @property
    def y1(self) -> float:
        return max(c.y1 for c in self.linhas)

    @property
    def centro_y(self) -> float:
        return (self.y0 + self.y1) / 2

    @property
    def texto(self) -> str:
        return ' '.join(c.texto.strip() for c in sorted(self.linhas, key=lambda c: c.y0)).strip()


@dataclass
class Transcricao:
    titulo: str
    ramos: List[List[str]]
    origem: str  # 'pdf-texto', 'ocr' ou 'texto'

    def como_texto(self) -> str:
        partes = []
        if self.titulo:
            partes.append(f'Título: {self.titulo}')
        for i, ramo in enumerate(self.ramos, 1):
            partes.append(f'{i}. ' + ' → '.join(ramo))
        return '\n'.join(partes)


# ---------------------------------------------------------------- reconstrução do layout

def _sobreposicao(a0: float, a1: float, b0: float, b1: float) -> float:
    return max(0.0, min(a1, b1) - max(a0, b0))


def agrupar_blocos(caixas: Iterable[Caixa]) -> List[Bloco]:
    """Junta as linhas que formam uma mesma caixa: alinhadas na horizontal e coladas na vertical."""
    blocos: List[Bloco] = []
    for c in sorted(caixas, key=lambda c: (c.y0, c.x0)):
        if not c.texto.strip() or _MARCAS_DAGUA.match(c.texto.strip()):
            continue
        destino = None
        for b in blocos:
            ultima = max(b.linhas, key=lambda l: l.y1)
            largura = min(c.x1 - c.x0, ultima.x1 - ultima.x0)
            if largura <= 0:
                continue
            alinhada = _sobreposicao(c.x0, c.x1, ultima.x0, ultima.x1) >= 0.3 * largura
            # o espaço entre linhas da mesma caixa é bem menor que a altura de uma linha
            vao = c.y0 - ultima.y1
            colada = -0.5 * ultima.altura <= vao <= 0.8 * max(ultima.altura, c.altura)
            if alinhada and colada:
                destino = b
                break
        if destino is None:
            blocos.append(Bloco([c]))
        else:
            destino.linhas.append(c)
    return blocos


def montar_ramos(blocos: Sequence[Bloco]) -> Transcricao:
    """Separa o título (nó mais à esquerda, sozinho na sua coluna) e monta uma linha por ramo."""
    if not blocos:
        return Transcricao('', [], '')
    restantes = sorted(blocos, key=lambda b: b.x0)
    titulo = ''
    raiz = restantes[0]
    outros = restantes[1:]
    if outros and raiz.x1 <= min(b.x0 for b in outros) + 1:
        titulo = raiz.texto
        restantes = outros

    # âncoras: a 1ª coluna de caixas depois do título (o nome de cada ramo)
    x_min = min(b.x0 for b in restantes)
    alturas = [l.altura for b in restantes for l in b.linhas]
    tolerancia_x = 1.5 * (median(alturas) if alturas else 10)
    ancoras = sorted([b for b in restantes if b.x0 <= x_min + tolerancia_x], key=lambda b: b.centro_y)
    ramos: List[List[Bloco]] = [[a] for a in ancoras]
    for b in restantes:
        if b in ancoras:
            continue
        # cada detalhe vai para o ramo cujo nome está mais perto na vertical
        i = min(range(len(ancoras)), key=lambda k: abs(ancoras[k].centro_y - b.centro_y))
        ramos[i].append(b)
    return Transcricao(titulo, [[b.texto for b in sorted(r, key=lambda b: b.x0)] for r in ramos], '')


# ---------------------------------------------------------------- fontes de caixas

def caixas_do_pdf(caminho: Path, pagina: int = 0) -> List[Caixa]:
    """Caixas a partir da camada de texto do PDF: palavras da mesma linha, separadas por vãos grandes, viram caixas."""
    import pdfplumber
    with pdfplumber.open(str(caminho)) as pdf:
        if pagina >= len(pdf.pages):
            return []
        palavras = pdf.pages[pagina].extract_words(keep_blank_chars=False, use_text_flow=False)
    linhas: List[List[dict]] = []
    for w in sorted(palavras, key=lambda w: (round(w['top']), w['x0'])):
        alvo = next((l for l in linhas if abs(l[0]['top'] - w['top']) <= 2), None)
        if alvo is None:
            linhas.append([w])
        else:
            alvo.append(w)
    caixas: List[Caixa] = []
    for linha in linhas:
        linha.sort(key=lambda w: w['x0'])
        atual = [linha[0]]
        for w in linha[1:]:
            altura = atual[-1]['bottom'] - atual[-1]['top']
            # entre palavras da mesma caixa há um espaço; entre caixas diferentes, um vão maior que a altura da letra
            if w['x0'] - atual[-1]['x1'] > 1.0 * altura:
                caixas.append(_caixa_de_palavras(atual))
                atual = [w]
            else:
                atual.append(w)
        caixas.append(_caixa_de_palavras(atual))
    return caixas


def _caixa_de_palavras(ws: List[dict]) -> Caixa:
    return Caixa(min(w['x0'] for w in ws), min(w['top'] for w in ws), max(w['x1'] for w in ws),
                 max(w['bottom'] for w in ws), ' '.join(w['text'] for w in ws))


_OCR = None


def _motor_ocr():
    global _OCR
    if _OCR is None:
        from rapidocr import LangRec, ModelType, OCRVersion, RapidOCR
        # reconhecimento para alfabeto latino: o modelo padrão (chinês/inglês) perde os acentos do português
        _OCR = RapidOCR(params={'Rec.lang_type': LangRec.LATIN, 'Rec.ocr_version': OCRVersion.PPOCRV5,
                                'Rec.model_type': ModelType.MOBILE, 'Global.log_level': 'error'})
    return _OCR


# O detector do OCR é sensível à escala: caixas curtas ("7 dias") somem numa escala e aparecem em outra, e não há uma
# escala que acerte todas. Medição nos 3 exemplos renderizados em 4 resoluções, PNG e JPEG (24 imagens), contando as
# caixas "N dias" lidas: original + referência 21/24; original + metade 22/24; referência + metade dela 23/24
# (≈ 6 s por imagem); uma 3ª escala não acrescentou acertos. A falha restante é um "7 dias" do Infinitto em 1569 px; o agente pergunta pela frequência que
# faltar, e o analista confere a transcrição.
LARGURA_REFERENCIA_OCR = 2400


def _ocr_uma_escala(img, fator: float, confianca_minima: float) -> List[Caixa]:
    import numpy as np
    from PIL import Image
    if abs(fator - 1) > 1e-6:
        img = img.resize((round(img.width * fator), round(img.height * fator)), Image.LANCZOS)
    r = _motor_ocr()(np.asarray(img))
    if r.txts is None:
        return []
    out = []
    for caixa, texto, score in zip(r.boxes, r.txts, r.scores):
        texto = limpar_texto_ocr(texto)
        if score < confianca_minima or not texto:
            continue
        xs, ys = [p[0] / fator for p in caixa], [p[1] / fator for p in caixa]  # volta para a escala original
        out.append(Caixa(float(min(xs)), float(min(ys)), float(max(xs)), float(max(ys)), texto))
    return out


def _area(c: Caixa) -> float:
    return max(0.0, c.x1 - c.x0) * max(0.0, c.y1 - c.y0)


def unir_caixas(base: List[Caixa], extras: Iterable[Caixa], limite: float = 0.3) -> List[Caixa]:
    """Acrescenta à `base` as caixas de `extras` que não se sobrepõem (mais que `limite` da menor área) a nenhuma."""
    out = list(base)
    for e in extras:
        if all(_sobreposicao(e.x0, e.x1, b.x0, b.x1) * _sobreposicao(e.y0, e.y1, b.y0, b.y1)
               <= limite * min(_area(e), _area(b)) for b in out):
            out.append(e)
    return out


def caixas_por_ocr(imagem, confianca_minima: float = 0.5) -> List[Caixa]:
    """Caixas a partir de uma imagem (caminho ou PIL.Image) com OCR local, em duas escalas.

    1ª passada na largura de referência; 2ª na metade dela. Da 2ª entram só as caixas que a 1ª não leu.
    As posições voltam para a escala original da imagem.
    """
    from PIL import Image
    img = Image.open(imagem) if isinstance(imagem, (str, Path)) else imagem
    img = img.convert('RGB')
    fator = LARGURA_REFERENCIA_OCR / img.width
    caixas = _ocr_uma_escala(img, fator, confianca_minima)
    return unir_caixas(caixas, _ocr_uma_escala(img, fator / 2, confianca_minima))


_MARCADOR_INICIAL = re.compile(r'^[\s\-–—•·*>]+(?=\S)')


def limpar_texto_ocr(texto: str) -> str:
    """Tira marcadores que o OCR lê nas bordas e nos conectores do mapa mental ("- 14 dias", "• Clientes …")."""
    return _MARCADOR_INICIAL.sub('', texto).strip()


def _renderizar_pdf(caminho: Path, pagina: int = 0, escala: float = 2.0):
    import pypdfium2 as pdfium
    return pdfium.PdfDocument(str(caminho))[pagina].render(scale=escala).to_pil()


def transcrever(caminho: Path, forcar_ocr: bool = False,
                ocr: Callable[[object], List[Caixa]] = caixas_por_ocr) -> Transcricao:
    """Transcreve um PDF ou uma imagem com a descrição das regras.

    PDF com texto suficiente usa a camada de texto; PDF escaneado (ou `forcar_ocr`) é renderizado e passa pelo OCR.
    """
    caminho = Path(caminho)
    sufixo = caminho.suffix.lower()
    if sufixo == '.pdf':
        caixas = [] if forcar_ocr else caixas_do_pdf(caminho)
        if sum(len(c.texto) for c in caixas) >= 20:
            origem = 'pdf-texto'
        else:
            caixas, origem = ocr(_renderizar_pdf(caminho)), 'ocr'
    elif sufixo in EXTENSOES_IMAGEM:
        caixas, origem = ocr(caminho), 'ocr'
    else:
        raise ValueError(f'formato não suportado: {sufixo} (use PDF ou imagem: {", ".join(sorted(EXTENSOES_IMAGEM))})')
    t = montar_ramos(agrupar_blocos(caixas))
    t.origem = origem
    return t


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description='Transcreve a imagem ou o PDF de uma regra de negócio (sem modelo pago).')
    ap.add_argument('arquivo', type=Path)
    ap.add_argument('--ocr', action='store_true', help='Força o OCR mesmo em PDF com camada de texto')
    args = ap.parse_args(argv)
    t = transcrever(args.arquivo, forcar_ocr=args.ocr)
    print(f'[origem: {t.origem}]')
    print(t.como_texto())
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
