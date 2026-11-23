"""Agente conversacional GoBR: da descrição (texto, imagem ou PDF) ao arquivo de regras, com um fluxo LangGraph.

    ler_entrada ─→ lembrar ──(empresa lembrada + pedido curto: "partir do arquivo anterior?")──→ ajustar ─→ revisar
                     └──(caso comum)──→ interpretar ─→ revisar ──(perguntas)──→ perguntar ⇄ analista ─→ incorporar ─┐
                                                         ↑  └──(sem perguntas)─→ planejar                          │
                                                         └─────────────────────────────────────────────────────────┘
    planejar ─→ redigir_bloco ─→ verificar_bloco ──(divergiu: corrigir)──→ redigir_bloco
                     ↑                  ├──(ok: próximo bloco)───────────────┘
                     │                  └──(todos)──→ montar ─→ responder ─→ aguardar ⇄ analista ─→ entender
                     │                                                                                 │
                     └── ajustar ◄──(ajuste, ou "aplica" depois de uma simulação)──────────────────────┤
                         conversa ◄──(pergunta, simulação, desfazer, comparar, lembrar/esquecer)───────┤ ─→ aguardar
                         memorizar ◄──(fim: o agente propõe o que guardar, o analista confirma)────────┘ ─→ END

Etapa 6 (memória, ver memoria.py): o estado da sessão é salvo por um checkpointer SQLite e pode ser retomado pelo
id; o histórico da conversa e as versões do arquivo ficam no estado (curto prazo); empresas, preferências e notas
ficam num LangGraph Store (longo prazo); o histórico entra nas chamadas ao modelo compactado (cabeça + cauda).

Papéis (cada nó tem uma responsabilidade e uma ferramenta):
- ler_entrada: transcreve imagem/PDF localmente (transcrever_entrada.py) ou numera o texto do analista;
- interpretar (modelo de linguagem, saída em JSON Schema): descrição → especificação estruturada;
- revisar (determinístico): pontos falhos da modelagem comercial → avisos e perguntas (lacunas.py);
- perguntar / aguardar: pausam o grafo (`interrupt`) até o analista responder;
- incorporar: respostas → decisões (formato "1a, 2: 21 dias" ou "ok"; texto livre passa pelo modelo);
- planejar (determinístico): blocos na ordem em que o GoBR os aplica;
- redigir_bloco (modelo + RAG da etapa 4): cada bloco é escrito a partir de exemplos reais e do manual recuperados,
  com a conferência de estrutura e catálogo da etapa 4;
- verificar_bloco (simulador): o bloco tem de decidir igual ao plano para ~3 mil clientes sintéticos; se divergir, o
  modelo recebe as divergências e tenta de novo; se continuar errado, entra o molde determinístico, com aviso;
- montar / responder: arquivo completo, verificação final e o resumo do que foi decidido;
- ajustar (modelo, JSON): pedidos de mudança depois da resposta ("prospects a cada 7 dias") editam a especificação;
- lembrar (memória de longo prazo): reconhece uma empresa já parametrizada e oferece partir do arquivo anterior;
- entender (regras de palavras; modelo só quando a mensagem depende da conversa): classifica a mensagem do
  analista depois do arquivo e reescreve referências ("aquela", "a mesma coisa") com o histórico;
- conversa: responde perguntas (modelo + manual), simula mudanças (simulador, sem aplicar), desfaz, compara versões
  e mostra/apaga o que o agente lembra;
- memorizar: no fim, propõe o que guardar para as próximas sessões e grava o que o analista confirmar.
"""
from __future__ import annotations

import json
import operator
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Annotated, Any, Dict, List, Optional, Sequence, Tuple, TypedDict

from especificacao import (BlocoPlano, Especificacao, SCHEMA_ESPECIFICACAO, interpretar, molde, montar_arquivo,
                           numerar_descricao, ramos_da_descricao)
from lacunas import (Decisao, Pergunta, aplicar_sugestoes, explicar_ordem, interpretar_respostas, planejar, revisar)
from langchain_core.runnables import RunnableConfig

from memoria import (OPCOES_PREFERENCIA, PREFERENCIAS, agora, aplicar_lembradas, chave_empresa, como_transcricao,
                     estimar_tokens, montar_historico, preferencia_do_texto)
from simulador_gobr import comparar, regras_do_texto

MAX_RODADAS_PERGUNTAS = 3
MAX_TENTATIVAS_BLOCO = 2  # redação + 1 correção semântica; depois disso entra o molde


class Estado(TypedDict, total=False):
    entrada: str
    descricao: str
    origem: str
    especificacao: Dict[str, Any]
    decisoes: Dict[str, Dict[str, Any]]
    perguntas: List[Dict[str, Any]]
    avisos: List[str]
    rodadas: int
    resposta_usuario: str
    plano: List[Dict[str, Any]]
    nome_time: str
    vendedores: str
    blocos: List[Dict[str, Any]]
    candidato: Dict[str, Any]
    feedback: str
    tentativa: int
    arquivo_gobr: str
    relatorio: Dict[str, Any]
    mensagens: Annotated[List[str], operator.add]
    fim: bool
    # etapa 6: memória de curto prazo (sessão) e o que veio da memória de longo prazo
    historico: Annotated[List[Dict[str, str]], operator.add]  # {'papel': 'analista'|'agente', 'texto': ...}
    versoes: List[Dict[str, Any]]  # cada arquivo gerado (ou restaurado), com especificação, plano e decisões
    intencao: str
    pedido: str
    proposta: Optional[Dict[str, Any]]  # especificação simulada à espera de "aplica"
    proposta_pedido: str
    empresa: str  # chave da empresa reconhecida na memória
    partiu_da_memoria: bool
    lembrete: str


@dataclass
class Servicos:
    """Dependências do grafo (o modelo, o RAG e o catálogo), injetadas para que os testes usem dublês."""
    backend: Any
    recuperador: Any
    gerador: Any
    transcrever: Any = None
    k_exemplos: int = 4
    k_manual: int = 3
    memoria: Any = None  # MemoriaLonga (memoria.py); None = sem memória de longo prazo
    conversa: bool = True  # False = comportamento da etapa 5 depois do arquivo (só "ajuste" ou "fim")
    compactar: bool = True  # False = histórico inteiro nas chamadas ao modelo (linha de base da avaliação)


# ---------------------------------------------------------------- utilidades

def _decisoes(estado: Estado) -> Dict[str, Decisao]:
    return {k: Decisao(**v) for k, v in (estado.get('decisoes') or {}).items()}


def _perguntas(estado: Estado) -> List[Pergunta]:
    return [Pergunta(**p) for p in estado.get('perguntas') or []]


def _plano(estado: Estado) -> List[BlocoPlano]:
    return [BlocoPlano(**b) for b in estado.get('plano') or []]


def _parece_arquivo(texto: str) -> Optional[Path]:
    t = texto.strip().strip('"').strip("'")
    if '\n' in t or len(t) > 400:
        return None
    p = Path(t)
    return p if p.suffix and p.exists() else None


# o que define uma versão do arquivo: restaurar estes campos restaura a versão inteira (desfazer, memória)
CAMPOS_VERSAO = ('arquivo_gobr', 'especificacao', 'plano', 'decisoes', 'blocos', 'relatorio', 'nome_time',
                 'vendedores', 'avisos')


def _foto(estado: Estado, n: int, pedido: str) -> Dict[str, Any]:
    return {**{k: estado.get(k) for k in CAMPOS_VERSAO}, 'n': n, 'pedido': pedido}


def _etapa(servicos: Servicos, nome: str) -> None:
    """Rótulo da etapa nas chamadas seguintes ao modelo (telemetria de tokens por etapa)."""
    try:
        servicos.backend.etapa = nome
    except AttributeError:
        pass


def _chave_bloco(bloco: Dict[str, Any], nome_time: str) -> str:
    return json.dumps({**bloco, '_time': nome_time}, sort_keys=True, ensure_ascii=False)


def bloco_reaproveitavel(versoes: Sequence[Dict[str, Any]], bloco: BlocoPlano, nome_time: str) -> Optional[Dict]:
    """Bloco idêntico já aceito numa versão anterior (memória de trabalho da sessão): um ajuste que muda uma regra
    não precisa redigir as outras de novo. O bloco reaproveitado ainda passa pela verificação semântica."""
    chave = _chave_bloco(asdict(bloco), nome_time)
    for v in reversed(list(versoes or [])):
        for b_plano, b in zip(v.get('plano') or [], v.get('blocos') or []):
            if b.get('verificacao') == 'ok' and b.get('gobr') and _chave_bloco(b_plano, v.get('nome_time')) == chave:
                return b
    return None


def formatar_perguntas(perguntas: Sequence[Pergunta]) -> str:
    linhas = []
    for n, p in enumerate(perguntas, 1):
        linhas.append(f'{n}. {p.texto}')
        for i, o in enumerate(p.opcoes):
            marca = '  ← sugestão' if p.sugestao == i else ''
            linhas.append(f'   {chr(ord("a") + i)}) {o}{marca}')
        if p.motivo:
            linhas.append(f'   (por quê: {p.motivo})')
    return '\n'.join(linhas)


def formatar_entendimento(esp: Especificacao) -> str:
    rot = {'frequencia': 'atender', 'nao_agendar': 'não agendar', 'agendar': 'agendar (padrão)',
           'fora_do_escopo': 'fora do escopo'}
    linhas = [f'Equipe: {esp.equipe.replace("nao_informado", "não informada")}']
    for it in esp.itens:
        partes = []
        if it.comprou_nos_ultimos_dias is not None or it.sem_comprar_ha_mais_de_dias is not None:
            a, b = it.sem_comprar_ha_mais_de_dias, it.comprou_nos_ultimos_dias
            partes.append('compra ' + ' e '.join(x for x in (f'há mais de {a} dias' if a is not None else '',
                                                             f'nos últimos {b} dias' if b is not None else '') if x))
        partes += it.filtros + it.outras_condicoes
        partes += [f'exceto {f}' for f in it.exceto]
        acao = rot.get(it.acao, it.acao)
        if it.acao == 'frequencia':
            acao += f' a cada {it.frequencia_dias} dias' if it.frequencia_dias else ' (frequência não informada)'
        linhas.append(f'- {it.nome}: {"; ".join(partes) or "todos"} → {acao}')
    return '\n'.join(linhas)


# ---------------------------------------------------------------- nós

def criar_grafo(servicos: Servicos, checkpointer: Any = None):
    from langgraph.graph import END, START, StateGraph
    from langgraph.types import interrupt

    def ler_entrada(estado: Estado) -> Estado:
        entrada = estado['entrada']
        arquivo = _parece_arquivo(entrada)
        if arquivo is not None:
            transcrever = servicos.transcrever
            if transcrever is None:
                from transcrever_entrada import transcrever
            t = transcrever(arquivo)
            descricao = t.como_texto()
            return {'descricao': descricao, 'origem': t.origem,
                    'mensagens': [f'Li o arquivo {arquivo.name} ({"camada de texto do PDF" if t.origem == "pdf-texto" else "OCR local"}).'],
                    'historico': [{'papel': 'analista', 'texto': f'(enviou o arquivo {arquivo.name})\n{descricao}'}]}
        return {'descricao': numerar_descricao(entrada), 'origem': 'texto', 'mensagens': [],
                'historico': [{'papel': 'analista', 'texto': entrada}]}

    def lembrar(estado: Estado) -> Estado:
        """Memória de longo prazo, na entrada: a empresa já foi parametrizada antes?

        - pedido curto ("Maxlub: prospects agora a cada 7 dias"): oferece partir do arquivo aprovado e das decisões
          daquela sessão; o pedido vira um ajuste e nada é perguntado de novo;
        - descrição completa de uma empresa lembrada: as respostas daquela sessão viram sugestões na revisão.
        """
        mem = servicos.memoria
        if mem is None:
            return {}
        achada = mem.achar_empresa(f'{estado["entrada"]}\n{estado.get("descricao", "")}')
        if achada is None:
            return {}
        chave, emp = achada
        versao = emp.get('versao') or {}
        curto = estado.get('origem') == 'texto' and len(ramos_da_descricao(estado.get('descricao', ''))) <= 2
        if not curto or not versao.get('arquivo_gobr'):
            return {'empresa': chave, 'lembrete': f'Lembro de "{emp.get("titulo", chave)}" (sessão de {emp.get("data")}): '
                                                  'as respostas daquela sessão entram como sugestão nas perguntas.'}
        mensagem = (f'Já parametrizei "{emp.get("titulo", chave)}" em {emp.get("data")} '
                    f'({len(versao.get("blocos") or [])} blocos, {len(versao.get("decisoes") or {})} decisões). '
                    'Quer partir daquele arquivo e aplicar este pedido a ele?\n'
                    '   a) sim, partir do arquivo anterior  ← sugestão\n'
                    '   b) não, começar do zero\n'
                    '(por quê: o arquivo anterior já foi revisado e aprovado; partir dele evita refazer as perguntas)')
        resposta = str(interrupt({'tipo': 'recordar', 'mensagem': mensagem, 'empresa': chave}))
        historico = [{'papel': 'agente', 'texto': mensagem}, {'papel': 'analista', 'texto': resposta}]
        if re.match(r'^\s*(b\b|n[aã]o|nao|do zero|come[cç]ar)', resposta, re.I):
            return {'empresa': chave, 'historico': historico}
        return {**{k: versao.get(k) for k in CAMPOS_VERSAO}, 'empresa': chave, 'partiu_da_memoria': True,
                'versoes': [{**versao, 'n': 0, 'pedido': f'arquivo lembrado de {emp.get("data")}'}],
                'resposta_usuario': estado['entrada'], 'pedido': estado['entrada'], 'rodadas': 0,
                'historico': historico}

    def apos_lembrar(estado: Estado) -> str:
        return 'ajustar' if estado.get('partiu_da_memoria') else 'interpretar'

    def no_interpretar(estado: Estado) -> Estado:
        _etapa(servicos, 'interpretar')
        esp = interpretar(servicos.backend, estado['descricao'])
        return {'especificacao': esp.to_dict(), 'decisoes': estado.get('decisoes') or {}, 'rodadas': 0}

    def no_revisar(estado: Estado) -> Estado:
        esp = Especificacao.from_dict(estado['especificacao'])
        rev = revisar(esp, _decisoes(estado))
        mem = servicos.memoria
        if mem is not None:
            lembradas = dict(mem.preferencias())
            emp = mem.empresa(estado['empresa']) if estado.get('empresa') else None
            for pid, d in ((emp or {}).get('versao') or {}).get('decisoes', {}).items():
                if pid in PREFERENCIAS and d.get('opcao') is not None:  # a decisão da própria empresa vale mais
                    lembradas[pid] = {'opcao': d['opcao'], 'data': emp.get('data'),
                                      'origem': f'na parametrização de "{emp.get("titulo")}"'}
            aplicar_lembradas(rev.perguntas, lembradas)
        return {'perguntas': [p.to_dict() for p in rev.perguntas], 'avisos': rev.avisos}

    def apos_revisar(estado: Estado) -> str:
        if estado.get('perguntas') and estado.get('rodadas', 0) < MAX_RODADAS_PERGUNTAS:
            return 'perguntar'
        return 'planejar'

    def perguntar(estado: Estado) -> Estado:
        esp = Especificacao.from_dict(estado['especificacao'])
        partes = []
        if estado.get('rodadas', 0) == 0:
            if estado.get('lembrete'):
                partes += [estado['lembrete'], '']
            if estado.get('origem') in ('ocr', 'pdf-texto') and not estado.get('partiu_da_memoria'):
                partes += ['Transcrição do arquivo (confira se está fiel):', estado['descricao'], '']
            partes += ['Entendi assim:', formatar_entendimento(esp), '']
            if estado.get('avisos'):
                partes += ['Pontos de atenção:'] + [f'- {a}' for a in estado['avisos']] + ['']
        else:
            ultima = estado.get('rodadas', 0) >= MAX_RODADAS_PERGUNTAS - 1
            partes += ['Estas perguntas não têm sugestão segura, então "ok" não as resolve.'
                       + (' Sem resposta agora, a regra fica fora do arquivo (com aviso).' if ultima else ''), '']
        partes += ['Antes de escrever as regras, preciso decidir:', formatar_perguntas(_perguntas(estado)), '',
                   'Responda por número e letra (ex.: "1a, 2b, 3: 21 dias"), escreva livremente, ou "ok" para usar as '
                   'sugestões.']
        mensagem = '\n'.join(partes)
        resposta = interrupt({'tipo': 'perguntas', 'mensagem': mensagem, 'perguntas': estado['perguntas']})
        return {'resposta_usuario': str(resposta), 'mensagens': [mensagem],
                'historico': [{'papel': 'agente', 'texto': mensagem}, {'papel': 'analista', 'texto': str(resposta)}]}

    def incorporar(estado: Estado) -> Estado:
        perguntas = _perguntas(estado)
        decisoes = _decisoes(estado)
        texto = estado.get('resposta_usuario', '')
        novas, aceite = interpretar_respostas(texto, perguntas)
        if not novas and not aceite and texto.strip():
            novas = _respostas_livres(servicos.backend, texto, perguntas)
        decisoes.update(novas)
        if aceite:
            aplicar_sugestoes(perguntas, decisoes)
        return {'decisoes': {k: asdict(v) for k, v in decisoes.items()}, 'rodadas': estado.get('rodadas', 0) + 1}

    def no_planejar(estado: Estado) -> Estado:
        esp = Especificacao.from_dict(estado['especificacao'])
        decisoes = _decisoes(estado)
        perguntas = _perguntas(estado)
        avisos = list(estado.get('avisos') or [])
        sem_resposta = [p for p in perguntas if p.id not in decisoes]
        pendentes = aplicar_sugestoes(perguntas, decisoes)
        for p in sem_resposta:
            if p.id not in pendentes:
                avisos.append(f'sem resposta para "{p.texto}"; usei a sugestão: {p.opcoes[p.sugestao]}')
        plano, nome_time, vendedores, avisos_plano = planejar(esp, decisoes)
        return {'plano': [asdict(b) for b in plano], 'nome_time': nome_time, 'vendedores': vendedores,
                'decisoes': {k: asdict(v) for k, v in decisoes.items()}, 'avisos': avisos + avisos_plano,
                'blocos': [], 'tentativa': 1, 'feedback': ''}

    def apos_planejar(estado: Estado) -> str:
        return 'redigir_bloco' if estado.get('plano') else 'montar'

    def redigir_bloco(estado: Estado) -> Estado:
        plano = _plano(estado)
        i = len(estado.get('blocos') or [])
        bloco = plano[i]
        if not estado.get('feedback'):
            antigo = bloco_reaproveitavel(estado.get('versoes') or [], bloco, estado['nome_time'])
            if antigo is not None:
                return {'candidato': {'gobr': antigo['gobr'], 'citacoes': antigo.get('citacoes', []), 'problemas': [],
                                      'exemplos': antigo.get('exemplos', []), 'trechos': antigo.get('trechos', []),
                                      'reaproveitado': True, 'fonte_original': antigo.get('fonte', 'modelo')}}
        _etapa(servicos, 'redigir')
        pedido = bloco.descricao(estado['nome_time'])
        ctx = servicos.recuperador.recuperar(pedido, servicos.k_exemplos, servicos.k_manual)
        if estado.get('feedback'):
            ctx.pergunta = (f'{pedido}\n\nAtenção: a versão anterior desta regra pegava os clientes errados:\n'
                            f'{estado["feedback"]}\n{dica_de_clausulas(bloco)}\n'
                            'Corrija as condições para pegar exatamente os clientes do pedido.')
        try:
            resp = servicos.gerador.gerar(ctx)
            gobr = resp.blocos_gobr[0] if resp.blocos_gobr else ''
            citacoes = resp.citacoes
            problemas = [p for v in resp.validacao for p in v['problemas']]
        except Exception as e:  # falha do modelo não derruba o fluxo: o molde cobre o bloco
            gobr, citacoes, problemas = '', [], [f'falha na geração: {e}']
        gobr = normalizar_bloco(gobr, bloco.nome, estado['nome_time'])
        return {'candidato': {'gobr': gobr, 'citacoes': citacoes, 'problemas': problemas,
                              'exemplos': [e.id for e in ctx.exemplos],
                              'trechos': [f'{t.secao} {t.titulo}' for t in ctx.trechos]}}

    def verificar_bloco(estado: Estado) -> Estado:
        plano = _plano(estado)
        blocos = list(estado.get('blocos') or [])
        i = len(blocos)
        bloco = plano[i]
        cand = estado['candidato']
        ref_bloco = molde(bloco, estado['nome_time'])
        aceitos = [b['gobr'] for b in blocos]
        status, detalhe = verificar_semantica(aceitos, cand['gobr'], plano[:i + 1], estado['nome_time'])
        tentativa = estado.get('tentativa', 1)
        if status in ('ok', 'nao_verificavel') and not cand['problemas'] and cand['gobr']:
            blocos.append({**cand, 'nome': bloco.nome, 'secao': bloco.secao,
                           'fonte': cand.get('fonte_original', 'modelo'), 'verificacao': status, 'tentativas': tentativa})
            return {'blocos': blocos, 'tentativa': 1, 'feedback': ''}
        if tentativa < MAX_TENTATIVAS_BLOCO:
            motivo = detalhe or '; '.join(cand['problemas']) or 'a resposta não trouxe a regra'
            return {'tentativa': tentativa + 1, 'feedback': motivo}
        if ref_bloco is not None:
            blocos.append({**cand, 'gobr': ref_bloco, 'nome': bloco.nome, 'secao': bloco.secao, 'fonte': 'molde',
                           'verificacao': 'ok', 'tentativas': tentativa,
                           'motivo_molde': detalhe or '; '.join(cand['problemas'])})
        else:
            blocos.append({**cand, 'nome': bloco.nome, 'secao': bloco.secao, 'fonte': 'modelo',
                           'verificacao': 'nao_verificado', 'tentativas': tentativa})
        return {'blocos': blocos, 'tentativa': 1, 'feedback': ''}

    def apos_verificar(estado: Estado) -> str:
        n = len(estado.get('blocos') or [])
        if estado.get('feedback'):
            return 'redigir_bloco'
        return 'redigir_bloco' if n < len(estado.get('plano') or []) else 'montar'

    def montar(estado: Estado) -> Estado:
        plano = _plano(estado)
        blocos = estado.get('blocos') or []
        esp = Especificacao.from_dict(estado['especificacao'])
        arquivo = montar_arquivo(esp.titulo, estado['nome_time'], estado['vendedores'],
                                 [b['gobr'] for b in blocos], [b['secao'] for b in blocos])
        return {'arquivo_gobr': arquivo, 'relatorio': relatorio_final(arquivo, plano, blocos, estado['nome_time'])}

    def responder(estado: Estado) -> Estado:
        versoes = list(estado.get('versoes') or [])
        pedido = estado.get('pedido') or ''
        n = len(versoes)
        rotulo = pedido if (pedido and n) else 'versão inicial'
        mensagem = formatar_resposta(estado, conversa=servicos.conversa)
        if n and servicos.conversa:
            mensagem = f'Versão {n} do arquivo (pedido: "{rotulo}"). ' + mensagem
        versoes.append(_foto(estado, n, rotulo))
        return {'mensagens': [mensagem], 'versoes': versoes, 'historico': [{'papel': 'agente', 'texto': mensagem}]}

    def aguardar(estado: Estado) -> Estado:
        resposta = interrupt({'tipo': 'resultado', 'mensagem': estado['mensagens'][-1],
                              'arquivo_gobr': estado.get('arquivo_gobr', '')})
        texto = str(resposta).strip()
        if servicos.conversa:
            return {'resposta_usuario': texto, 'fim': False, 'historico': [{'papel': 'analista', 'texto': texto}]}
        if not texto or re.fullmatch(r'(fim|sair|encerrar|obrigad[oa].*|valeu.*|ok|pronto)', texto, re.I):
            return {'fim': True}
        return {'resposta_usuario': texto, 'fim': False}

    def apos_aguardar(estado: Estado) -> str:
        if servicos.conversa:
            return 'entender'
        return END if estado.get('fim') else 'ajustar'

    def entender(estado: Estado) -> Estado:
        """Classifica a mensagem: regras de palavras primeiro (desfazer, comparar, fim, pergunta, ajuste...); o modelo
        só entra quando a mensagem depende da conversa ("faz a mesma coisa para os inativos")."""
        texto = estado.get('resposta_usuario', '')
        direta = intencao_direta(texto)
        if direta is not None:
            intencao, pedido = direta
        else:
            _etapa(servicos, 'entender')
            intencao, pedido = classificar_mensagem(servicos, estado, texto)
        out: Dict[str, Any] = {'intencao': intencao, 'pedido': pedido}
        if intencao == 'ajuste':
            out.update({'resposta_usuario': pedido, 'rodadas': 0})
        elif intencao == 'aplicar' and estado.get('proposta'):
            out.update({'intencao': 'aplicar_proposta', 'especificacao': estado['proposta'], 'proposta': None,
                        'pedido': estado.get('proposta_pedido', ''), 'rodadas': 0})
        return out

    def apos_entender(estado: Estado) -> str:
        i = estado.get('intencao')
        if i == 'fim':
            return 'memorizar' if servicos.memoria is not None else END
        return {'ajuste': 'ajustar', 'aplicar_proposta': 'revisar'}.get(i, 'conversa')

    def conversa(estado: Estado) -> Estado:
        out, mensagem = tratar_conversa(servicos, estado)
        mensagem += ('\n\nPeça uma mudança, faça uma pergunta, "o que muda se …", "desfazer", "comparar", '
                     '"o que você lembra?" ou "fim".')
        return {**out, 'mensagens': [mensagem], 'historico': [{'papel': 'agente', 'texto': mensagem}]}

    def memorizar(estado: Estado, config: RunnableConfig) -> Estado:
        """Seleção híbrida do que lembrar (livro 4.7.3): o agente propõe, o analista confirma."""
        mem = servicos.memoria
        candidatos = candidatos_a_lembrar(mem, estado)
        if not candidatos:
            return {'fim': True}
        linhas = [f'{n}. {texto}' for n, (_, texto) in enumerate(candidatos, 1)]
        mensagem = ('Antes de encerrar: posso guardar para as próximas sessões\n' + '\n'.join(linhas) +
                    '\nResponda "sim" (tudo), "não", ou os números do que quer guardar (ex.: "1").')
        resposta = str(interrupt({'tipo': 'memoria', 'mensagem': mensagem, 'itens': [t for _, t in candidatos]}))
        if re.match(r'^\s*(n[aã]o|nao|nada|nenhum)', resposta, re.I):
            escolhidos = []
        elif re.search(r'\d', resposta):
            nums = {int(x) for x in re.findall(r'\d+', resposta)}
            escolhidos = [c for n, c in enumerate(candidatos, 1) if n in nums]
        else:
            escolhidos = candidatos
        sessao = ((config or {}).get('configurable') or {}).get('thread_id', '')
        guardados = gravar_lembrancas(mem, estado, escolhidos, sessao)
        final = ('Guardei: ' + '; '.join(guardados) + '.') if guardados else 'Não guardei nada desta sessão.'
        return {'fim': True, 'mensagens': [final],
                'historico': [{'papel': 'agente', 'texto': mensagem}, {'papel': 'analista', 'texto': resposta},
                              {'papel': 'agente', 'texto': final}]}

    def ajustar(estado: Estado) -> Estado:
        _etapa(servicos, 'ajustar')
        esp = Especificacao.from_dict(estado['especificacao'])
        nova = ajustar_especificacao(servicos.backend, esp, estado['resposta_usuario'])
        return {'especificacao': nova.to_dict(), 'rodadas': 0, 'pedido': estado['resposta_usuario'],
                'mensagens': [f'Ajuste pedido: {estado["resposta_usuario"]}']}

    g = StateGraph(Estado)
    for nome, fn in [('ler_entrada', ler_entrada), ('lembrar', lembrar), ('interpretar', no_interpretar),
                     ('revisar', no_revisar), ('perguntar', perguntar), ('incorporar', incorporar),
                     ('planejar', no_planejar), ('redigir_bloco', redigir_bloco), ('verificar_bloco', verificar_bloco),
                     ('montar', montar), ('responder', responder), ('aguardar', aguardar), ('ajustar', ajustar),
                     ('entender', entender), ('conversa', conversa), ('memorizar', memorizar)]:
        g.add_node(nome, fn)
    g.add_edge(START, 'ler_entrada')
    g.add_edge('ler_entrada', 'lembrar')
    g.add_conditional_edges('lembrar', apos_lembrar, ['interpretar', 'ajustar'])
    g.add_edge('interpretar', 'revisar')
    g.add_conditional_edges('revisar', apos_revisar, ['perguntar', 'planejar'])
    g.add_edge('perguntar', 'incorporar')
    g.add_edge('incorporar', 'revisar')
    g.add_conditional_edges('planejar', apos_planejar, ['redigir_bloco', 'montar'])
    g.add_edge('redigir_bloco', 'verificar_bloco')
    g.add_conditional_edges('verificar_bloco', apos_verificar, ['redigir_bloco', 'montar'])
    g.add_edge('montar', 'responder')
    g.add_edge('responder', 'aguardar')
    g.add_conditional_edges('aguardar', apos_aguardar, ['entender', 'ajustar', END])
    g.add_conditional_edges('entender', apos_entender, ['ajustar', 'revisar', 'conversa', 'memorizar', END])
    g.add_edge('conversa', 'aguardar')
    g.add_edge('memorizar', END)
    g.add_edge('ajustar', 'revisar')
    if checkpointer is None:
        from langgraph.checkpoint.memory import InMemorySaver
        checkpointer = InMemorySaver()
    return g.compile(checkpointer=checkpointer)


# ---------------------------------------------------------------- verificação

_FONTE_RE = re.compile(r'^\s*(do time|da carteira|da segmentacao)\s*\(.*\)\s*$', re.I)


def normalizar_bloco(gobr: str, nome: str, nome_time: str) -> str:
    """Nome e fonte de clientes vêm do plano: o modelo escreve as condições e a ação.

    A fonte é sempre o time do arquivo (o modelo costuma deixar `da carteira("<nome>")` como espaço reservado) e o
    nome é o do plano, que já foi tornado único (manual 7.6: nomes distintos).
    """
    linhas = [l.rstrip() for l in gobr.strip().splitlines() if l.strip()]
    cabecalhos = [k for k, l in enumerate(linhas) if re.match(r'^\s*parametros\s+"', l)]
    if len(cabecalhos) > 1:  # mais de um bloco na resposta: fica o primeiro
        linhas = linhas[:cabecalhos[1]]
    corpo = [l.strip() for l in linhas if not re.match(r'^\s*parametros\s+"', l) and not _FONTE_RE.match(l)
             and not l.strip().startswith('#') and not re.match(r'^\s*(version|time\s+")', l)
             and not re.match(r'^\s*vendedores\b', l)]
    if not corpo:
        return ''
    return '\n'.join([f'parametros "{nome}":', f'    do time("{nome_time}")'] + [f'    {l}' for l in corpo])


def verificar_semantica(aceitos: Sequence[str] | str, candidato: str, plano_ate_aqui: Sequence[BlocoPlano],
                        nome_time: str) -> tuple:
    """Compara (blocos aceitos + candidato) com o plano até este bloco, cliente a cliente.

    A referência de cada bloco anterior é o seu molde; um bloco sem molde (condição própria, como curva A) entra na
    referência com o próprio texto aceito, para não contaminar a verificação dos seguintes. Assim, qualquer
    diferença vem do candidato, considerando a ordem (um bloco que pega mais clientes do que o pedido só é problema
    se esses clientes ainda chegarem até ele).

    - bloco do plano sem molde: 'nao_verificavel' (só a conferência de estrutura e catálogo vale);
    - bloco com molde e candidato com cláusula que o simulador não conhece: 'divergente' (o pedido só usa filtros
      conhecidos, então a cláusula estranha está errada ou sobrando).
    """
    if isinstance(aceitos, str):
        aceitos = [a for a in aceitos.split('\n\n') if a.strip()]
    aceitos = list(aceitos)
    alvo = molde(plano_ate_aqui[-1], nome_time)
    if alvo is None:
        return 'nao_verificavel', ''
    obtido = regras_do_texto('\n\n'.join(aceitos + [candidato]))
    if len(obtido) != len(plano_ate_aqui):
        return 'divergente', '- a resposta deve ter exatamente um bloco `parametros`'
    if not obtido[-1].verificavel:
        estranhas = ', '.join(f'"{c}"' for c in obtido[-1].nao_suportado) or 'a ação'
        return 'divergente', (f'- as condições {estranhas} não correspondem ao pedido; use só cláusulas que '
                              'selecionem exatamente os clientes descritos')
    referencia = [molde(b, nome_time) or aceitos[i] for i, b in enumerate(plano_ate_aqui[:-1])] + [alvo]
    regras_ref = regras_do_texto('\n\n'.join(referencia))
    if not all(r.verificavel for r in regras_ref[:-1]):
        # um bloco anterior que o simulador não interpreta esconde quais clientes chegam até este
        return 'nao_verificavel', ''
    cmp = comparar(regras_ref, obtido)
    if cmp.divergencias:
        return 'divergente', '\n'.join(f'- {l}' for l in cmp.resumo(4))
    return 'ok', ''


def dica_de_clausulas(bloco: BlocoPlano) -> str:
    """Na correção, as cláusulas que o manual documenta para os filtros do pedido (seções 6.1, 6.2, 6.3 e 6.7)."""
    from especificacao import CLAUSULA_FILTRO, DESCRICAO_FILTRO
    dicas = [f'- {DESCRICAO_FILTRO[f]}: `{CLAUSULA_FILTRO[f]}`' for f in bloco.filtros]
    if bloco.comprou_nos_ultimos_dias is not None:
        dicas.append("- comprou nos últimos N dias: `recencia de positivacao em N dias`")
    if bloco.sem_comprar_ha_mais_de_dias is not None:
        dicas.append("- está há mais de N dias sem comprar: `fora da recencia de positivacao em N dias`")
    if 'inadimplente' in bloco.nao_filtros:
        dicas.append('- exceto inadimplentes: `adimplentes`')
    return ('Cláusulas do manual para este pedido:\n' + '\n'.join(dicas)) if dicas else ''


def relatorio_final(arquivo: str, plano: Sequence[BlocoPlano], blocos: Sequence[Dict], nome_time: str) -> Dict:
    from catalogo_gobr import carregar_catalogo
    from rag import validar_dsl
    try:
        catalogo = carregar_catalogo()
    except Exception:
        catalogo = None
    validacao = validar_dsl(arquivo, catalogo)
    moldes = [molde(b, nome_time) for b in plano]
    sem = None
    if moldes and all(m is not None for m in moldes):
        cmp = comparar(regras_do_texto('\n\n'.join(moldes)), regras_do_texto(arquivo))
        sem = {'concordancia': cmp.concordancia, 'divergencias': cmp.resumo(5), 'clientes': cmp.total}
    return {'validacao': validacao, 'semantica': sem,
            'fontes': {f: sum(1 for b in blocos if b['fonte'] == f) for f in ('modelo', 'molde')},
            'corrigidos': sum(1 for b in blocos if b.get('tentativas', 1) > 1),
            'reaproveitados': sum(1 for b in blocos if b.get('reaproveitado'))}


def formatar_resposta(estado: Estado, conversa: bool = False) -> str:
    plano = _plano(estado)
    blocos = estado.get('blocos') or []
    rel = estado.get('relatorio') or {}
    partes = ['Regras em GoBR:', '', '```gobr', estado.get('arquivo_gobr', '').rstrip(), '```', '']
    partes.append(explicar_ordem(plano))
    sugeridos = [b.nome for b in plano if b.origem == 'sugestao']
    if sugeridos:
        partes.append('Blocos acrescentados pelas decisões da revisão: ' + '; '.join(f'"{n}"' for n in sugeridos) + '.')
    if estado.get('avisos'):
        partes += ['', 'Pontos de atenção:'] + [f'- {a}' for a in estado['avisos']]
    partes += ['', 'Conferência:']
    ok = [v for v in rel.get('validacao', []) if v['status'] == 'ok']
    partes.append(f'- estrutura e cláusulas (manual + regras reais): {len(ok)}/{len(rel.get("validacao", []))} blocos ok')
    for v in rel.get('validacao', []):
        if v['status'] != 'ok':
            partes.append(f'  - "{v["bloco"]}": {"; ".join(v["problemas"])}')
    sem = rel.get('semantica')
    if sem:
        partes.append(f'- simulação em {sem["clientes"]} clientes sintéticos: {sem["concordancia"]:.1%} das decisões '
                      'iguais às do plano acordado')
        partes += [f'  - {d}' for d in sem['divergencias']]
    f = rel.get('fontes', {})
    partes.append(f'- {f.get("modelo", 0)} blocos escritos pelo modelo com RAG'
                  + (f', {f["molde"]} pelo molde determinístico (o modelo errou duas vezes)' if f.get('molde') else '')
                  + (f'; {rel["corrigidos"]} corrigidos após a verificação' if rel.get('corrigidos') else ''))
    if rel.get('reaproveitados'):
        partes.append(f'- {rel["reaproveitados"]} blocos iguais aos da versão anterior foram reaproveitados '
                      '(e verificados de novo), sem chamar o modelo')
    nao_verif = [b['nome'] for b in blocos if b.get('verificacao') == 'nao_verificado']
    if nao_verif:
        partes.append('- não verificados pela simulação (condições fora do simulador): ' + ', '.join(nao_verif))
    if conversa:
        partes += ['', 'Quer ajustar algo? Peça uma mudança (ex.: "prospects a cada 7 dias"), faça uma pergunta, '
                       '"o que muda se …", "desfazer", "comparar", "o que você lembra?" ou "fim".']
    else:
        partes += ['', 'Quer ajustar algo? Descreva a mudança (ex.: "prospects a cada 7 dias") ou responda "fim".']
    return '\n'.join(partes)


# ---------------------------------------------------------------- texto livre

SCHEMA_RESPOSTAS = {
    'type': 'object',
    'properties': {'respostas': {'type': 'array', 'items': {
        'type': 'object',
        'properties': {'pergunta': {'type': 'integer'}, 'opcao': {'type': ['string', 'null']},
                       'dias': {'type': ['integer', 'null']}},
        'required': ['pergunta', 'opcao', 'dias']}}},
    'required': ['respostas'],
}


def _respostas_livres(backend: Any, texto: str, perguntas: Sequence[Pergunta]) -> Dict[str, Decisao]:
    from llm_json import pedir_json
    system = ('Você converte a resposta livre de um analista em escolhas para perguntas numeradas. Para cada pergunta '
              'que a resposta decide, informe o número da pergunta, a letra da opção escolhida (a, b, c…) e, se o '
              'analista disse um número de dias, os dias. Não invente respostas para perguntas que o texto não decide.')
    usuario = f'<perguntas>\n{formatar_perguntas(perguntas)}\n</perguntas>\n\n<resposta>\n{texto}\n</resposta>'
    try:
        bruto = pedir_json(backend, system, usuario, SCHEMA_RESPOSTAS)
    except Exception:
        return {}
    out: Dict[str, Decisao] = {}
    for r in bruto['respostas']:
        n = r['pergunta'] - 1
        if not 0 <= n < len(perguntas):
            continue
        p = perguntas[n]
        letra = (r.get('opcao') or '').strip().lower()[:1]
        if letra and 0 <= ord(letra) - ord('a') < len(p.opcoes):
            out[p.id] = Decisao(opcao=ord(letra) - ord('a'), texto=texto, explicita=True)
        elif r.get('dias') and p.aceita_numero:
            out[p.id] = Decisao(numero=int(r['dias']), texto=texto, explicita=True)
    return out


def ajustar_especificacao(backend: Any, esp: Especificacao, pedido: str) -> Especificacao:
    """Aplica um pedido de mudança à especificação (o modelo devolve a especificação inteira, já alterada)."""
    import json
    from llm_json import pedir_json
    from especificacao import Item, SYSTEM_INTERPRETAR
    atual = {'titulo': esp.titulo, 'equipe': esp.equipe,
             'itens': [{k: v for k, v in asdict(it).items() if k not in ('texto_original', 'origem')} for it in esp.itens]}
    usuario = (f'Especificação atual:\n{json.dumps(atual, ensure_ascii=False)}\n\nPedido de mudança do analista:\n'
               f'{pedido}\n\nDevolva a especificação inteira com a mudança aplicada. Mantenha igual tudo o que o '
               'pedido não muda. Uma regra nova recebe o próximo número de ramo.')
    bruto = pedir_json(backend, SYSTEM_INTERPRETAR, usuario, SCHEMA_ESPECIFICACAO)
    originais = {it.ramo: it for it in esp.itens}
    nova = Especificacao(bruto.get('titulo') or esp.titulo, bruto.get('equipe') or esp.equipe, esp.nome_time)
    for i in bruto['itens']:
        antigo = originais.get(i['ramo'])
        nova.itens.append(Item(
            nome=i['nome'], acao=i['acao'], ramo=i['ramo'], frequencia_dias=i['frequencia_dias'],
            comprou_nos_ultimos_dias=i['comprou_nos_ultimos_dias'],
            sem_comprar_ha_mais_de_dias=i['sem_comprar_ha_mais_de_dias'], filtros=sorted(set(i['filtros'])),
            exceto=sorted(set(i['exceto'])), outras_condicoes=list(i['outras_condicoes']),
            texto_original=antigo.texto_original if antigo else pedido))
    return nova


# ---------------------------------------------------------------- conversa depois do arquivo (etapa 6)

_FIM = re.compile(r'^\s*(fim|sair|encerrar|encerra|tchau|obrigad[oa]\b.*|valeu.*|ok|okay|pronto|é isso|era isso|'
                  r's[oó] isso)\s*[.!]*\s*$', re.I)
_DESFAZER = re.compile(r'\b(desfa[zç]\w*|volt[ae]\w*\s+(como|ao que|para o que|à vers[aã]o|a vers[aã]o)|'
                       r'vers[aã]o anterior|como estava)', re.I)
_COMPARAR = re.compile(r'\b(compar\w*|o que mudou|mudou o qu[eê]|diferen[cç]as? entre)', re.I)
_MEMORIA = re.compile(r'\bo que (voc[eê] )?(lembra|guardou|tem guardado|sabe sobre mim)\b|\bsua mem[oó]ria\b', re.I)
_ESQUECER = re.compile(r'^\s*(esque[cç]a|esquece|apague|apaga|remova|remove)\b\s*(.*)$', re.I)
_LEMBRAR = re.compile(r'^\s*(lembre|lembra|guarde|guarda|memorize|anote|anota|grave|grava)\b\s*(?:(?:que|de|disso)\b)?'
                      r'\s*(.*)$', re.I)
_APLICAR = re.compile(r'^\s*(aplica|aplique|aplicar|pode aplicar|confirma|confirmo|faz isso|fa[cç]a isso)\b', re.I)
_SIMULAR = re.compile(r'^\s*(?:e\s+)?(?:o que|quem|quantos clientes)\s+(?:muda|mudaria|mudam|mudariam|acontece|'
                      r'aconteceria)\s+se\s+(.*)$|^\s*e se\s+(.*)$|^\s*simul\w*\s*:?\s*(.*)$', re.I)
_PERGUNTA = re.compile(r'\?\s*$|^\s*(por ?qu[eê]|porque|como|qual|quais|quando|onde|quem|o que|explica|explique|'
                       r'me explica)\b', re.I)
_AJUSTE = re.compile(r'(a cada \d+|\d+\s*dias|\b(mud[ae]\w*|troc[ae]\w*|alter[ae]\w*|coloc[ae]\w*|tir[ae]\w*|'
                     r'remov[ae]\w*|inclu[ai]\w*|acrescent[ae]\w*|adicion[ae]\w*|bloque[ie]\w*|n[aã]o agend\w*|'
                     r'passa\w* a|cri[ae]\w*)\b)', re.I)
# referência a algo da conversa: sem o histórico, o pedido é ambíguo (o modelo reescreve com a conversa)
_ANAFORA = re.compile(r'\b(mesm[ao]s?|aquel[ae]s?|daquel[ae]s?|ess[ae]s?|dess[ae]s?|isso|disso|tamb[eé]m|idem|'
                      r'igual (a|à|ao))\b', re.I)


def intencao_direta(texto: str) -> Optional[Tuple[str, str]]:
    """Intenção por regras de palavras, ou None quando a mensagem precisa do histórico para ser entendida."""
    t = (texto or '').strip()
    if not t or _FIM.match(t):
        return 'fim', ''
    m = _ESQUECER.match(t)
    if m:
        return 'esquecer', m.group(2).strip()
    if _MEMORIA.search(t):
        return 'memoria', ''
    m = _LEMBRAR.match(t)
    if m:
        return 'lembrar', (m.group(2) or t).strip()
    if _APLICAR.match(t):
        return 'aplicar', ''
    if _DESFAZER.search(t):
        return 'desfazer', ''
    if _COMPARAR.search(t):
        return 'comparar', ''
    m = _SIMULAR.match(t)
    if m:
        return 'simulacao', next((g for g in m.groups() if g), t).strip().rstrip('?').strip()
    if _ANAFORA.search(t):
        return None
    if _PERGUNTA.search(t):
        return 'pergunta', t
    if _AJUSTE.search(t):
        return 'ajuste', t
    return None


SCHEMA_INTENCAO = {
    'type': 'object',
    'properties': {'intencao': {'type': 'string', 'enum': ['ajuste', 'pergunta', 'simulacao', 'outro']},
                   'pedido': {'type': 'string'}},
    'required': ['intencao', 'pedido'],
}

SYSTEM_INTENCAO = """\
Você acompanha a conversa entre um analista e o agente que escreve regras de parametrização GoBR (Govendas). O \
arquivo de regras já foi gerado. Classifique a última mensagem do analista:
- "ajuste": pede para mudar as regras (frequência, faixa de dias, bloqueio, regra nova ou retirada);
- "pergunta": quer uma explicação sobre o arquivo, a ordem das regras ou o GoBR;
- "simulacao": quer saber o que mudaria se algo fosse diferente, sem aplicar;
- "outro": qualquer outra coisa.
Em "pedido", reescreva a mensagem de forma completa e explícita, trocando referências ("aquela", "a mesma coisa", \
"essa regra", "também") pelo que elas indicam na conversa, com o nome exato da regra da lista. Não invente valores \
que não estejam na mensagem ou na conversa."""

RESERVA_RESPOSTA = 900  # tokens reservados para a resposta do modelo nas chamadas da conversa


def _janela(servicos: Servicos) -> int:
    return int(getattr(servicos.backend, 'num_ctx', 8192))


def _historico_anterior(estado: Estado) -> List[Dict[str, str]]:
    """Histórico sem a última mensagem do analista (ela entra à parte, como o pedido atual)."""
    h = list(estado.get('historico') or [])
    return h[:-1] if h and h[-1]['papel'] == 'analista' else h


def classificar_mensagem(servicos: Servicos, estado: Estado, texto: str) -> Tuple[str, str]:
    from llm_json import pedir_json
    from rag import ErroGeracao
    esp = Especificacao.from_dict(estado['especificacao'])
    fixo = f'<regras>\n{formatar_entendimento(esp)}\n</regras>\n\nÚltima mensagem do analista: {texto}'
    orcamento = _janela(servicos) - estimar_tokens(SYSTEM_INTENCAO + fixo) - 600 - 200
    hist = montar_historico(_historico_anterior(estado), orcamento, compactar=servicos.compactar)
    usuario = f'<conversa>\n{como_transcricao(hist)}\n</conversa>\n\n{fixo}'
    try:
        r = pedir_json(servicos.backend, SYSTEM_INTENCAO, usuario, SCHEMA_INTENCAO)
        return r['intencao'], (r.get('pedido') or texto).strip()
    except ErroGeracao as e:
        return 'outro', f'(não consegui entender: {e})'


SYSTEM_CONVERSA = """\
Você é o agente que escreveu o arquivo de regras GoBR (Govendas) desta conversa e agora responde às perguntas do \
analista sobre ele. Responda em português, em poucas frases, com base no arquivo atual, na explicação da ordem e nos \
trechos do manual abaixo. Regra central do GoBR: cada cliente recebe a ação da primeira regra que o pega; regras \
seguintes não o reprocessam (manual 7.6). Se a resposta não estiver nessas fontes nem na conversa, diga que não sabe."""


def responder_pergunta(servicos: Servicos, estado: Estado, pergunta: str) -> str:
    from rag import ErroGeracao
    esp = Especificacao.from_dict(estado['especificacao'])
    try:
        trechos = servicos.recuperador.recuperar(pergunta, 0, 2).trechos
    except Exception:
        trechos = []
    manual = '\n\n'.join(f'[manual {t.secao} {t.titulo}]\n{t.texto[:1500]}' for t in trechos)
    system = (f'{SYSTEM_CONVERSA}\n\n<arquivo_atual>\n{estado.get("arquivo_gobr", "")}\n</arquivo_atual>\n\n'
              f'<regras>\n{formatar_entendimento(esp)}\n</regras>\n\n<ordem>\n{explicar_ordem(_plano(estado))}\n'
              f'</ordem>\n\n<manual>\n{manual}\n</manual>')
    orcamento = _janela(servicos) - estimar_tokens(system + pergunta) - RESERVA_RESPOSTA - 200
    hist = montar_historico(_historico_anterior(estado), orcamento, compactar=servicos.compactar)
    mensagens = hist.mensagens + [{'role': 'user', 'content': pergunta}]
    if len(mensagens) >= 2 and mensagens[-2]['role'] == 'user':
        mensagens = mensagens[:-2] + [{'role': 'user', 'content': mensagens[-2]['content'] + '\n\n' + pergunta}]
    _etapa(servicos, 'responder_pergunta')
    antes = getattr(servicos.backend, 'max_tokens', None)
    try:
        if antes is not None:
            servicos.backend.max_tokens = RESERVA_RESPOSTA
        return servicos.backend.completar(system, mensagens).texto.strip()
    except ErroGeracao as e:
        return f'Não consegui responder: {e}'
    finally:
        if antes is not None:
            servicos.backend.max_tokens = antes


def _rotulo_simulacao(linha: str) -> str:
    return linha.replace(': esperado ', ': hoje ').replace(', obtido ', ', com a mudança ')


def simular_mudanca(servicos: Servicos, estado: Estado, pedido: str) -> Tuple[str, Optional[Dict[str, Any]]]:
    """"O que muda se ...": aplica a mudança numa cópia da especificação, monta o plano com os moldes e compara com o
    arquivo atual no simulador. A resposta é a diferença de decisões, não uma opinião do modelo; nada é aplicado."""
    from rag import ErroGeracao
    _etapa(servicos, 'simular')
    esp = Especificacao.from_dict(estado['especificacao'])
    try:
        nova = ajustar_especificacao(servicos.backend, esp, pedido)
    except ErroGeracao as e:
        return f'Não consegui simular: {e}', None
    decisoes = _decisoes(estado)
    rev = revisar(nova, decisoes)
    pendentes = aplicar_sugestoes(rev.perguntas, decisoes)
    plano, nome_time, _, _ = planejar(nova, decisoes)
    moldes = [molde(b, nome_time) for b in plano]
    if not plano or any(m is None for m in moldes):
        sem = [b.nome for b, m in zip(plano, moldes) if m is None]
        return ('Não consigo simular essa mudança com exatidão: ' +
                (f'as regras {", ".join(sem)} têm condições fora do simulador.' if sem else 'o plano ficou vazio.'),
                nova.to_dict())
    cmp = comparar(regras_do_texto(estado.get('arquivo_gobr', '')), regras_do_texto('\n\n'.join(moldes)))
    mudam = len(cmp.divergencias)
    if not mudam:
        texto = (f'Simulei "{pedido}" em {cmp.total} clientes sintéticos: nenhum muda de decisão em relação ao arquivo '
                 'atual.')
    else:
        texto = (f'Simulei "{pedido}" em {cmp.total} clientes sintéticos: {mudam} ({mudam / cmp.total:.1%}) mudariam '
                 'de decisão:\n' + '\n'.join(f'- {_rotulo_simulacao(l)}' for l in cmp.resumo(6)))
    if pendentes:
        texto += '\nA mudança abriria perguntas sem resposta segura; elas aparecem se você aplicar.'
    return texto + '\nNada foi aplicado. Para aplicar, responda "aplica".', nova.to_dict()


def desfazer_versao(estado: Estado) -> Tuple[Dict[str, Any], str]:
    versoes = list(estado.get('versoes') or [])
    if len(versoes) < 2:
        return {}, 'Não há versão anterior para voltar: este é o primeiro arquivo da sessão.'
    atual, alvo = versoes[-1], versoes[-2]
    nova = {**alvo, 'n': len(versoes), 'pedido': f'desfazer (volta à versão {alvo["n"]})'}
    mudancas = {**{k: alvo.get(k) for k in CAMPOS_VERSAO}, 'versoes': versoes + [nova], 'proposta': None}
    mensagem = (f'Voltei à versão {alvo["n"]} ("{alvo["pedido"]}"), desfazendo "{atual["pedido"]}". Esta é a versão '
                f'{nova["n"]}:\n\n```gobr\n{(alvo.get("arquivo_gobr") or "").rstrip()}\n```')
    return mudancas, mensagem


def comparar_versoes(estado: Estado, a: Optional[int] = None, b: Optional[int] = None) -> str:
    versoes = list(estado.get('versoes') or [])
    if len(versoes) < 2:
        return 'Só existe uma versão do arquivo nesta sessão; não há o que comparar.'
    va, vb = versoes[-2 if a is None else a], versoes[-1 if b is None else b]
    blocos_a = {x['nome']: x['gobr'] for x in va.get('blocos') or []}
    blocos_b = {x['nome']: x['gobr'] for x in vb.get('blocos') or []}
    linhas = [f'Versão {va["n"]} ("{va["pedido"]}") × versão {vb["n"]} ("{vb["pedido"]}"):']
    for nome in blocos_b:
        if nome not in blocos_a:
            linhas.append(f'- regra nova: "{nome}"')
        elif blocos_a[nome] != blocos_b[nome]:
            linhas.append(f'- regra alterada: "{nome}"')
    linhas += [f'- regra retirada: "{nome}"' for nome in blocos_a if nome not in blocos_b]
    cmp = comparar(regras_do_texto(va.get('arquivo_gobr') or ''), regras_do_texto(vb.get('arquivo_gobr') or ''))
    if cmp.divergencias:
        linhas.append(f'Efeito em {cmp.total} clientes sintéticos: {len(cmp.divergencias)} mudam de decisão:')
        linhas += [f'  - {l.replace(": esperado ", ": antes ").replace(", obtido ", ", depois ")}' for l in cmp.resumo(6)]
    else:
        linhas.append(f'Efeito em {cmp.total} clientes sintéticos: nenhum muda de decisão.')
    return '\n'.join(linhas)


def tratar_conversa(servicos: Servicos, estado: Estado) -> Tuple[Dict[str, Any], str]:
    intencao, pedido = estado.get('intencao', 'outro'), estado.get('pedido', '')
    mem = servicos.memoria
    if intencao == 'pergunta':
        return {}, responder_pergunta(servicos, estado, pedido)
    if intencao == 'simulacao':
        texto, proposta = simular_mudanca(servicos, estado, pedido)
        return {'proposta': proposta, 'proposta_pedido': pedido}, texto
    if intencao == 'desfazer':
        return desfazer_versao(estado)
    if intencao == 'comparar':
        return {}, comparar_versoes(estado)
    if intencao in ('lembrar', 'esquecer', 'memoria') and mem is None:
        return {}, 'Esta sessão está sem memória de longo prazo (opção --sem-memoria): não guardo nada entre sessões.'
    if intencao == 'lembrar':
        pref = preferencia_do_texto(pedido)
        if pref:
            texto = mem.lembrar_preferencia(pref[0], pref[1], origem='a seu pedido')
            return {}, (f'Guardei a preferência: {texto}. Nas próximas sessões, quando essa pergunta aparecer, ela '
                        'vem com esta sugestão (você ainda confirma). Para mudar o arquivo atual, peça o ajuste.')
        mem.lembrar_nota(pedido)
        return {}, f'Guardei a nota: "{pedido}".'
    if intencao == 'esquecer':
        apagados = mem.esquecer(pedido)
        return {}, ('Esqueci ' + '; '.join(apagados) + '.') if apagados else \
            f'Não encontrei nada sobre "{pedido}" na memória. Pergunte "o que você lembra?" para ver o que está guardado.'
    if intencao == 'memoria':
        return {}, mem.descrever()
    if intencao == 'aplicar':
        return {}, 'Não há simulação pendente para aplicar. Para mudar o arquivo, descreva a mudança.'
    return {}, ('Não entendi o pedido. ' + (pedido if pedido.startswith('(não consegui') else ''))


def candidatos_a_lembrar(mem: Any, estado: Estado) -> List[Tuple[str, str]]:
    """O que vale a pena lembrar desta sessão: a empresa (arquivo aprovado + decisões) e as preferências que o
    analista escolheu explicitamente e que ainda não estão guardadas."""
    if mem is None or not estado.get('arquivo_gobr'):
        return []
    esp = Especificacao.from_dict(estado['especificacao'])
    chave = estado.get('empresa') or chave_empresa(esp.titulo)
    decisoes = estado.get('decisoes') or {}
    out: List[Tuple[str, str]] = []
    if chave:
        out.append(('empresa', f'o arquivo aprovado de "{esp.titulo}" ({len(estado.get("blocos") or [])} blocos) e as '
                               f'{len(decisoes)} decisões desta conversa, para partir deles numa próxima sessão'))
    prefs = mem.preferencias()
    for pid in PREFERENCIAS:
        d = decisoes.get(pid) or {}
        if d.get('explicita') and d.get('opcao') is not None and (prefs.get(pid) or {}).get('opcao') != d['opcao']:
            out.append((f'pref:{pid}', f'sua preferência para todas as empresas: {OPCOES_PREFERENCIA[pid][d["opcao"]]}'))
    return out


def gravar_lembrancas(mem: Any, estado: Estado, escolhidos: Sequence[Tuple[str, str]], sessao: str) -> List[str]:
    esp = Especificacao.from_dict(estado['especificacao'])
    guardados = []
    for tipo, texto in escolhidos:
        if tipo == 'empresa':
            chave = estado.get('empresa') or chave_empresa(esp.titulo)
            pedidos = [h['texto'][:160] for h in estado.get('historico') or [] if h['papel'] == 'analista'][1:]
            mem.lembrar_empresa(chave, {'titulo': esp.titulo, 'data': agora(), 'sessao': sessao,
                                        'versao': _foto(estado, 0, 'aprovado'), 'pedidos': pedidos[:20]})
            guardados.append(f'"{esp.titulo}" (arquivo e decisões)')
        elif tipo.startswith('pref:'):
            pid = tipo.split(':', 1)[1]
            d = (estado.get('decisoes') or {}).get(pid) or {}
            guardados.append(mem.lembrar_preferencia(pid, d['opcao'], origem=f'escolhida em "{esp.titulo}"'))
    return guardados


# ---------------------------------------------------------------- montagem dos serviços e linha de comando

def criar_servicos(backend_nome: str = 'ollama', modelo: Optional[str] = None, memoria: Any = None,
                   conversa: bool = True, compactar: bool = True) -> Servicos:
    from catalogo_gobr import carregar_catalogo
    from rag import Gerador, carregar_recuperador, criar_backend
    backend = criar_backend(backend_nome, modelo)
    if backend_nome == 'ollama':
        backend.max_tokens = 4096  # a especificação de um mapa com ~10 ramos passa de 2 mil tokens
    # uma tentativa no Gerador: a correção fica com verificar_bloco, que manda ao modelo as divergências concretas
    return Servicos(backend, carregar_recuperador(), Gerador(backend, carregar_catalogo(), max_tentativas=1),
                    memoria=memoria, conversa=conversa, compactar=compactar)


def abrir_memoria(pasta: Path, analista: str = 'analista') -> Tuple[Any, Any]:
    """Checkpointer das sessões (curto prazo) e memória de longo prazo, cada um num arquivo SQLite da pasta."""
    import sqlite3
    from langgraph.checkpoint.sqlite import SqliteSaver
    from langgraph.store.sqlite import SqliteStore
    from memoria import MemoriaLonga
    pasta.mkdir(parents=True, exist_ok=True)
    saver = SqliteSaver(sqlite3.connect(str(pasta / 'sessoes.sqlite'), check_same_thread=False))
    store = SqliteStore(sqlite3.connect(str(pasta / 'memoria.sqlite'), check_same_thread=False, isolation_level=None))
    store.setup()
    return saver, MemoriaLonga(store, analista)


def pendencias(grafo, thread: str) -> List[Any]:
    """Interrupções pendentes de uma sessão salva (o grafo parou esperando o analista)."""
    snap = grafo.get_state({'configurable': {'thread_id': thread}})
    return [i for t in snap.tasks for i in t.interrupts] if snap.next else []


def conversar(grafo, entrada: Optional[str], respostas: Optional[List[str]] = None, thread: str = 'sessao',
              saida=print, ler=input) -> Dict[str, Any]:
    """Roda a conversa. Com `respostas`, elas são usadas em ordem no lugar do teclado (execução roteirizada).

    Se a sessão `thread` parou no meio (programa fechado com uma pergunta pendente), continua de onde parou: o
    checkpointer devolve o estado e a pergunta pendente, sem refazer o que já foi feito.
    """
    from langgraph.types import Command
    config = {'configurable': {'thread_id': thread}, 'recursion_limit': 300}
    fila = list(respostas or [])
    pendentes = pendencias(grafo, thread)
    if pendentes:
        saida(f'(retomando a sessão "{thread}" de onde ela parou)')
        resultado: Dict[str, Any] = {'__interrupt__': pendentes}
    else:
        if entrada is None:
            raise ValueError(f'a sessão "{thread}" não tem nada pendente; informe uma entrada para começar')
        resultado = grafo.invoke({'entrada': entrada}, config)
    mostrada = None
    while '__interrupt__' in resultado:
        pedido = resultado['__interrupt__'][0].value
        mostrada = pedido['mensagem']
        saida('\n' + mostrada + '\n')
        if respostas is not None:
            resposta = fila.pop(0) if fila else 'fim'
            saida(f'> {resposta}')
        else:
            resposta = ler('> ')
        resultado = grafo.invoke(Command(resume=resposta), config)
    final = (resultado.get('mensagens') or [None])[-1]
    if final and final != mostrada and final.startswith(('Guardei', 'Não guardei')):
        saida('\n' + final)
    return resultado


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse
    from rag import BACKENDS, ErroGeracao
    ap = argparse.ArgumentParser(description='Agente conversacional que escreve regras GoBR a partir da descrição '
                                             '(texto, imagem ou PDF) das regras de negócio.')
    ap.add_argument('entrada', nargs='?', help='Descrição das regras ou caminho de uma imagem/PDF '
                                               '(sem argumento, pergunta no terminal)')
    ap.add_argument('--backend', default='ollama', choices=BACKENDS,
                    help='ollama: modelo local e gratuito (padrão); anthropic: Claude pela API, pago')
    ap.add_argument('--modelo', help='Modelo do backend (padrão: qwen2.5:7b no Ollama)')
    ap.add_argument('--respostas', nargs='*', help='Respostas roteirizadas, em ordem (ex.: --respostas ok fim)')
    ap.add_argument('--salvar', type=Path, help='Salva o arquivo GoBR final neste caminho')
    ap.add_argument('--sessao', help='Id da sessão: o mesmo id retoma uma sessão interrompida (padrão: um id novo)')
    ap.add_argument('--memoria', type=Path, default=Path('memoria'),
                    help='Pasta dos bancos SQLite de sessões e de memória de longo prazo (padrão: memoria/)')
    ap.add_argument('--analista', default='analista', help='Quem está usando (as preferências são por analista)')
    ap.add_argument('--sem-memoria', action='store_true',
                    help='Comportamento da etapa 5: sessão só na RAM, sem memória entre sessões nem conversa')
    ap.add_argument('--sem-compactacao', action='store_true', help='Histórico inteiro nas chamadas ao modelo')
    args = ap.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    from datetime import datetime
    sessao = args.sessao or f'sessao-{datetime.now():%Y%m%d-%H%M%S}'
    if args.sem_memoria:
        checkpointer, memoria = None, None
    else:
        checkpointer, memoria = abrir_memoria(args.memoria, args.analista)
    print('Carregando os índices e o modelo…')
    try:
        grafo = criar_grafo(criar_servicos(args.backend, args.modelo, memoria=memoria, conversa=not args.sem_memoria,
                                           compactar=not args.sem_compactacao), checkpointer)
        entrada = args.entrada
        if not pendencias(grafo, sessao) and not entrada:
            entrada = input('Descreva as regras de negócio (ou informe o caminho de uma imagem/PDF):\n> ')
        print(f'Sessão: {sessao} (para retomar depois: --sessao {sessao})')
        resultado = conversar(grafo, entrada, args.respostas, thread=sessao)
    except ErroGeracao as e:
        print(f'erro: {e}')
        return 1
    if args.salvar and resultado.get('arquivo_gobr'):
        args.salvar.write_text(resultado['arquivo_gobr'], encoding='utf-8')
        print(f'\nArquivo salvo em {args.salvar}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
