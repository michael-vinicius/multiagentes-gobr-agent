from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import numpy as np
from fastembed import TextEmbedding


class IndiceManual:
    """Busca semântica sobre o índice do manual gerado por indexar_manual.py."""

    def __init__(self, dir_indice: Path):
        self.manifesto = json.loads((dir_indice / 'manifesto.json').read_text(encoding='utf-8'))
        self.vetores = np.load(dir_indice / 'embeddings.npy')
        with (dir_indice / 'chunks.jsonl').open(encoding='utf-8') as f:
            self.chunks = [json.loads(l) for l in f if l.strip()]
        if len(self.chunks) != len(self.vetores):
            raise ValueError('chunks e embeddings com tamanhos diferentes; gere o índice novamente')
        self.embedder = TextEmbedding(model_name=self.manifesto['modelo'])

    def buscar(self, consulta: str, k: int = 5) -> List[Dict]:
        q = np.array(next(iter(self.embedder.embed([self.manifesto['prefixo_consulta'] + consulta]))), dtype=np.float32)
        q /= np.linalg.norm(q)
        scores = self.vetores @ q
        return [{**self.chunks[i], 'score': round(float(scores[i]), 4)} for i in np.argsort(-scores)[:k]]


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='Busca trechos do manual GoBR relacionados a uma pergunta ou descrição.')
    ap.add_argument('consulta', help='Pergunta ou descrição em linguagem natural')
    ap.add_argument('-k', type=int, default=3)
    ap.add_argument('--indice', type=Path, default=Path('index/manual'))
    ap.add_argument('--json', action='store_true', help='Imprime o resultado em JSON')
    ap.add_argument('--resumo', action='store_true', help='Mostra só a seção de cada resultado, sem o texto')
    args = ap.parse_args()

    resultados = IndiceManual(args.indice).buscar(args.consulta, args.k)
    if args.json:
        print(json.dumps(resultados, ensure_ascii=False, indent=2))
    else:
        for n, r in enumerate(resultados, 1):
            parte = f' (parte {r["parte"]})' if r['parte'] != '1/1' else ''
            print(f'{n}. [{r["score"]:.3f}] {r["titulo"]}{parte} — p. {", ".join(map(str, r["paginas"]))}')
            if not args.resumo:
                # a primeira linha do chunk é o caminho de títulos, já mostrado acima
                for linha in r['texto'].split('\n\n', 1)[-1].splitlines():
                    print(f'   {linha}')
                print()
