from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import numpy as np
from fastembed import TextEmbedding


class IndiceExplicacoes:
    """Busca semântica sobre o índice gerado por indexar_explicacoes.py."""

    def __init__(self, dir_indice: Path, explicadas: Path):
        self.manifesto = json.loads((dir_indice / 'manifesto.json').read_text(encoding='utf-8'))
        self.vetores = np.load(dir_indice / 'embeddings.npy')
        with (dir_indice / 'metadados.jsonl').open(encoding='utf-8') as f:
            self.metadados = [json.loads(l) for l in f if l.strip()]
        if len(self.metadados) != len(self.vetores):
            raise ValueError('metadados e embeddings com tamanhos diferentes; gere o índice novamente')
        with explicadas.open(encoding='utf-8') as f:
            self.completos = {r['id']: r for r in map(json.loads, f) if r}
        self.posicao = {(m['arquivo'], m['ordem_no_arquivo']): i for i, m in enumerate(self.metadados)}
        self.embedder = TextEmbedding(model_name=self.manifesto['modelo'])

    def buscar(self, consulta: str, k: int = 5, contexto: int = 0) -> List[Dict]:
        q = np.array(next(iter(self.embedder.embed([consulta]))), dtype=np.float32)
        q /= np.linalg.norm(q)
        scores = self.vetores @ q
        melhores = np.argsort(-scores)[:k]
        resultados = []
        for i in melhores:
            meta = self.metadados[i]
            res = {**meta, 'score': round(float(scores[i]), 4), **self._detalhes(meta['id'])}
            if contexto:
                # a ordem dos blocos importa no GoBR: regras anteriores capturam clientes antes das seguintes
                res['vizinhos'] = self._vizinhos(meta['arquivo'], meta['ordem_no_arquivo'], contexto)
            resultados.append(res)
        return resultados

    def _detalhes(self, id_: str) -> Dict:
        r = self.completos.get(id_, {})
        return {'explicacao_detalhada': r.get('explicacao_detalhada'), 'dsl_original': r.get('dsl_original')}

    def _vizinhos(self, arquivo: str, ordem: int, n: int) -> List[Dict]:
        out = []
        for o in range(ordem - n, ordem + n + 1):
            i = self.posicao.get((arquivo, o))
            if o != ordem and i is not None:
                m = self.metadados[i]
                out.append({'id': m['id'], 'ordem_no_arquivo': o, 'nome_regra': m['nome_regra']})
        return out


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='Busca parametrizações GoBR semanticamente próximas de uma descrição.')
    ap.add_argument('consulta', help='Descrição da regra de negócio em linguagem natural')
    ap.add_argument('-k', type=int, default=5)
    ap.add_argument('--contexto', type=int, default=0, help='Quantos blocos vizinhos do mesmo arquivo exibir')
    ap.add_argument('--indice', type=Path, default=Path('index'))
    ap.add_argument('--explicadas', type=Path, default=Path('data/parametrizacoes_explicadas.jsonl'))
    ap.add_argument('--json', action='store_true', help='Imprime o resultado em JSON')
    args = ap.parse_args()

    resultados = IndiceExplicacoes(args.indice, args.explicadas).buscar(args.consulta, args.k, args.contexto)
    if args.json:
        print(json.dumps(resultados, ensure_ascii=False, indent=2))
    else:
        for n, r in enumerate(resultados, 1):
            print(f'{n}. [{r["score"]:.3f}] {r["id"]} — {r["nome_regra"]}')
            print(f'   {r["explicacao_detalhada"]}')
            for linha in (r['dsl_original'] or '').splitlines():
                print(f'   | {linha}')
            for v in r.get('vizinhos', []):
                print(f'   ↳ vizinho #{v["ordem_no_arquivo"]}: {v["nome_regra"]}')
            print()
