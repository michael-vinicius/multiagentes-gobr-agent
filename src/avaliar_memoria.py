"""Avaliação da memória do agente (etapa 6), com usuário simulado e comparação com uma linha de base.

Cenários em data/cenarios_memoria.json, escritos (com o resultado esperado) antes de rodar o modelo. Cada cenário
roda em dois braços:
- "memoria": o agente da etapa 6 (sessão em SQLite, conversa depois do arquivo, memória de longo prazo,
  compactação do histórico);
- "base": o comportamento da etapa 5 (sessão só na RAM, depois do arquivo só "ajuste" ou "fim", nada entre
  sessões), para medir o que a memória muda;
- "sem-compactacao": a etapa 6 com o histórico inteiro nas chamadas ao modelo (só no cenário de conversa longa).

Cada sessão de um cenário é um "processo" novo: grafo novo e conexões SQLite reabertas. No braço base, um processo
novo perde a sessão (InMemorySaver). Métricas: concordância do arquivo final com o esperado (simulador, ~6,4 mil
clientes), decisões pontuais em versões intermediárias, conteúdo de respostas, perguntas feitas, chamadas e tokens
por etapa (o Ollama informa prompt_eval_count), tempo.
"""
from __future__ import annotations

import json
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence

from simulador_gobr import Cliente, comparar, decidir, regras_do_texto


def aplicar_trocas(gobr: str, trocas: Sequence[Sequence[str]]) -> str:
    """[[trecho do nome do bloco, de, para], ...]: troca só dentro do bloco indicado."""
    partes = re.split(r'(?m)^(?=parametros ")', gobr)
    for nome, de, para in trocas:
        alvo = [i for i, p in enumerate(partes) if p.startswith('parametros "') and nome in p.split('\n', 1)[0]]
        if len(alvo) != 1 or de not in partes[alvo[0]]:
            raise ValueError(f'troca inválida no gabarito: bloco "{nome}", trecho "{de}"')
        partes[alvo[0]] = partes[alvo[0]].replace(de, para)
    return ''.join(partes)


def esperado_final(esp: Dict[str, Any], exemplos: Optional[Path]) -> str:
    if 'gobr' in esp:
        return esp['gobr']
    if exemplos is None:
        raise ValueError('o cenário usa um exemplo do professor: informe --exemplos')
    return aplicar_trocas((exemplos / esp['exemplo']).read_text(encoding='utf-8'), esp.get('trocas', []))


def responder_perguntas(pedido: Dict[str, Any], roteiro: Dict[str, str]) -> str:
    partes = []
    for n, p in enumerate(pedido.get('perguntas') or [], 1):
        for padrao, resposta in roteiro.items():
            if re.fullmatch(padrao, p['id']):
                partes.append(f'{n}{resposta}' if re.fullmatch(r'[a-z]', resposta) else f'{n}: {resposta}')
                break
    return (', '.join(partes) + '; o resto com as sugestões') if partes else 'ok'


def rodar_sessao(fabrica: Callable[[], Any], cfg: Dict[str, Any], entrada: str, thread: str) -> Dict[str, Any]:
    """Roda uma sessão com o usuário simulado. `fabrica()` cria o grafo como um processo novo do programa."""
    from agente import pendencias
    from langgraph.types import Command
    config = {'configurable': {'thread_id': thread}, 'recursion_limit': 600}
    conversa = list(cfg.get('conversa') or [])
    grafo = fabrica()
    dialogo: List[Dict[str, str]] = []
    perguntas: List[str] = []
    reiniciou = False
    t0 = time.time()
    resultado = grafo.invoke({'entrada': entrada}, config)
    while '__interrupt__' in resultado:
        pedido = resultado['__interrupt__'][0].value
        tipo = pedido['tipo']
        if tipo == 'perguntas' and cfg.get('reiniciar_na_pergunta') and not reiniciou:
            reiniciou = True
            grafo = fabrica()  # o programa foi fechado com a pergunta na tela e aberto de novo
            if pendencias(grafo, thread):
                dialogo.append({'tipo': 'reinicio', 'agente': '(programa reaberto: sessão retomada do SQLite)',
                                'analista': ''})
            else:
                dialogo.append({'tipo': 'reinicio', 'agente': '(programa reaberto: a sessão se perdeu; recomeça)',
                                'analista': ''})
                resultado = grafo.invoke({'entrada': entrada}, config)
                continue
        if tipo == 'perguntas':
            perguntas += [p['id'] for p in pedido.get('perguntas') or []]
            resposta = responder_perguntas(pedido, cfg.get('perguntas') or {})
        elif tipo == 'resultado':
            resposta = conversa.pop(0) if conversa else 'fim'
        elif tipo == 'recordar':
            resposta = cfg.get('recordar', 'a')
        elif tipo == 'memoria':
            resposta = cfg.get('memoria', 'sim')
        else:
            resposta = 'ok'
        dialogo.append({'tipo': tipo, 'agente': pedido['mensagem'], 'analista': resposta})
        resultado = grafo.invoke(Command(resume=resposta), config)
    final = (resultado.get('mensagens') or [''])[-1]
    if not dialogo or dialogo[-1]['agente'] != final:
        dialogo.append({'tipo': 'final', 'agente': final, 'analista': ''})
    return {'resultado': resultado, 'dialogo': dialogo, 'perguntas': perguntas, 'segundos': round(time.time() - t0)}


def resposta_ao_turno(dialogo: Sequence[Dict[str, str]], inicio: str) -> Optional[str]:
    for j, d in enumerate(dialogo):
        if d['analista'].lower().startswith(inicio.lower()):
            return dialogo[j + 1]['agente'] if j + 1 < len(dialogo) else None
    return None


def decisao(arquivo: str, cliente: Dict[str, Any]) -> str:
    return decidir(regras_do_texto(arquivo), Cliente(**cliente))[0]


def medir(cenario: Dict[str, Any], sessoes: List[Dict[str, Any]], exemplos: Optional[Path], uso: List[Dict]) -> Dict:
    esp = cenario['esperado']
    ultima = sessoes[-1]
    arquivo = ultima['resultado'].get('arquivo_gobr', '')
    cmp = comparar(regras_do_texto(esperado_final(esp['final'], exemplos)), regras_do_texto(arquivo))
    checagens: List[Dict[str, Any]] = []
    for v in esp.get('versoes', []):
        s = sessoes[v['sessao']] if v['sessao'] < len(sessoes) else None
        versoes = (s or {}).get('resultado', {}).get('versoes') or []
        for d in v['decisoes']:
            obtido = decisao(versoes[v['versao']]['arquivo_gobr'], d['cliente']) if len(versoes) > v['versao'] else \
                'versão não existe'
            checagens.append({'checagem': f'versão {v["versao"]}: {d["cliente"]} → {d["acao"]}', 'obtido': obtido,
                              'ok': obtido == d['acao']})
    for r in esp.get('respostas', []):
        s = sessoes[r['sessao']] if r['sessao'] < len(sessoes) else None
        txt = resposta_ao_turno(s['dialogo'], r['turno']) if s else None
        # uma resposta que é o arquivo regenerado não responde à pergunta (o texto padrão do arquivo fala de "ordem")
        regenerou = bool(txt) and bool(re.match(r'(Versão \d+ do arquivo|Regras em GoBR)', txt))
        ok = bool(txt) and not regenerou and any(k.lower() in txt.lower() for k in r['contem_algum'])
        checagens.append({'checagem': f'resposta a "{r["turno"]}…" cita {r["contem_algum"]}', 'obtido': (txt or '')[:400],
                          'ok': ok})
    for m in esp.get('mensagens', []):
        s = sessoes[m['sessao']] if m['sessao'] < len(sessoes) else None
        ok = bool(s) and any(m['contem'] in d['agente'] for d in s['dialogo'])
        checagens.append({'checagem': f'mensagem da sessão {m["sessao"] + 1} contém "{m["contem"]}"', 'ok': ok})
    if 'perguntas_max_ultima_sessao' in esp:
        n = len(ultima['perguntas'])
        checagens.append({'checagem': f'perguntas na última sessão ≤ {esp["perguntas_max_ultima_sessao"]}',
                          'obtido': n, 'ok': n <= esp['perguntas_max_ultima_sessao']})
    interpretacoes = sum(1 for u in uso if u['etapa'] == 'interpretar')
    if 'interpretacoes_max' in esp:
        checagens.append({'checagem': f'interpretações da descrição ≤ {esp["interpretacoes_max"]}',
                          'obtido': interpretacoes, 'ok': interpretacoes <= esp['interpretacoes_max']})
    conversa = [u for u in uso if u['etapa'] in ('entender', 'responder_pergunta')]
    janela = sum(1 for s in sessoes for d in s['dialogo'] if 'não coube na janela' in d['agente'])
    return {
        'concordancia': cmp.concordancia, 'divergencias': cmp.resumo(4), 'checagens': checagens,
        'checagens_ok': sum(c['ok'] for c in checagens), 'checagens_total': len(checagens),
        'perguntas_por_sessao': [len(s['perguntas']) for s in sessoes],
        'segundos_por_sessao': [s['segundos'] for s in sessoes],
        'chamadas_modelo': len(uso), 'chamadas_por_etapa': {e: sum(1 for u in uso if u['etapa'] == e)
                                                            for e in sorted({u['etapa'] for u in uso})},
        'maior_prompt': max((u['entrada'] for u in uso), default=0),
        'maior_prompt_conversa': max((u['entrada'] for u in conversa), default=0),
        'prompts_conversa': [u['entrada'] for u in conversa],
        'estouros_de_janela': janela, 'interpretacoes': interpretacoes,
    }


def entrada_da_sessao(cfg: Dict[str, Any], exemplos: Optional[Path]) -> str:
    e = cfg['entrada']
    if e.startswith('exemplo:'):
        if exemplos is None:
            raise ValueError('o cenário usa um exemplo do professor: informe --exemplos')
        return str(exemplos / e.split(':', 1)[1])
    return e


def rodar_cenario(cenario: Dict[str, Any], braco: str, base_servicos: Any, exemplos: Optional[Path],
                  pasta: Path) -> Dict[str, Any]:
    import sqlite3
    from agente import abrir_memoria, criar_grafo
    from langgraph.checkpoint.sqlite import SqliteSaver
    pasta_mem = pasta / 'memoria' / f'{cenario["id"]}-{braco}'
    shutil.rmtree(pasta_mem, ignore_errors=True)
    servicos = base_servicos
    servicos.conversa = braco != 'base'
    servicos.compactar = braco != 'sem-compactacao'
    servicos.backend.uso = []

    def fabrica():
        if braco == 'base':
            servicos.memoria = None
            return criar_grafo(servicos)  # InMemorySaver novo: um processo novo não vê a sessão anterior
        _, mem = abrir_memoria(pasta_mem, 'avaliacao')
        servicos.memoria = mem
        saver = SqliteSaver(sqlite3.connect(str(pasta_mem / 'sessoes.sqlite'), check_same_thread=False))
        return criar_grafo(servicos, saver)

    sessoes = []
    for cfg in cenario['sessoes']:
        if braco not in cfg.get('so_bracos', [braco]):
            continue
        sessoes.append(rodar_sessao(fabrica, cfg, entrada_da_sessao(cfg, exemplos), f'{cfg["thread"]}-{braco}'))
    m = medir(cenario, sessoes, exemplos, list(servicos.backend.uso))
    return {'id': cenario['id'], 'braco': braco, **m, 'sessoes': [
        {'dialogo': s['dialogo'], 'perguntas': s['perguntas'], 'segundos': s['segundos'],
         'arquivo_gobr': s['resultado'].get('arquivo_gobr', ''),
         'versoes': [{'n': v['n'], 'pedido': v['pedido'], 'arquivo_gobr': v['arquivo_gobr']}
                     for v in s['resultado'].get('versoes') or []]} for s in sessoes],
        'uso': list(servicos.backend.uso)}


def manter_acordado() -> None:
    """No Windows, impede o computador de suspender enquanto a avaliação roda (só durante este processo).

    Na 1ª rodada, uma chamada ao modelo ficou 14 h aberta porque o computador suspendeu no meio dela."""
    if sys.platform == 'win32':
        import ctypes
        ES_CONTINUOUS, ES_SYSTEM_REQUIRED = 0x80000000, 0x00000001
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)


def remedir(cenarios: Sequence[Dict[str, Any]], pasta: Path, exemplos: Optional[Path]) -> int:
    linhas = []
    for c in cenarios:
        for braco in c['bracos']:
            f = pasta / f'{c["id"]}-{braco}.json'
            if not f.exists():
                continue
            r = json.loads(f.read_text(encoding='utf-8'))
            sessoes = [{'resultado': {'arquivo_gobr': s['arquivo_gobr'], 'versoes': s['versoes']},
                        'dialogo': s['dialogo'], 'perguntas': s['perguntas'], 'segundos': s['segundos']}
                       for s in r['sessoes']]
            r.update(medir(c, sessoes, exemplos, r['uso']))
            f.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding='utf-8')
            linhas.append({k: v for k, v in r.items() if k not in ('sessoes', 'uso', 'prompts_conversa')})
            print(f'{c["id"]:30s} {braco:16s} arquivo {r["concordancia"]:6.1%}  checagens {r["checagens_ok"]}/'
                  f'{r["checagens_total"]}')
            for ch in r['checagens']:
                if not ch['ok']:
                    print(f'    ✗ {ch["checagem"]}: {str(ch.get("obtido", ""))[:120]}')
    (pasta / 'resumo.json').write_text(json.dumps(linhas, ensure_ascii=False, indent=2), encoding='utf-8')
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description='Avalia a memória do agente com cenários de várias sessões.')
    ap.add_argument('--cenarios', type=Path, default=Path('data/cenarios_memoria.json'))
    ap.add_argument('--exemplos', type=Path, help='Pasta com os exemplos do professor (.pdf + .gobr)')
    ap.add_argument('--so', nargs='*', help='Só os cenários cujo id contém um destes textos')
    ap.add_argument('--bracos', nargs='*', help='Só estes braços (memoria, base, sem-compactacao)')
    ap.add_argument('--saida', type=Path, default=Path('resultados/memoria'))
    ap.add_argument('--remedir', action='store_true',
                    help='Recalcula as métricas a partir dos diálogos já salvos em --saida, sem rodar o modelo')
    args = ap.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    args.saida.mkdir(parents=True, exist_ok=True)
    cenarios = json.loads(args.cenarios.read_text(encoding='utf-8'))
    if args.so:
        cenarios = [c for c in cenarios if any(s in c['id'] for s in args.so)]

    if args.remedir:
        return remedir(cenarios, args.saida, args.exemplos)
    manter_acordado()
    from agente import criar_servicos
    servicos = criar_servicos('ollama')
    linhas = []
    for c in cenarios:
        for braco in c['bracos']:
            if args.bracos and braco not in args.bracos:
                continue
            r = rodar_cenario(c, braco, servicos, args.exemplos, args.saida)
            (args.saida / f'{c["id"]}-{braco}.json').write_text(json.dumps(r, ensure_ascii=False, indent=2),
                                                                 encoding='utf-8')
            linha = {k: v for k, v in r.items() if k not in ('sessoes', 'uso', 'prompts_conversa')}
            linhas.append(linha)
            print(f'{c["id"]:30s} {braco:16s} arquivo {r["concordancia"]:6.1%}  checagens {r["checagens_ok"]}/'
                  f'{r["checagens_total"]}  perguntas {r["perguntas_por_sessao"]}  chamadas {r["chamadas_modelo"]}  '
                  f'maior prompt {r["maior_prompt"]} (conversa {r["maior_prompt_conversa"]})  estouros '
                  f'{r["estouros_de_janela"]}  {sum(r["segundos_por_sessao"])} s', flush=True)
            for ch in r['checagens']:
                if not ch['ok']:
                    print(f'    ✗ {ch["checagem"]}: {str(ch.get("obtido", ""))[:160]}', flush=True)
            for d in r['divergencias'][:2]:
                print(f'    ≠ {d}', flush=True)
    (args.saida / 'resumo.json').write_text(json.dumps(linhas, ensure_ascii=False, indent=2), encoding='utf-8')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
