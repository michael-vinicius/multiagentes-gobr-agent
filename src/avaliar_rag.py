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

from catalogo_gobr import carregar_catalogo
from gerar_explicacoes_gobr import canon
from rag import (BACKENDS, ESFORCO_PADRAO, Contexto, ErroGeracao, Gerador, Recuperador, carregar_recuperador,
                 criar_backend, validar_dsl)

Clausula = Tuple[str, ...]

# Conjunto de AJUSTE: usado para diagnosticar e calibrar o fluxo (prompt, busca, validação).
CASOS_AJUSTE: List[Tuple[str, List[Clausula]]] = [
    ('Para o time de televendas, não agendar os clientes que são filiais',
     [('do time',), ('cliente filial',), ('nao agendar',)]),
    ('Clientes da carteira fixa sem compra há mais de 90 dias devem ser atendidos a cada 14 dias',
     [('da carteira',),
      ('inatividade de 90 dias', 'inatividade global de 90 dias', 'fora da recencia de positivacao em 90 dias',
       'fora da recencia de positivacao do vendedor em 90 dias', 'fora da recencia de positivacao global em 90 dias'),
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

# Conjunto de TESTE: escrito antes das melhorias e nunca usado para ajustá-las; mede a generalização.
# Toda alternativa aceita aparece nas regras reais ou nas tabelas do manual (verificado em test_avaliar_rag.py).
CASOS_TESTE: List[Tuple[str, List[Clausula]]] = [
    ('Clientes ativos para o vendedor devem ser visitados a cada 21 dias',
     [('ativos para o vendedor',), ('frequencia de 21 dias',)]),
    ('Clientes sem venda devem ser atendidos semanalmente',
     [('sem venda', 'sem vendas'), ('frequencia semanal()', 'frequencia de 7 dias')]),
    ('Clientes inativos para o vendedor e inadimplentes não devem ser agendados',
     [('inativos para o vendedor',), ('inadimplentes',), ('nao agendar',)]),
    ('Clientes prospect da empresa recebem visita mensal',
     # `prospects da empresa` (tabela 6.1 do manual) acrescentada na auditoria do gabarito contra o manual
     [('no ciclo de vida prospect com a empresa', 'prospects da empresa'),
      ('frequencia mensal()', 'frequencia de 30 dias')]),
    ('Não agendar clientes com situação baixada na Receita Federal',
     [('status na receita federal definido como baixada',), ('nao agendar',)]),
    ('Clientes adimplentes devem ser atendidos a cada 15 dias, de preferência nos dias úteis',
     [('adimplentes',), ('frequencia de 15 dias', 'frequencia quinzenal()'), ('preferencia nos dias uteis',)]),
    ('Clientes pessoa jurídica com a última compra entre 30 e 60 dias atrás devem ser atendidos a cada 10 dias',
     # "do vendedor" e "global" foram acrescentadas depois da 1ª rodada do sistema melhorado, que usou
     # `recencia de positivacao do vendedor entre 30 dias e 60 dias` (forma de 22 regras reais); o caso equivalente
     # do ajuste já aceitava essas variantes. O relatório traz os números com e sem esta correção.
     [('pessoa juridica',), ('recencia de positivacao entre 30 dias e 60 dias',
                             'recencia de positivacao do vendedor entre 30 dias e 60 dias',
                             'recencia de positivacao global entre 30 dias e 60 dias'), ('frequencia de 10 dias',)]),
    ('Clientes que fizeram uma única compra com o vendedor devem ter frequência de 14 dias',
     [('unica compra com o vendedor',), ('frequencia de 14 dias',)]),
    ('Clientes bloqueados não devem entrar na agenda', [('bloqueados',), ('nao agendar',)]),
    ('Clientes do ramo de atividade FARMACIA devem ter preferência de visita na terça',
     [('ramo de atividade igual',), ('preferencia na terca',)]),
    ('Para os clientes do televendas, evitar choque de agendamento com o time de campo',
     [('sem choque',)]),
]

CONJUNTOS = {'ajuste': CASOS_AJUSTE, 'teste': CASOS_TESTE}
CASOS = CASOS_AJUSTE + CASOS_TESTE


def _norm(s: str) -> str:
    return re.sub(r'\s+', ' ', canon(s))


def _sem_aspas(dsl: str) -> str:
    return re.sub(r'"[^"\n]*"', '""', dsl)


def _contem(texto_norm: str, alternativa: str) -> bool:
    # palavra inteira: "adimplentes" não pode casar dentro de "inadimplentes"
    return re.search(r'(?<!\w)' + re.escape(_norm(alternativa)) + r'(?!\w)', texto_norm) is not None


def faltando(texto: str, clausulas: Sequence[Clausula], forma: bool = False) -> List[str]:
    """Grupos de cláusulas sem nenhuma alternativa presente no texto (cada grupo é identificado pela 1ª forma).

    Com `forma=True` os números (e o marcador `<<N>>` do manual) viram `#` dos dois lados: o que se procura é a
    forma da cláusula (`frequencia de # dias`), porque o valor vem do pedido do usuário, não do contexto.
    """
    def f(s: str) -> str:
        s = _norm(s)
        return re.sub(r'\d+', '#', s.replace('<<n>>', '#')) if forma else s
    t = f(texto)
    return [g[0] for g in clausulas if not any(_contem(t, f(alt)) for alt in g)]


def _texto_contexto(ctx: Contexto) -> str:
    return '\n'.join([e.dsl for e in ctx.exemplos] + [t.texto for t in ctx.trechos])


def avaliar_caso(recuperador: Recuperador, gerador: Gerador, pergunta: str, clausulas: Sequence[Clausula],
                 k_exemplos: int, k_manual: int) -> Dict:
    ctx = recuperador.recuperar(pergunta, k_exemplos, k_manual)
    fora_do_contexto = faltando(_texto_contexto(ctx), clausulas, forma=True)
    r = {'pergunta': pergunta, 'secoes_recuperadas': [t.secao for t in ctx.trechos],
         'exemplos_recuperados': [e.id for e in ctx.exemplos],
         'fora_do_contexto': fora_do_contexto, 'contexto_cobre': not fora_do_contexto}
    try:
        resp = gerador.gerar(ctx)
    except ErroGeracao as e:
        return {**r, 'erro': str(e), 'aprovado': False}
    return _pontuar(r, asdict(resp), clausulas)


def _pontuar(r: Dict, resp: Dict, clausulas: Sequence[Clausula]) -> Dict:
    ausentes = faltando(_sem_aspas('\n'.join(resp['blocos_gobr'])), clausulas)
    r.update({
        'tem_dsl': bool(resp['blocos_gobr']),
        'dsl_valida': bool(resp['validacao']) and all(v['status'] == 'ok' for v in resp['validacao']),
        'citou_fontes': bool(resp['citacoes']),
        'citacoes_invalidas': resp['citacoes_invalidas'],
        'clausulas_faltando': ausentes,
        'resposta': resp,
    })
    r['aprovado'] = (r['tem_dsl'] and r['dsl_valida'] and r['citou_fontes'] and not r['citacoes_invalidas']
                     and not ausentes)
    return r


def reavaliar(resultados: List[Dict], catalogo) -> List[Dict]:
    """Recalcula a nota de uma rodada salva com o gabarito e o validador atuais (a resposta não muda).

    Permite comparar rodadas feitas em momentos diferentes pela mesma régua. A cobertura do contexto fica como foi
    medida na rodada, porque depende da busca usada nela.
    """
    gabarito = {p: (nome, c) for nome, casos in CONJUNTOS.items() for p, c in casos}
    out = []
    for r in resultados:
        nome, clausulas = gabarito[r['pergunta']]
        r = {**r, 'conjunto': nome}
        if 'resposta' in r:
            resp = {**r['resposta']}
            resp['validacao'] = [v for b in resp['blocos_gobr'] for v in validar_dsl(b, catalogo)]
            r = _pontuar(r, resp, clausulas)
        out.append(r)
    return out


def resumir(resultados: List[Dict], nomes: Sequence[str]) -> None:
    modelo = next((r['resposta']['modelo'] for r in resultados if 'resposta' in r), '?')
    print(f'\nmodelo: {modelo}')
    for nome in nomes:
        rs = [r for r in resultados if r['conjunto'] == nome]
        if not rs:
            continue
        n = len(rs)
        soma = lambda chave: sum(bool(r.get(chave)) for r in rs)
        clausulas_ok = sum('clausulas_faltando' in r and not r['clausulas_faltando'] for r in rs)
        corrigidos = sum(r.get('resposta', {}).get('tentativas', 1) > 1 for r in rs)
        tokens = sum(r.get('resposta', {}).get('uso', {}).get('input_tokens', 0) for r in rs)
        print(f'{nome}: aprovados {soma("aprovado")}/{n} · contexto cobre {soma("contexto_cobre")}/{n} · '
              f'cláusulas certas {clausulas_ok}/{n} · DSL válida {soma("dsl_valida")}/{n} · '
              f'citou fontes {soma("citou_fontes")}/{n} · com correção {corrigidos} · erros {soma("erro")} · '
              f'tokens de entrada {tokens}')


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
    ap.add_argument('--conjunto', choices=['ajuste', 'teste', 'todos'], default='todos')
    ap.add_argument('--busca', choices=['hibrida', 'vetorial'], default='hibrida')
    ap.add_argument('--tentativas', type=int, default=2)
    ap.add_argument('--sem-catalogo', action='store_true')
    ap.add_argument('--reavaliar', type=Path, metavar='JSON',
                    help='Recalcula a nota de uma rodada salva com --saida, sem gerar de novo')
    args = ap.parse_args()

    nomes = list(CONJUNTOS) if args.conjunto == 'todos' else [args.conjunto]
    if args.reavaliar:
        catalogo = None if args.sem_catalogo else carregar_catalogo()
        resultados = reavaliar(json.loads(args.reavaliar.read_text(encoding='utf-8')), catalogo)
        resumir(resultados, nomes)
        if args.saida:
            args.saida.write_text(json.dumps(resultados, ensure_ascii=False, indent=2), encoding='utf-8')
        return
    casos = [(nome, p, c) for nome in nomes for p, c in CONJUNTOS[nome]]
    recuperador = carregar_recuperador(hibrida=args.busca == 'hibrida')
    if args.so_busca:
        cobertos = {nome: 0 for nome in nomes}
        for nome, pergunta, clausulas in casos:
            ctx = recuperador.recuperar(pergunta, args.k_exemplos, args.k_manual)
            fora = faltando(_texto_contexto(ctx), clausulas, forma=True)
            cobertos[nome] += not fora
            print(f'[{"✓" if not fora else "✗"}] ({nome}) {pergunta}' + (f'  · fora do contexto: {fora}' if fora else ''))
        print('\ncontexto cobre todas as cláusulas: ' +
              ' · '.join(f'{n} {cobertos[n]}/{len(CONJUNTOS[n])}' for n in nomes) +
              f'  (k_exemplos={args.k_exemplos}, k_manual={args.k_manual})')
        return

    catalogo = None if args.sem_catalogo else carregar_catalogo()
    gerador = Gerador(criar_backend(args.backend, args.modelo, args.esforco), catalogo, args.tentativas)
    resultados = []
    for nome, pergunta, clausulas in casos:
        inicio = time.perf_counter()
        r = {'conjunto': nome, **avaliar_caso(recuperador, gerador, pergunta, clausulas, args.k_exemplos, args.k_manual)}
        r['segundos'] = round(time.perf_counter() - inicio, 1)
        resultados.append(r)
        if 'erro' in r:
            print(f'[ERRO ] ({nome}) {pergunta}\n        {r["erro"]}', flush=True)
            continue
        marca = 'OK   ' if r['aprovado'] else 'FALHA'
        print(f'[{marca}] ({nome}) {pergunta}  ({r["segundos"]} s)')
        print(f'        contexto {"✓" if r["contexto_cobre"] else "✗ " + str(r["fora_do_contexto"])} · '
              f'dsl {"✓" if r["dsl_valida"] else "✗"} · citações {r["resposta"]["citacoes"]}'
              + (f' · tentativas {r["resposta"]["tentativas"]}' if r['resposta'].get('tentativas', 1) > 1 else '')
              + (f' · inválidas {r["citacoes_invalidas"]}' if r['citacoes_invalidas'] else '')
              + (f' · faltando na regra {r["clausulas_faltando"]}' if r['clausulas_faltando'] else ''), flush=True)

    resumir(resultados, nomes)
    if args.saida:
        args.saida.write_text(json.dumps(resultados, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
