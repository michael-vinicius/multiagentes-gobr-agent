from __future__ import annotations

import re
from pathlib import Path
from typing import Callable, Dict, List, Optional

import pdfplumber

# Layout do manual (pontos PDF): cabeçalho e rodapé repetidos ficam fora desta faixa vertical.
TOPO_CONTEUDO, BASE_CONTEUDO = 70, 780
LARGURA_COURIER = 6.0          # Courier 10pt: cada caractere ocupa 6pt, o que dá a indentação do código
RECUO_CODIGO = 3.0             # distância entre a borda do bloco cinza e o início do texto
ESPACO_MIN = 1.0               # vão horizontal entre palavras a partir do qual há um espaço
ENTRELINHA_MAX = 17.5          # linhas de um mesmo parágrafo distam 16pt; itens e parágrafos novos, 19pt ou mais
ENTRELINHA_SIMBOLO = 21.0      # a seta (fonte Symbol) aumenta a entrelinha; vale só se a frase não terminou
RE_TITULO = re.compile(r'^(\d+(?:\.\d+)*)\s+(.+)$')
RE_ITEM_NUMERADO = re.compile(r'^(\d+)\.\s*(\S.*)$')
TAMANHO_TITULO = {16.0: 'capitulo', 12.0: 'secao', 9.5: 'subsecao'}


def _cinza(rect: Dict) -> bool:
    cor = rect.get('non_stroking_color')
    return isinstance(cor, (tuple, list)) and len(cor) == 3 and all(0.9 < c < 1.0 for c in cor)


def _dentro(palavra: Dict, rect: Dict) -> bool:
    cx, cy = (palavra['x0'] + palavra['x1']) / 2, (palavra['top'] + palavra['bottom']) / 2
    return rect['x0'] <= cx <= rect['x1'] and rect['top'] <= cy <= rect['bottom']


def _no_codigo(palavra: Dict, rect: Dict) -> bool:
    # linhas de código longas ultrapassam a borda direita do bloco cinza
    cy = (palavra['top'] + palavra['bottom']) / 2
    return palavra['x0'] >= rect['x0'] - 2 and rect['top'] <= cy <= rect['bottom']


def _texto(palavra: Dict) -> str:
    # a fonte Symbol do PDF só é usada para a seta "→", que o extrator lê como a ligadura "ﬁ"
    return '→' if 'Symbol' in palavra['fontname'] else palavra['text']


def _eh_codigo(palavra: Dict) -> bool:
    return palavra['fontname'].startswith('Courier')


def _agrupar_linhas(palavras: List[Dict]) -> List[List[Dict]]:
    linhas: List[List[Dict]] = []
    for p in sorted(palavras, key=lambda p: (p['top'], p['x0'])):
        # Courier e Helvetica na mesma linha têm topos ligeiramente diferentes
        if linhas and p['top'] - linhas[-1][0]['top'] <= 3:
            linhas[-1].append(p)
        else:
            linhas.append([p])
    return [sorted(l, key=lambda p: p['x0']) for l in linhas]


def _juntar(palavras: List[Dict], marcar_codigo: bool = True) -> str:
    """Junta palavras em texto, envolvendo trechos em Courier com crases (código inline)."""
    partes: List[str] = []
    anterior: Optional[Dict] = None
    em_codigo = False
    for p in palavras:
        codigo = marcar_codigo and _eh_codigo(p)
        nova_linha = anterior is not None and abs(p['top'] - anterior['top']) > 3
        # palavra hifenizada na quebra de linha ("pré-" + "calculada") continua sem espaço
        hifen = nova_linha and len(anterior['text']) > 1 and anterior['text'].endswith('-')
        espaco = anterior is not None and not hifen and (nova_linha or p['x0'] - anterior['x1'] > ESPACO_MIN)
        if codigo != em_codigo:
            if em_codigo:
                partes.append('`')
            if espaco:
                partes.append(' ')
            if codigo:
                partes.append('`')
            em_codigo = codigo
        elif espaco:
            partes.append(' ')
        partes.append(_texto(p))
        anterior = p
    if em_codigo:
        partes.append('`')
    return ''.join(partes)


def _bloco_codigo(palavras: List[Dict], rect: Dict) -> str:
    linhas = _agrupar_linhas(palavras)
    vaos = [b[0]['top'] - a[0]['top'] for a, b in zip(linhas, linhas[1:])]
    passo = min(vaos) if vaos and min(vaos) < 20 else 16.0
    saida: List[str] = []
    for i, linha in enumerate(linhas):
        if i:
            saida.extend([''] * (round(vaos[i - 1] / passo) - 1))
        indent = max(0, round((linha[0]['x0'] - rect['x0'] - RECUO_CODIGO) / LARGURA_COURIER))
        saida.append(' ' * indent + _juntar(linha, marcar_codigo=False))
    return '\n'.join(saida)


def _ajustar(textos: List[str], n: int) -> List[str]:
    """Normaliza a linha para n colunas; o texto de células excedentes (falhas de diagramação) vai para a última."""
    if len(textos) > n:
        extra = ' '.join(t for t in textos[n:] if t)
        textos = textos[:n - 1] + [f'{textos[n - 1]} {extra}'.strip()]
    return textos + [''] * (n - len(textos))


def _tabelas(celulas: List[Dict], palavras: List[Dict]) -> List[Dict]:
    """Reconstrói as tabelas a partir dos retângulos das células (o cabeçalho tem fundo cinza)."""
    linhas: List[List[Dict]] = []
    for c in sorted(celulas, key=lambda c: (round(c['top']), c['x0'])):
        if linhas and abs(c['top'] - linhas[-1][0]['top']) <= 2:
            linhas[-1].append(c)
        else:
            linhas.append([c])
    tabelas: List[Dict] = []
    for linha in linhas:
        textos = [_juntar([p for p in palavras if _dentro(p, c)]) for c in linha]
        x0 = round(linha[0]['x0'])
        anterior = tabelas[-1] if tabelas else None
        if all(_cinza(c) for c in linha):
            tabelas.append({'tipo': 'tabela', 'top': linha[0]['top'], 'cabecalho': textos, 'linhas': [], 'x0': x0, 'n': len(textos)})
        elif anterior and anterior['x0'] == x0 and linha[0]['top'] - anterior['bottom'] < 5:
            anterior['linhas'].append(_ajustar(textos, anterior['n']))
        else:
            tabelas.append({'tipo': 'tabela', 'top': linha[0]['top'], 'cabecalho': None, 'linhas': [textos], 'x0': x0, 'n': len(textos)})
        tabelas[-1]['bottom'] = max(c['bottom'] for c in linha)
    return tabelas


def _titulo(linha: List[Dict]) -> Optional[str]:
    """Nível do título se a linha for inteiramente em negrito num dos tamanhos de título, senão None."""
    if not all('Bold' in p['fontname'] for p in linha):
        return None
    nivel = TAMANHO_TITULO.get(round(linha[0]['size'], 1))
    if nivel == 'subsecao' and linha[0]['x0'] > 75:
        return None
    return nivel


def _emendar(texto: str, continuacao: str) -> str:
    """Junta a linha seguinte de um parágrafo, unindo o código inline que foi quebrado entre as linhas."""
    sem_espaco = re.compile(r'(\w-|/)$')  # palavra hifenizada ou URL quebrada no fim da linha
    if texto.endswith('`') and continuacao.startswith('`'):
        return texto[:-1] + ('' if sem_espaco.search(texto[:-1]) else ' ') + continuacao[1:]
    if sem_espaco.search(texto):
        return texto + continuacao
    return texto + ' ' + continuacao


def _elementos_texto(palavras: List[Dict]) -> List[Dict]:
    elementos: List[Dict] = []
    for linha in _agrupar_linhas(palavras):
        texto = _juntar(linha)
        if re.fullmatch(r'\.{5,}', texto):
            continue  # linha pontilhada sob o título do capítulo
        x0, top = linha[0]['x0'], linha[0]['top']
        nivel = _titulo(linha)
        ultimo = elementos[-1] if elementos else None
        if nivel:
            m = RE_TITULO.match(texto)
            if m:
                elementos.append({'tipo': 'titulo', 'top': top, 'ultimo_top': top, 'numero': m.group(1), 'texto': texto})
            elif ultimo and ultimo['tipo'] == 'titulo':
                # título longo quebrado em duas linhas
                ultimo['texto'] += ' ' + texto
                ultimo['ultimo_top'] = top
            else:
                elementos.append({'tipo': 'paragrafo', 'top': top, 'ultimo_top': top, 'x0': x0, 'texto': texto})
            continue
        item = texto.startswith('•') or (x0 > 78 and RE_ITEM_NUMERADO.match(texto))
        if item:
            texto = texto.lstrip('• ').strip()
            m = RE_ITEM_NUMERADO.match(texto)
            if m and not texto.startswith('•'):
                texto = f'{m.group(1)}. {m.group(2)}'
            elementos.append({'tipo': 'item', 'top': top, 'ultimo_top': top, 'x0': x0, 'texto': texto})
        elif (ultimo and ultimo['tipo'] in ('paragrafo', 'item') and x0 >= ultimo['x0'] - 1
              and (top - ultimo['ultimo_top'] <= ENTRELINHA_MAX
                   or (top - ultimo['ultimo_top'] <= ENTRELINHA_SIMBOLO and not re.search(r'[.:!?]$', ultimo['texto'])))):
            ultimo['texto'] = _emendar(ultimo['texto'], texto)
            ultimo['ultimo_top'] = top
        else:
            elementos.append({'tipo': 'paragrafo', 'top': top, 'ultimo_top': top, 'x0': x0, 'texto': texto})
    return elementos


def _numero_pagina(page) -> Optional[int]:
    """Número impresso no cabeçalho da página (difere do índice da página no PDF)."""
    topo = [w for w in page.extract_words() if w['top'] < TOPO_CONTEUDO]
    numeros = [w['text'] for w in sorted(topo, key=lambda w: w['x0']) if w['text'].isdigit()]
    return int(numeros[-1]) if numeros else None


def _elementos_pagina(page) -> List[Dict]:
    palavras = [w for w in page.extract_words(x_tolerance=1.5, extra_attrs=['fontname', 'size'])
                if TOPO_CONTEUDO < w['top'] < BASE_CONTEUDO]
    # blocos de código são recuados (x0 = 94); tabelas, inclusive as de uma coluna, começam na margem (x0 = 72)
    codigos = [r for r in page.rects if _cinza(r) and r['x0'] > 85 and r['x1'] - r['x0'] > 300]
    celulas = [r for r in page.rects if r not in codigos and r['bottom'] - r['top'] > 10]

    elementos: List[Dict] = []
    for r in codigos:
        dentro = [p for p in palavras if _no_codigo(p, r)]
        if dentro:
            elementos.append({'tipo': 'codigo', 'top': r['top'], 'texto': _bloco_codigo(dentro, r)})
    elementos.extend(_tabelas(celulas, palavras))
    soltas = [p for p in palavras
              if not any(_no_codigo(p, r) for r in codigos) and not any(_dentro(p, r) for r in celulas)]
    elementos.extend(_elementos_texto(soltas))

    pagina = _numero_pagina(page)
    for e in elementos:
        e['pagina'] = pagina
    return sorted(elementos, key=lambda e: e['top'])


def _continua(anterior: Dict, primeiro: Dict) -> bool:
    """Se o primeiro elemento da página continua o último da página anterior."""
    if anterior['tipo'] == primeiro['tipo'] == 'tabela':
        return primeiro['cabecalho'] is None and primeiro['x0'] == anterior['x0']
    if anterior['tipo'] == primeiro['tipo'] == 'codigo':
        return True
    if anterior['tipo'] in ('paragrafo', 'item') and primeiro['tipo'] == 'paragrafo':
        return not re.search(r'[.:;!?)]$', anterior['texto'])
    return False


def extrair_elementos(caminho_pdf: Path) -> List[Dict]:
    """Elementos do manual em ordem de leitura: titulo, paragrafo, item, codigo e tabela, com a página impressa."""
    elementos: List[Dict] = []
    with pdfplumber.open(caminho_pdf) as pdf:
        for page in pdf.pages:
            da_pagina = _elementos_pagina(page)
            if elementos and da_pagina and _continua(elementos[-1], da_pagina[0]):
                anterior, primeiro = elementos[-1], da_pagina.pop(0)
                if anterior['tipo'] == 'tabela':
                    anterior['linhas'].extend(_ajustar(l, anterior['n']) for l in primeiro['linhas'])
                elif anterior['tipo'] == 'codigo':
                    anterior['texto'] += '\n' + primeiro['texto']
                else:
                    anterior['texto'] = _emendar(anterior['texto'], primeiro['texto'])
                anterior.setdefault('paginas_extra', []).append(primeiro['pagina'])
            elementos.extend(da_pagina)
    # capa e índice vêm antes do primeiro título numerado e não fazem parte do conteúdo
    inicio = next(i for i, e in enumerate(elementos) if e['tipo'] == 'titulo')
    return elementos[inicio:]


def montar_secoes(elementos: List[Dict]) -> List[Dict]:
    secoes: List[Dict] = []
    caminho: Dict[int, str] = {}
    for e in elementos:
        if e['tipo'] == 'titulo':
            nivel = e['numero'].count('.') + 1
            caminho = {n: t for n, t in caminho.items() if n < nivel}
            caminho[nivel] = e['texto']
            secoes.append({'numero': e['numero'], 'titulo': e['texto'], 'caminho': [caminho[n] for n in sorted(caminho)],
                           'pagina': e['pagina'], 'elementos': []})
        else:
            secoes[-1]['elementos'].append(e)
    return secoes


def _celula(texto: str) -> str:
    return texto.replace('|', '\\|')


def _tabela_md(cabecalho: List[str]) -> str:
    return '| ' + ' | '.join(map(_celula, cabecalho)) + ' |\n|' + '---|' * len(cabecalho)


def _pecas(secao: Dict) -> List[Dict]:
    """Unidades que nunca são quebradas: parágrafo, item, bloco de código (com a frase que o introduz) e linha de tabela."""
    pecas: List[Dict] = []
    for n, e in enumerate(secao['elementos']):
        paginas = [e['pagina']] + e.get('paginas_extra', [])
        if e['tipo'] == 'tabela':
            cabecalho = e['cabecalho'] or [''] * e['n']
            for linha in e['linhas']:
                pecas.append({'texto': '| ' + ' | '.join(map(_celula, linha)) + ' |', 'tabela': (secao['numero'], n),
                              'cabecalho': _tabela_md(cabecalho), 'paginas': paginas})
            continue
        if e['tipo'] == 'codigo':
            texto = f'```gobr\n{e["texto"]}\n```'
            if pecas and pecas[-1].get('tabela') is None and pecas[-1]['texto'].endswith(':'):
                pecas[-1]['texto'] += '\n' + texto
                pecas[-1]['paginas'] += paginas
                continue
        else:
            numerado = RE_ITEM_NUMERADO.match(e['texto'])
            texto = ('- ' if e['tipo'] == 'item' and not numerado else '') + e['texto']
        pecas.append({'texto': texto, 'tabela': None, 'paginas': paginas})
    return pecas


def gerar_chunks(secoes: List[Dict], contar_tokens: Callable[[str], int], max_tokens: int) -> List[Dict]:
    """Um chunk por seção; seções longas são divididas entre peças, repetindo o caminho de títulos e o cabeçalho da tabela."""
    chunks: List[Dict] = []
    for secao in secoes:
        pecas = _pecas(secao)
        if not pecas:
            continue  # título sem texto próprio (o conteúdo está nas subseções)
        topo = 'Manual GoBR > ' + ' > '.join(secao['caminho'])
        grupos: List[List[Dict]] = [[]]
        for peca in pecas:
            atual = grupos[-1]
            candidato = _render(topo, atual + [peca])
            if atual and contar_tokens(candidato) > max_tokens:
                grupos.append([peca])
            else:
                atual.append(peca)
        for parte, grupo in enumerate(grupos, 1):
            paginas = sorted({p for peca in grupo for p in peca['paginas'] if p is not None})
            chunks.append({
                'id': f'manual_{secao["numero"]}' + (f'_p{parte}' if len(grupos) > 1 else ''),
                'secao': secao['numero'],
                'titulo': secao['titulo'],
                'caminho': secao['caminho'],
                'paginas': paginas,
                'parte': f'{parte}/{len(grupos)}',
                'texto': _render(topo, grupo),
            })
    return chunks


def _render(topo: str, pecas: List[Dict]) -> str:
    blocos: List[str] = [topo]
    tabela_atual = None
    for peca in pecas:
        if peca['tabela'] is not None and peca['tabela'] == tabela_atual:
            blocos[-1] += '\n' + peca['texto']
        elif peca['tabela'] is not None:
            blocos.append(peca['cabecalho'] + '\n' + peca['texto'])
        else:
            blocos.append(peca['texto'])
        tabela_atual = peca['tabela']
    return '\n\n'.join(blocos)


def manual_markdown(secoes: List[Dict]) -> str:
    """Manual inteiro em Markdown, para conferir a extração."""
    saida: List[str] = []
    for secao in secoes:
        saida.append('#' * min(len(secao['caminho']), 4) + f' {secao["titulo"]}  (p. {secao["pagina"]})')
        if secao['elementos']:
            saida.append(_render('', _pecas(secao)).lstrip('\n'))
    return '\n\n'.join(saida) + '\n'


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='Extrai o manual GoBR (PDF) em Markdown estruturado, para conferência.')
    ap.add_argument('pdf', type=Path, help='Caminho do govendas-rules.pdf')
    ap.add_argument('--md', type=Path, default=Path('index/manual/manual_extraido.md'))
    args = ap.parse_args()
    secoes = montar_secoes(extrair_elementos(args.pdf))
    args.md.parent.mkdir(parents=True, exist_ok=True)
    args.md.write_text(manual_markdown(secoes), encoding='utf-8', newline='\n')
    print(f'{len(secoes)} seções extraídas em {args.md}')
