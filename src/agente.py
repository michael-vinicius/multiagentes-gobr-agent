"""Agente conversacional GoBR: da descrição (texto, imagem ou PDF) ao arquivo de regras, com um fluxo LangGraph.

    ler_entrada ─→ interpretar ─→ revisar ──(perguntas)──→ perguntar ⇄ analista ─→ incorporar ─┐
                                    ↑  └──(sem perguntas)─→ planejar                           │
                                    └──────────────────────────────────────────────────────────┘
    planejar ─→ redigir_bloco ─→ verificar_bloco ──(divergiu: corrigir)──→ redigir_bloco
                     ↑                  ├──(ok: próximo bloco)───────────────┘
                     │                  └──(todos)──→ montar ─→ responder ─→ aguardar ⇄ analista
                     │                                                          ├─(ajuste)─→ ajustar ─→ revisar
                     └──────────────────────────────────────────────────────────└─(fim)───→ END

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
- ajustar (modelo, JSON): pedidos de mudança depois da resposta ("prospects a cada 7 dias") editam a especificação.
"""
from __future__ import annotations

import operator
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Annotated, Any, Dict, List, Optional, Sequence, TypedDict

from especificacao import (BlocoPlano, Especificacao, SCHEMA_ESPECIFICACAO, interpretar, molde, montar_arquivo,
                           numerar_descricao)
from lacunas import (Decisao, Pergunta, aplicar_sugestoes, explicar_ordem, interpretar_respostas, planejar, revisar)
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


@dataclass
class Servicos:
    """Dependências do grafo (o modelo, o RAG e o catálogo), injetadas para que os testes usem dublês."""
    backend: Any
    recuperador: Any
    gerador: Any
    transcrever: Any = None
    k_exemplos: int = 4
    k_manual: int = 3


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
            return {'descricao': t.como_texto(), 'origem': t.origem,
                    'mensagens': [f'Li o arquivo {arquivo.name} ({"camada de texto do PDF" if t.origem == "pdf-texto" else "OCR local"}).']}
        return {'descricao': numerar_descricao(entrada), 'origem': 'texto', 'mensagens': []}

    def no_interpretar(estado: Estado) -> Estado:
        esp = interpretar(servicos.backend, estado['descricao'])
        return {'especificacao': esp.to_dict(), 'decisoes': estado.get('decisoes') or {}, 'rodadas': 0}

    def no_revisar(estado: Estado) -> Estado:
        esp = Especificacao.from_dict(estado['especificacao'])
        rev = revisar(esp, _decisoes(estado))
        return {'perguntas': [p.to_dict() for p in rev.perguntas], 'avisos': rev.avisos}

    def apos_revisar(estado: Estado) -> str:
        if estado.get('perguntas') and estado.get('rodadas', 0) < MAX_RODADAS_PERGUNTAS:
            return 'perguntar'
        return 'planejar'

    def perguntar(estado: Estado) -> Estado:
        esp = Especificacao.from_dict(estado['especificacao'])
        partes = []
        if estado.get('rodadas', 0) == 0:
            if estado.get('origem') in ('ocr', 'pdf-texto'):
                partes += ['Transcrição do arquivo (confira se está fiel):', estado['descricao'], '']
            partes += ['Entendi assim:', formatar_entendimento(esp), '']
            if estado.get('avisos'):
                partes += ['Pontos de atenção:'] + [f'- {a}' for a in estado['avisos']] + ['']
        partes += ['Antes de escrever as regras, preciso decidir:', formatar_perguntas(_perguntas(estado)), '',
                   'Responda por número e letra (ex.: "1a, 2b, 3: 21 dias"), escreva livremente, ou "ok" para usar as '
                   'sugestões.']
        mensagem = '\n'.join(partes)
        resposta = interrupt({'tipo': 'perguntas', 'mensagem': mensagem, 'perguntas': estado['perguntas']})
        return {'resposta_usuario': str(resposta), 'mensagens': [mensagem]}

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
            blocos.append({**cand, 'nome': bloco.nome, 'secao': bloco.secao, 'fonte': 'modelo',
                           'verificacao': status, 'tentativas': tentativa})
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
        mensagem = formatar_resposta(estado)
        return {'mensagens': [mensagem]}

    def aguardar(estado: Estado) -> Estado:
        resposta = interrupt({'tipo': 'resultado', 'mensagem': estado['mensagens'][-1],
                              'arquivo_gobr': estado.get('arquivo_gobr', '')})
        texto = str(resposta).strip()
        if not texto or re.fullmatch(r'(fim|sair|encerrar|obrigad[oa].*|valeu.*|ok|pronto)', texto, re.I):
            return {'fim': True}
        return {'resposta_usuario': texto, 'fim': False}

    def apos_aguardar(estado: Estado) -> str:
        return END if estado.get('fim') else 'ajustar'

    def ajustar(estado: Estado) -> Estado:
        esp = Especificacao.from_dict(estado['especificacao'])
        nova = ajustar_especificacao(servicos.backend, esp, estado['resposta_usuario'])
        return {'especificacao': nova.to_dict(), 'rodadas': 0,
                'mensagens': [f'Ajuste pedido: {estado["resposta_usuario"]}']}

    g = StateGraph(Estado)
    for nome, fn in [('ler_entrada', ler_entrada), ('interpretar', no_interpretar), ('revisar', no_revisar),
                     ('perguntar', perguntar), ('incorporar', incorporar), ('planejar', no_planejar),
                     ('redigir_bloco', redigir_bloco), ('verificar_bloco', verificar_bloco), ('montar', montar),
                     ('responder', responder), ('aguardar', aguardar), ('ajustar', ajustar)]:
        g.add_node(nome, fn)
    g.add_edge(START, 'ler_entrada')
    g.add_edge('ler_entrada', 'interpretar')
    g.add_edge('interpretar', 'revisar')
    g.add_conditional_edges('revisar', apos_revisar, ['perguntar', 'planejar'])
    g.add_edge('perguntar', 'incorporar')
    g.add_edge('incorporar', 'revisar')
    g.add_conditional_edges('planejar', apos_planejar, ['redigir_bloco', 'montar'])
    g.add_edge('redigir_bloco', 'verificar_bloco')
    g.add_conditional_edges('verificar_bloco', apos_verificar, ['redigir_bloco', 'montar'])
    g.add_edge('montar', 'responder')
    g.add_edge('responder', 'aguardar')
    g.add_conditional_edges('aguardar', apos_aguardar, ['ajustar', END])
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
        dicas.append(f'- comprou nos últimos N dias: `recencia de positivacao em N dias`')
    if bloco.sem_comprar_ha_mais_de_dias is not None:
        dicas.append(f'- está há mais de N dias sem comprar: `fora da recencia de positivacao em N dias`')
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
            'corrigidos': sum(1 for b in blocos if b.get('tentativas', 1) > 1)}


def formatar_resposta(estado: Estado) -> str:
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
    nao_verif = [b['nome'] for b in blocos if b.get('verificacao') == 'nao_verificado']
    if nao_verif:
        partes.append('- não verificados pela simulação (condições fora do simulador): ' + ', '.join(nao_verif))
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
            out[p.id] = Decisao(opcao=ord(letra) - ord('a'), texto=texto)
        elif r.get('dias') and p.aceita_numero:
            out[p.id] = Decisao(numero=int(r['dias']), texto=texto)
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


# ---------------------------------------------------------------- montagem dos serviços e linha de comando

def criar_servicos(backend_nome: str = 'ollama', modelo: Optional[str] = None) -> Servicos:
    from catalogo_gobr import carregar_catalogo
    from rag import Gerador, carregar_recuperador, criar_backend
    backend = criar_backend(backend_nome, modelo)
    if backend_nome == 'ollama':
        backend.max_tokens = 4096  # a especificação de um mapa com ~10 ramos passa de 2 mil tokens
    # uma tentativa no Gerador: a correção fica com verificar_bloco, que manda ao modelo as divergências concretas
    return Servicos(backend, carregar_recuperador(), Gerador(backend, carregar_catalogo(), max_tentativas=1))


def conversar(grafo, entrada: str, respostas: Optional[List[str]] = None, thread: str = 'sessao',
              saida=print, ler=input) -> Dict[str, Any]:
    """Roda a conversa. Com `respostas`, elas são usadas em ordem no lugar do teclado (execução roteirizada)."""
    from langgraph.types import Command
    config = {'configurable': {'thread_id': thread}, 'recursion_limit': 200}
    fila = list(respostas or [])
    resultado = grafo.invoke({'entrada': entrada}, config)
    while '__interrupt__' in resultado:
        pedido = resultado['__interrupt__'][0].value
        saida('\n' + pedido['mensagem'] + '\n')
        if respostas is not None:
            resposta = fila.pop(0) if fila else 'fim'
            saida(f'> {resposta}')
        else:
            resposta = ler('> ')
        resultado = grafo.invoke(Command(resume=resposta), config)
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
    args = ap.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    entrada = args.entrada or input('Descreva as regras de negócio (ou informe o caminho de uma imagem/PDF):\n> ')
    print('Carregando os índices e o modelo…')
    try:
        grafo = criar_grafo(criar_servicos(args.backend, args.modelo))
        resultado = conversar(grafo, entrada, args.respostas)
    except ErroGeracao as e:
        print(f'erro: {e}')
        return 1
    if args.salvar and resultado.get('arquivo_gobr'):
        args.salvar.write_text(resultado['arquivo_gobr'], encoding='utf-8')
        print(f'\nArquivo salvo em {args.salvar}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
