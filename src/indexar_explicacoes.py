from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import numpy as np
from fastembed import TextEmbedding

MODELO_PADRAO = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
CAMPOS_METADADOS = ('id', 'arquivo', 'ordem_no_arquivo', 'nome_regra', 'status_validacao')


def carregar_registros(caminho: Path) -> List[Dict]:
    with caminho.open(encoding='utf-8') as f:
        return [json.loads(linha) for linha in f if linha.strip()]


def validar_registros(registros: List[Dict]) -> None:
    """Falha cedo se houver ids duplicados ou textos vazios, para não gerar um índice silenciosamente incompleto."""
    vistos = set()
    for r in registros:
        if r['id'] in vistos:
            raise ValueError(f'id duplicado: {r["id"]}')
        vistos.add(r['id'])
        if not r.get('texto', '').strip():
            raise ValueError(f'texto vazio: {r["id"]}')


def sha256_arquivo(caminho: Path) -> str:
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def indexar(entrada: Path, saida: Path, modelo: str, batch_size: int) -> Dict:
    registros = carregar_registros(entrada)
    validar_registros(registros)

    embedder = TextEmbedding(model_name=modelo)
    vetores = np.array(list(embedder.embed([r['texto'] for r in registros], batch_size=batch_size)), dtype=np.float32)
    # normaliza para que o produto escalar seja a similaridade de cosseno
    vetores /= np.linalg.norm(vetores, axis=1, keepdims=True)

    saida.mkdir(parents=True, exist_ok=True)
    np.save(saida / 'embeddings.npy', vetores)
    with (saida / 'metadados.jsonl').open('w', encoding='utf-8') as w:
        for r in registros:
            w.write(json.dumps({k: r[k] for k in CAMPOS_METADADOS}, ensure_ascii=False) + '\n')

    manifesto = {
        'modelo': modelo,
        'dimensao': int(vetores.shape[1]),
        'total_vetores': int(vetores.shape[0]),
        'metrica': 'cosseno (vetores normalizados, produto escalar)',
        'campo_indexado': 'texto',
        'fonte': entrada.as_posix(),
        'fonte_sha256': sha256_arquivo(entrada),
        'gerado_em': datetime.now(timezone.utc).isoformat(timespec='seconds'),
    }
    (saida / 'manifesto.json').write_text(json.dumps(manifesto, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return manifesto


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='Gera o índice vetorial das explicações de parametrizações GoBR.')
    ap.add_argument('--entrada', type=Path, default=Path('data/parametrizacoes_para_embeddings.jsonl'))
    ap.add_argument('--saida', type=Path, default=Path('index'))
    ap.add_argument('--modelo', default=MODELO_PADRAO, help='Modelo de embeddings suportado pelo fastembed')
    ap.add_argument('--batch-size', type=int, default=64)
    args = ap.parse_args()
    m = indexar(args.entrada, args.saida, args.modelo, args.batch_size)
    print(f'Indexados {m["total_vetores"]} textos com {m["modelo"]} (dimensão {m["dimensao"]}) em {args.saida}/.')
