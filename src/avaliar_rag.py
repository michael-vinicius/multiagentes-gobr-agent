"""Avaliação ponta a ponta do RAG: recuperação + geração (Ollama ou Claude) + pós-checagens.

Cada caso traz as cláusulas que a regra gerada precisa ter. Cada cláusula é um grupo de alternativas
equivalentes, todas com sintaxe documentada no manual ou usada nas regras reais (por exemplo `quinzenal()` e
`frequencia de 15 dias`). A conferência é por substring, sem acentos, sem diferença de maiúsculas e ignorando o
texto entre aspas, para que um filtro usado como nome (`da carteira("curva A com a empresa")`) não conte.
Ela mede se o modelo usou a sintaxe certa, não se a regra inteira é a única resposta possível.

A mesma conferência é feita no contexto enviado ao modelo (exemplos + trechos do manual). Isso separa as falhas
de busca (a cláusula nem chegou ao modelo) das falhas de geração (chegou, mas o modelo não usou).
"""
from __future__ import annotations

import json
import re
import time
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from gerar_explicacoes_gobr import canon
from rag import (BACKENDS, ESFORCO_PADRAO, Contexto, ErroGeracao, Gerador, Recuperador, carregar_recuperador,
                 criar_backend)

Clausula = Tuple[str, ...]

CASOS: List[Tuple[str, List[Clausula]]] = [
    ('Para o time de televendas, não agendar os clientes que são filiais',
     [('do time',), ('cliente filial',), ('nao agendar',)]),
    ('Clientes da carteira fixa sem compra há mais de 90 dias devem ser atendidos a cada 14 dias',
     [('da carteira',),
      ('inatividade de 90 dias', 'inatividade global de 90 dias', 'fora da recencia de positivacao do vendedor em 90 dias'),
      ('frequencia de 14 dias',)]),
    ('Os televendas não podem ligar para o cliente no mesmo dia em que o vendedor de campo visita',
     [('sem choque',)]),
    ('Clientes da curva A com a empresa devem ter preferência de visita na segunda e na terça',
     [('curva a com a empresa',), ('preferencia na segunda e na terca',)]),
    ('Clientes inadimplentes não devem ser agendados', [('inadimplentes',), ('nao agendar',)]),
    ('Clientes inativos da carteira de campo recebem visita quinzenal',
     [('da carteira',), ('inativos para o vendedor', 'inativos para a empresa'),
      ('frequencia quinzenal()', 'frequencia de 15 dias')]),
]


def _norm(s: str) -> str:
    return re.sub(r'\s+', ' ', canon(s))


def _sem_aspas(dsl: str) -> str:
    return re.sub(r'"[^"\n]*"', '""', dsl)


def faltando(texto: str, clausulas: Sequence[Clausula]) -> List[str]:
    """Grupos de cláusulas sem nenhuma alternativa presente no texto (cada grupo é identificado pela 1ª forma)."""
    t = _norm(texto)
    return [g[0] for g in clausulas if not any(_norm(alt) in t for alt in g)]


def _texto_contexto(ctx: Contexto) -> str:
    return '\n'.join([e.dsl for e in ctx.exemplos] + [t.texto for t in ctx.trechos])


def avaliar_caso(recuperador: Recuperador, gerador: Gerador, pergunta: str, clausulas: Sequence[Clausula],
                 k_exemplos: int, k_manual: int) -> Dict:
    ctx = recuperador.recuperar(pergunta, k_exemplos, k_manual)
    fora_do_contexto = faltando(_texto_contexto(ctx), clausulas)
    r = {'pergunta': pergunta, 'secoes_recuperadas': [t.secao for t in ctx.trechos],
         'exemplos_recuperados': [e.id for e in ctx.exemplos],
         'fora_do_contexto': fora_do_contexto, 'contexto_cobre': not fora_do_contexto}
    try:
        resp = gerador.gerar(ctx)
    except ErroGeracao as e:
        return {**r, 'erro': str(e), 'aprovado': False}
    ausentes = faltando(_sem_aspas('\n'.join(resp.blocos_gobr)), clausulas)
    r.update({
        'tem_dsl': bool(resp.blocos_gobr),
        'dsl_valida': resp.dsl_valida,
        'citou_fontes': bool(resp.citacoes),
        'citacoes_invalidas': resp.citacoes_invalidas,
        'clausulas_faltando': ausentes,
        'resposta': asdict(resp),
    })
    r['aprovado'] = (r['tem_dsl'] and r['dsl_valida'] and r['citou_fontes'] and not r['citacoes_invalidas']
                     and not ausentes)
    return r


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser(description='Avalia o RAG ponta a ponta (recuperação + geração + pós-checagens).')
    ap.add_argument('-k', '--k-exemplos', type=int, default=5)
    ap.add_argument('--k-manual', type=int, default=4)
    ap.add_argument('--backend', default='ollama', choices=BACKENDS)
    ap.add_argument('--modelo', help='Padrão do backend escolhido')
    ap.add_argument('--esforco', default=ESFORCO_PADRAO, choices=['low', 'medium', 'high', 'xhigh', 'max'])
    ap.add_argument('--saida', type=Path, help='Grava os resultados completos (com as respostas) em JSON')
    ap.add_argument('--so-busca', action='store_true',
                    help='Mede só a cobertura do contexto recuperado, sem chamar o modelo de linguagem')
    args = ap.parse_args()

    recuperador = carregar_recuperador()
    if args.so_busca:
        cobertos = 0
        for pergunta, clausulas in CASOS:
            ctx = recuperador.recuperar(pergunta, args.k_exemplos, args.k_manual)
            fora = faltando(_texto_contexto(ctx), clausulas)
            cobertos += not fora
            print(f'[{"✓" if not fora else "✗"}] {pergunta}' + (f'  · fora do contexto: {fora}' if fora else ''))
        print(f'\ncontexto cobre todas as cláusulas: {cobertos}/{len(CASOS)} '
              f'(k_exemplos={args.k_exemplos}, k_manual={args.k_manual})')
        return

    gerador = Gerador(criar_backend(args.backend, args.modelo, args.esforco))
    resultados, entrada, saida = [], 0, 0
    for pergunta, clausulas in CASOS:
        inicio = time.perf_counter()
        r = avaliar_caso(recuperador, gerador, pergunta, clausulas, args.k_exemplos, args.k_manual)
        r['segundos'] = round(time.perf_counter() - inicio, 1)
        resultados.append(r)
        uso = r.get('resposta', {}).get('uso', {})
        entrada += uso.get('input_tokens', 0)
        saida += uso.get('output_tokens', 0)
        if 'erro' in r:
            print(f'[ERRO ] {pergunta}\n        {r["erro"]}')
            continue
        marca = 'OK   ' if r['aprovado'] else 'FALHA'
        print(f'[{marca}] {pergunta}  ({r["segundos"]} s)')
        print(f'        contexto {"✓" if r["contexto_cobre"] else "✗ " + str(r["fora_do_contexto"])} · '
              f'dsl {"✓" if r["dsl_valida"] else "✗"} · citações {r["resposta"]["citacoes"]}'
              + (f' · inválidas {r["citacoes_invalidas"]}' if r['citacoes_invalidas'] else '')
              + (f' · faltando na regra {r["clausulas_faltando"]}' if r['clausulas_faltando'] else ''))

    n = len(CASOS)
    soma = lambda chave: sum(bool(r.get(chave)) for r in resultados)
    modelo = next((r['resposta']['modelo'] for r in resultados if 'resposta' in r), args.modelo or args.backend)
    clausulas_ok = sum('clausulas_faltando' in r and not r['clausulas_faltando'] for r in resultados)
    print(f'\nmodelo: {modelo} · aprovados: {soma("aprovado")}/{n} · contexto cobre: {soma("contexto_cobre")}/{n} · '
          f'cláusulas certas: {clausulas_ok}/{n} · DSL válida: {soma("dsl_valida")}/{n} · '
          f'citou fontes: {soma("citou_fontes")}/{n} · tokens: {entrada} de entrada, {saida} de saída')
    if args.saida:
        args.saida.write_text(json.dumps(resultados, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
