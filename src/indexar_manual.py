from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, List

import numpy as np
from fastembed import TextEmbedding
from tokenizers import Tokenizer

from extrair_manual import extrair_elementos, gerar_chunks, manual_markdown, montar_secoes
from indexar_explicacoes import sha256_arquivo

MODELO_PADRAO = 'intfloat/multilingual-e5-large'
# seções só são divididas quando não cabem na janela de 512 tokens do modelo (com margem)
MAX_TOKENS_PADRAO = 500
# os modelos e5 foram treinados com prefixos que distinguem consulta e documento
PREFIXOS = {'intfloat/multilingual-e5-large': ('query: ', 'passage: ')}
CAMPOS_CHUNK = ('id', 'secao', 'titulo', 'caminho', 'paginas', 'parte', 'tokens', 'texto')


def contador_tokens(embedder: TextEmbedding) -> Callable[[str], int]:
    """Conta tokens com o tokenizador do próprio modelo, sem o truncamento que o fastembed aplica."""
    tok = Tokenizer.from_str(embedder.model.tokenizer.to_str())
    tok.no_truncation()
    tok.no_padding()
    return lambda texto: len(tok.encode(texto).ids)


def limite_tokens(embedder: TextEmbedding) -> int:
    """Tamanho a partir do qual o fastembed trunca a entrada do modelo."""
    return embedder.model.tokenizer.truncation['max_length']


def validar_chunks(chunks: List[Dict], limite: int) -> None:
    """Falha cedo se algum chunk seria truncado pelo modelo, o que tiraria parte dele da busca sem aviso."""
    ids = [c['id'] for c in chunks]
    if len(ids) != len(set(ids)):
        raise ValueError('ids de chunk duplicados')
    grandes = [f'{c["id"]} ({c["tokens"]} tokens)' for c in chunks if c['tokens'] > limite]
    if grandes:
        raise ValueError(f'chunks acima do limite de {limite} tokens do modelo: {", ".join(grandes)}')


def indexar(pdf: Path, saida: Path, modelo: str, max_tokens: int, batch_size: int) -> Dict:
    embedder = TextEmbedding(model_name=modelo)
    contar = contador_tokens(embedder)
    _, prefixo_documento = PREFIXOS.get(modelo, ('', ''))

    secoes = montar_secoes(extrair_elementos(pdf))
    chunks = gerar_chunks(secoes, lambda t: contar(prefixo_documento + t), max_tokens)
    for c in chunks:
        c['tokens'] = contar(prefixo_documento + c['texto'])
    limite = limite_tokens(embedder)
    validar_chunks(chunks, limite)

    textos = [prefixo_documento + c['texto'] for c in chunks]
    vetores = np.array(list(embedder.embed(textos, batch_size=batch_size)), dtype=np.float32)
    # normaliza para que o produto escalar seja a similaridade de cosseno
    vetores /= np.linalg.norm(vetores, axis=1, keepdims=True)

    saida.mkdir(parents=True, exist_ok=True)
    np.save(saida / 'embeddings.npy', vetores)
    with (saida / 'chunks.jsonl').open('w', encoding='utf-8', newline='\n') as w:
        for c in chunks:
            w.write(json.dumps({k: c[k] for k in CAMPOS_CHUNK}, ensure_ascii=False) + '\n')
    (saida / 'manual_extraido.md').write_text(manual_markdown(secoes), encoding='utf-8', newline='\n')

    tokens = sorted(c['tokens'] for c in chunks)
    manifesto = {
        'modelo': modelo,
        'dimensao': int(vetores.shape[1]),
        'total_vetores': int(vetores.shape[0]),
        'metrica': 'cosseno (vetores normalizados, produto escalar)',
        'prefixo_consulta': PREFIXOS.get(modelo, ('', ''))[0],
        'prefixo_documento': prefixo_documento,
        'limite_tokens_modelo': limite,
        'max_tokens_chunk': max_tokens,
        'tokens_por_chunk': {'min': tokens[0], 'mediana': tokens[len(tokens) // 2], 'max': tokens[-1]},
        'secoes': len(secoes),
        'fonte': pdf.name,
        'fonte_sha256': sha256_arquivo(pdf),
        'gerado_em': datetime.now(timezone.utc).isoformat(timespec='seconds'),
    }
    (saida / 'manifesto.json').write_text(json.dumps(manifesto, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    return manifesto


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='Gera o índice vetorial do manual GoBR a partir do PDF.')
    ap.add_argument('pdf', type=Path, help='Caminho do govendas-rules.pdf')
    ap.add_argument('--saida', type=Path, default=Path('index/manual'))
    ap.add_argument('--modelo', default=MODELO_PADRAO, help='Modelo de embeddings suportado pelo fastembed')
    ap.add_argument('--max-tokens', type=int, default=MAX_TOKENS_PADRAO, help='Tamanho máximo de cada chunk, em tokens do modelo')
    ap.add_argument('--batch-size', type=int, default=16)
    args = ap.parse_args()
    m = indexar(args.pdf, args.saida, args.modelo, args.max_tokens, args.batch_size)
    t = m['tokens_por_chunk']
    print(f'Indexados {m["total_vetores"]} chunks de {m["secoes"]} seções com {m["modelo"]} (dimensão {m["dimensao"]}) em {args.saida}/.')
    print(f'Tokens por chunk: mín. {t["min"]}, mediana {t["mediana"]}, máx. {t["max"]} (limite do modelo: {m["limite_tokens_modelo"]}).')
