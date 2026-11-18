"""Avaliação ponta a ponta do agente conversacional contra gabaritos, com um usuário simulado.

Casos:
- exemplos do professor (pasta com pares <nome>.pdf + <nome>.gobr): a entrada é o PDF; com `--imagem`, o PDF é
  renderizado em PNG (1569 a 2268 px de largura) e entra pelo OCR, como uma imagem enviada pelo analista;
- cenários próprios (data/cenarios_agente.json): descrições em texto escritas para esta avaliação, com gabarito e
  respostas do analista definidos antes de rodar o agente.

O usuário simulado responde às perguntas pelo id (roteiro de cada cenário) e aceita a sugestão nas demais. Nos
exemplos do professor não há roteiro: ele aceita todas as sugestões.

Métricas por caso, todas pela simulação semântica (simulador_gobr.py, ~6,4 mil clientes sintéticos):
- arquivo: decisões do arquivo gerado iguais às do gabarito;
- plano: decisões do plano (moldes dos blocos planejados) iguais às do gabarito; separa erro de entendimento e
  decisão (plano) de erro de redação (arquivo);
- estrutura: blocos aprovados na conferência da etapa 4 (classificador + catálogo de cláusulas).
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from especificacao import BlocoPlano, molde
from simulador_gobr import comparar, regras_do_texto


def usuario_simulado(roteiro: Dict[str, str]):
    """Responde "1a, 3: 28 dias; o resto com as sugestões" a partir do roteiro {regex do id: resposta}."""
    def responder(pedido: Dict[str, Any]) -> str:
        if pedido.get('tipo') != 'perguntas':
            return 'fim'
        partes = []
        for n, p in enumerate(pedido.get('perguntas') or [], 1):
            for padrao, resposta in roteiro.items():
                if re.fullmatch(padrao, p['id']):
                    partes.append(f'{n}{resposta}' if re.fullmatch(r'[a-z]', resposta) else f'{n}: {resposta}')
                    break
        return (', '.join(partes) + '; o resto com as sugestões') if partes else 'ok'
    return responder


def rodar_caso(grafo, entrada: str, roteiro: Dict[str, str], thread: str) -> Dict[str, Any]:
    from langgraph.types import Command
    config = {'configurable': {'thread_id': thread}, 'recursion_limit': 300}
    responder = usuario_simulado(roteiro)
    dialogo: List[Dict[str, str]] = []
    resultado = grafo.invoke({'entrada': entrada}, config)
    while '__interrupt__' in resultado:
        pedido = resultado['__interrupt__'][0].value
        resposta = responder(pedido)
        dialogo.append({'agente': pedido['mensagem'], 'analista': resposta})
        resultado = grafo.invoke(Command(resume=resposta), config)
    resultado['dialogo'] = dialogo
    return resultado


def medir(resultado: Dict[str, Any], gabarito: str) -> Dict[str, Any]:
    esperado = regras_do_texto(gabarito)
    arquivo = resultado.get('arquivo_gobr', '')
    cmp_arquivo = comparar(esperado, regras_do_texto(arquivo))
    plano = [BlocoPlano(**b) for b in resultado.get('plano') or []]
    moldes = [molde(b, resultado.get('nome_time', 't')) for b in plano]
    cmp_plano = comparar(esperado, regras_do_texto('\n\n'.join(moldes))) if all(m is not None for m in moldes) \
        else None
    rel = resultado.get('relatorio') or {}
    validacao = rel.get('validacao') or []
    perguntas = []
    for turno in resultado.get('dialogo', []):
        trecho = turno['agente'].split('preciso decidir:', 1)
        if len(trecho) == 2:
            perguntas += re.findall(r'^\d+\. (.*)$', trecho[1], re.M)
    return {
        'arquivo': cmp_arquivo.concordancia, 'arquivo_divergencias': cmp_arquivo.resumo(6),
        'arquivo_indeterminados': cmp_arquivo.indeterminados,
        'plano': None if cmp_plano is None else cmp_plano.concordancia,
        'plano_divergencias': [] if cmp_plano is None else cmp_plano.resumo(6),
        'estrutura_ok': sum(1 for v in validacao if v['status'] == 'ok'), 'blocos': len(validacao),
        'problemas_estrutura': [f'{v["bloco"]}: {"; ".join(v["problemas"])}' for v in validacao if v['status'] != 'ok'],
        'fontes': rel.get('fontes'), 'corrigidos': rel.get('corrigidos'),
        'nao_verificados': [b['nome'] for b in resultado.get('blocos') or [] if b.get('verificacao') == 'nao_verificado'],
        'perguntas': perguntas,
        'avisos': resultado.get('avisos') or [],
    }


# Respostas do analista nos exemplos do professor quando não há sugestão segura. Só o Infinitto em imagem precisa: o
# OCR perde o "7 dias" do ramo "Risco de inatividade", o agente pergunta a frequência, e o analista (que está vendo a
# imagem que ele mesmo enviou) responde. Sem esta resposta a regra fica fora do arquivo (96,3% na rodada v1).
ROTEIRO_EXEMPLOS = {'RegraInfinittoDesign (imagem)': {r'frequencia:.*': '7 dias'}}


def casos_exemplos(pasta: Path, imagem: bool, saida: Path) -> List[Dict[str, Any]]:
    casos = []
    for gobr in sorted(pasta.glob('*.gobr')):
        pdf = gobr.with_suffix('.pdf')
        if not pdf.exists():
            continue
        entrada = pdf
        if imagem:
            import pypdfium2 as pdfium
            entrada = saida / f'{gobr.stem}.png'
            pdfium.PdfDocument(str(pdf))[0].render(scale=2).to_pil().save(entrada)
        id_caso = f'{gobr.stem}{" (imagem)" if imagem else ""}'
        casos.append({'id': id_caso, 'entrada': str(entrada), 'respostas': ROTEIRO_EXEMPLOS.get(id_caso, {}),
                      'gabarito': gobr.read_text(encoding='utf-8')})
    return casos


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description='Avalia o agente contra gabaritos com um usuário simulado.')
    ap.add_argument('--exemplos', type=Path, help='Pasta com os pares <nome>.pdf + <nome>.gobr')
    ap.add_argument('--imagem', action='store_true', help='Envia os exemplos como PNG (passa pelo OCR)')
    ap.add_argument('--cenarios', type=Path, help='JSON com cenários próprios (ex.: data/cenarios_agente.json)')
    ap.add_argument('--so', nargs='*', help='Roda só os casos cujo id contém um destes textos')
    ap.add_argument('--saida', type=Path, default=Path('resultados/agente'))
    ap.add_argument('--backend', default='ollama')
    args = ap.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    args.saida.mkdir(parents=True, exist_ok=True)

    casos: List[Dict[str, Any]] = []
    if args.exemplos:
        casos += casos_exemplos(args.exemplos, args.imagem, args.saida)
    if args.cenarios:
        for c in json.loads(args.cenarios.read_text(encoding='utf-8')):
            casos.append({'id': c['id'], 'entrada': c['descricao'], 'respostas': c['respostas'],
                          'gabarito': c['gabarito']})
    if args.so:
        casos = [c for c in casos if any(s in c['id'] for s in args.so)]
    if not casos:
        print('nenhum caso; use --exemplos e/ou --cenarios')
        return 1

    from agente import criar_grafo, criar_servicos
    grafo = criar_grafo(criar_servicos(args.backend))
    linhas = []
    for n, caso in enumerate(casos, 1):
        t0 = time.time()
        resultado = rodar_caso(grafo, caso['entrada'], caso['respostas'], thread=f'aval-{n}-{time.time()}')
        m = medir(resultado, caso['gabarito'])
        m.update({'id': caso['id'], 'segundos': round(time.time() - t0)})
        nome = re.sub(r'[^\w-]+', '_', caso['id'])
        (args.saida / f'{nome}.gobr').write_text(resultado.get('arquivo_gobr', ''), encoding='utf-8')
        (args.saida / f'{nome}.json').write_text(json.dumps(
            {**m, 'dialogo': resultado.get('dialogo'), 'especificacao': resultado.get('especificacao'),
             'blocos': resultado.get('blocos')}, ensure_ascii=False, indent=2), encoding='utf-8')
        linhas.append(m)
        plano = '—' if m['plano'] is None else f'{m["plano"]:.1%}'
        print(f'{caso["id"]:40s} arquivo {m["arquivo"]:.1%}  plano {plano:>6}  estrutura {m["estrutura_ok"]}/'
              f'{m["blocos"]}  fontes {m["fontes"]}  corrigidos {m["corrigidos"]}  {m["segundos"]} s', flush=True)
        for d in m['arquivo_divergencias'][:3]:
            print(f'    ≠ {d}', flush=True)
    (args.saida / 'resumo.json').write_text(json.dumps(linhas, ensure_ascii=False, indent=2), encoding='utf-8')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
