"""Pedidos ao modelo com resposta em JSON (saída estruturada), usando os backends da etapa 4.

- Ollama: o JSON Schema vai no campo `format` e o próprio servidor restringe a geração a ele;
- Claude (opcional, pago): o schema vai no prompt e a resposta é lida como JSON.

Em ambos a resposta é conferida contra os campos obrigatórios do schema antes de ser usada.
"""
from __future__ import annotations

import json
import re
import urllib.error
from typing import Any, Dict, List

from memoria import registrar_uso
from rag import BackendOllama, ErroGeracao


def _extrair_json(texto: str) -> Any:
    texto = texto.strip()
    m = re.search(r'```(?:json)?\s*(.*?)```', texto, re.S)
    if m:
        texto = m.group(1)
    inicio = min([i for i in (texto.find('{'), texto.find('[')) if i >= 0], default=-1)
    if inicio < 0:
        raise ErroGeracao('o modelo não devolveu JSON')
    try:
        return json.JSONDecoder().raw_decode(texto[inicio:])[0]
    except json.JSONDecodeError as e:
        raise ErroGeracao(f'JSON inválido na resposta do modelo: {e}') from e


def _conferir(valor: Any, schema: Dict, caminho: str = '$') -> List[str]:
    """Conferência mínima (tipos e obrigatórios) para não depender de biblioteca de validação."""
    tipos = schema.get('type')
    tipos = tipos if isinstance(tipos, list) else [tipos] if tipos else []
    mapa = {'object': dict, 'array': list, 'string': str, 'integer': int, 'boolean': bool, 'null': type(None),
            'number': (int, float)}
    if tipos and not any(isinstance(valor, mapa[t]) and not (t == 'integer' and isinstance(valor, bool))
                         for t in tipos):
        return [f'{caminho}: esperado {"/".join(tipos)}, veio {type(valor).__name__}']
    erros = []
    if 'enum' in schema and valor not in schema['enum']:
        erros.append(f'{caminho}: valor {valor!r} fora de {schema["enum"]}')
    if isinstance(valor, dict):
        for k in schema.get('required', []):
            if k not in valor:
                erros.append(f'{caminho}: falta o campo "{k}"')
        for k, sub in schema.get('properties', {}).items():
            if k in valor:
                erros += _conferir(valor[k], sub, f'{caminho}.{k}')
    if isinstance(valor, list) and 'items' in schema:
        for i, v in enumerate(valor):
            erros += _conferir(v, schema['items'], f'{caminho}[{i}]')
    return erros


def pedir_json(backend: Any, system: str, usuario: str, schema: Dict, tentativas: int = 2) -> Any:
    """Pede ao modelo uma resposta no formato do `schema`; repete uma vez se vier fora do formato."""
    ultimo = ''
    for _ in range(tentativas):
        try:
            if isinstance(backend, BackendOllama):
                payload = {
                    'model': backend.modelo,
                    'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': usuario}],
                    'stream': False, 'format': schema,
                    'options': {'num_ctx': backend.num_ctx, 'num_predict': backend.max_tokens, 'temperature': 0},
                }
                r = backend.transporte(f'{backend.url}/api/chat', payload, backend.timeout)
                registrar_uso(backend, r.get('prompt_eval_count', 0), r.get('eval_count', 0))
                if r.get('prompt_eval_count', 0) + r.get('eval_count', 0) >= backend.num_ctx:
                    raise ErroGeracao(f'o prompt não coube na janela num_ctx={backend.num_ctx}')
                if r.get('done_reason') == 'length':
                    raise ErroGeracao('resposta JSON truncada')
                texto = (r.get('message') or {}).get('content', '')
            else:
                instrucao = (f'{system}\n\nResponda somente com um objeto JSON válido neste JSON Schema, '
                             f'sem texto fora dele:\n{json.dumps(schema, ensure_ascii=False)}')
                texto = backend.completar(instrucao, [{'role': 'user', 'content': usuario}]).texto
            valor = _extrair_json(texto)
            erros = _conferir(valor, schema)
            if not erros:
                return valor
            ultimo = '; '.join(erros[:5])
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            raise ErroGeracao(f'sem conexão com o modelo ({e})') from e
        except ErroGeracao as e:
            ultimo = str(e)
    raise ErroGeracao(f'o modelo não devolveu o JSON esperado: {ultimo}')
