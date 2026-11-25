"""Revisão comercial da especificação: encontra pontos falhos e monta as perguntas ao analista.

É a parte proativa do agente. As verificações são determinísticas, a partir da especificação estruturada, e cada uma
explica o motivo com base no manual ou nas regras reais:

| Verificação | O que acusa |
|---|---|
| equipe | a descrição não diz quem atende (televendas, campo) e o arquivo precisa de um time (manual, seção 10) |
| frequência | regra de agendamento sem frequência |
| cobertura das faixas | intervalos de dias sem compra que nenhuma regra cobre, ou faixas que se sobrepõem |
| acima da última faixa | clientes mais antigos que a maior faixa ficam sem regra (falta a regra final) |
| prospects | clientes que nunca compraram não caem em nenhuma regra de recência |
| exceções repetidas | "somente clientes fora da rota" repetido em todos os ramos vira um bloqueio único no início |
| baixados na Receita | bloqueio comum nas regras reais que a descrição não menciona |
| inadimplentes | a descrição não diz o que fazer com eles |
| agendar | "agendar X" já é o comportamento padrão; conflito se outro ramo bloqueia X |
| fora do escopo | itens que não são parametrização (meta, capacidade de atendimento) não entram no arquivo |
| prioridade | regra com condição própria (curva A, ramo…) que se sobrepõe às regras de recência |

Depois das respostas, `planejar()` monta os blocos na ordem em que o GoBR os aplica: a 1ª regra que pega o cliente
vale (manual 7.6), então bloqueios primeiro, depois prospects e regras com condição própria, as faixas de recência
da mais recente para a mais antiga e, por último, a regra final.
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

from especificacao import (BlocoPlano, DESCRICAO_FILTRO, Especificacao, Item, NOME_TIME_PADRAO,
                           VENDEDORES_POR_EQUIPE, nomes_unicos)

INFINITO = 10 ** 6
# bloqueio de baixados na Receita: 35 regras reais usam `quando status na receita federal definido como baixada`
REGRAS_REAIS_BAIXADOS = 35


@dataclass
class Pergunta:
    id: str
    texto: str
    opcoes: List[str]
    sugestao: Optional[int]  # índice da opção sugerida; None quando só o analista sabe a resposta
    motivo: str = ''
    aceita_numero: bool = False  # a resposta pode ser um número de dias digitado

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Revisao:
    perguntas: List[Pergunta] = field(default_factory=list)
    avisos: List[str] = field(default_factory=list)


@dataclass
class Decisao:
    opcao: Optional[int] = None
    numero: Optional[int] = None
    texto: str = ''
    explicita: bool = False  # o analista respondeu (e não só aceitou a sugestão): candidata a preferência lembrada


# ---------------------------------------------------------------- utilidades das faixas

def faixa(it: Item) -> Tuple[int, int]:
    """Intervalo (a, b] de dias sem compra coberto pelo item (a exclusivo, b inclusivo)."""
    a = it.sem_comprar_ha_mais_de_dias if it.sem_comprar_ha_mais_de_dias is not None else -1
    b = it.comprou_nos_ultimos_dias if it.comprou_nos_ultimos_dias is not None else INFINITO
    return a, b


def _txt_faixa(a: int, b: int) -> str:
    if b >= INFINITO:
        return f'mais de {a} dias sem comprar'
    if a < 0:
        return f'até {b} dias sem comprar'
    return f'de {a + 1} a {b} dias sem comprar'


def _itens_de_recencia(esp: Especificacao) -> List[Item]:
    return [it for it in esp.itens if it.acao in ('frequencia', 'nao_agendar') and it.tem_recencia
            and not it.filtros and not it.outras_condicoes]


def _itens_agendamento(esp: Especificacao) -> List[Item]:
    return [it for it in esp.itens if it.acao == 'frequencia']


def _regra_final(esp: Especificacao) -> Optional[Item]:
    """Item sem condição nenhuma (pega todos os que sobraram)."""
    for it in esp.itens:
        if it.acao in ('frequencia', 'nao_agendar') and not it.tem_recencia and not it.filtros \
                and not it.outras_condicoes:
            return it
    return None


# ---------------------------------------------------------------- revisão

def revisar(esp: Especificacao, decisoes: Dict[str, Decisao]) -> Revisao:
    """Perguntas ainda sem decisão e avisos. Perguntas já decididas não voltam."""
    rev = Revisao(avisos=list(esp.avisos))
    perguntas: List[Pergunta] = []

    # equipe
    if esp.equipe == 'nao_informado':
        perguntas.append(Pergunta(
            'equipe', 'A descrição não diz quem faz o atendimento. Para qual equipe são as regras?',
            ['televendas (vendedores todostelevendas)', 'campo (vendedores todosdecampo)', 'todos os vendedores'], 0,
            'todo arquivo GoBR precisa definir pelo menos um time (manual, seção 10); as regras de frequência por '
            'recência dos exemplos são de televendas'))

    # frequência ausente
    for idx, it in enumerate(esp.itens):
        if it.acao == 'frequencia' and not it.frequencia_dias:
            perguntas.append(Pergunta(
                f'frequencia:{idx}', f'A regra "{it.nome}" não informa a frequência de atendimento. De quantos em '
                f'quantos dias esses clientes devem ser atendidos?',
                ['7 dias', '14 dias', '28 dias', 'não criar esta regra'], None,
                'regra de agendamento sem frequência não pode ser escrita', aceita_numero=True))

    # agendar / fora do escopo
    bloqueados = {f for it in esp.itens if it.acao == 'nao_agendar' for f in it.filtros}
    for idx, it in enumerate(esp.itens):
        if it.acao == 'fora_do_escopo':
            rev.avisos.append(f'"{it.nome}" não é uma regra de parametrização (quem agendar e com que frequência); '
                              'o manual não tem cláusula de `parametros` para isso, então fica fora do arquivo')
        elif it.acao == 'agendar':
            conflito = [DESCRICAO_FILTRO[f] for f in it.filtros if f in bloqueados]
            if conflito:
                perguntas.append(Pergunta(
                    f'conflito:{idx}', f'"{it.nome}" pede para agendar {", ".join(conflito)}, mas outro ramo bloqueia '
                    'esses clientes. Qual vale?', ['bloquear (não agendar)', 'agendar normalmente'], None,
                    'as duas instruções se contradizem'))
            else:
                rev.avisos.append(f'"{it.nome}": agendar é o comportamento padrão quando nenhum bloqueio pega o '
                                  'cliente; basta não criar bloqueio para eles, então não há bloco para este ramo')

    # exceções repetidas → bloqueio único
    agendamento = _itens_agendamento(esp)
    for f in sorted({f for it in agendamento for f in it.exceto}):
        com = [it for it in agendamento if f in it.exceto]
        if f in bloqueados:
            rev.avisos.append(f'a exceção "{DESCRICAO_FILTRO[f]}" já é coberta pelo bloqueio explícito, que vem antes '
                              'das regras de agendamento; não precisa repetir em cada regra')
        elif len(com) == len(agendamento) and len(com) >= 2:
            perguntas.append(Pergunta(
                f'excecao:{f}', f'Todas as regras de agendamento excluem {DESCRICAO_FILTRO[f]}. Posso trocar a '
                'exceção repetida por um bloqueio único no início do arquivo?',
                ['sim, criar um bloqueio "não agendar" no início', 'não, manter só como exceção de cada regra'], 0,
                'um bloqueio no início tem o mesmo efeito para as regras de agendamento (a 1ª regra que pega o '
                'cliente vale, manual 7.6), é mais simples de manter e deixa explícito o que acontece com eles'))

    # baixados na Receita
    if 'baixado_receita' not in bloqueados:
        perguntas.append(Pergunta(
            'baixados', 'A descrição não fala de clientes baixados na Receita Federal. Devo bloquear o agendamento '
            'deles?', ['sim, não agendar baixados na Receita', 'não'], 0,
            f'empresa baixada não compra; esse bloqueio aparece em {REGRAS_REAIS_BAIXADOS} regras reais e '
            'nos três exemplos de referência'))

    # inadimplentes
    mencionado = any('inadimplente' in it.filtros + it.exceto for it in esp.itens)
    if not mencionado:
        perguntas.append(Pergunta(
            'inadimplentes', 'A descrição não diz o que fazer com clientes inadimplentes. Como tratá-los?',
            ['agendar normalmente (padrão do sistema)', 'não agendar inadimplentes'], 0,
            'muitas empresas bloqueiam inadimplentes; sem regra, eles seguem as regras de recência como os demais'))

    # cobertura das faixas
    final = _regra_final(esp)
    rec = sorted(_itens_de_recencia(esp), key=lambda it: (faixa(it)[1], faixa(it)[0]))
    if rec:
        intervalos = [faixa(it) for it in rec]
        for (a1, b1), (a2, b2), i1, i2 in zip(intervalos, intervalos[1:], rec, rec[1:]):
            if a2 < b1:
                perguntas.append(Pergunta(
                    f'sobreposicao:{esp.itens.index(i1)}:{esp.itens.index(i2)}',
                    f'As faixas de "{i1.nome}" ({_txt_faixa(a1, b1)}) e "{i2.nome}" ({_txt_faixa(a2, b2)}) se '
                    'sobrepõem. Para os clientes que estão nas duas, qual regra vale?',
                    [f'"{i1.nome}"', f'"{i2.nome}"'], 0,
                    'só a 1ª regra que pega o cliente vale (manual 7.6); a sugestão segue a ordem da recência'))
        coberto_ate = -1
        for a, b in intervalos:
            if a > coberto_ate and final is None:
                rev_falta = _txt_faixa(coberto_ate, a)
                perguntas.append(Pergunta(
                    f'buraco:{coberto_ate}:{a}', f'Nenhuma regra cobre clientes na faixa "{rev_falta}". O que fazer com eles?',
                    ['não agendar', 'atender com uma frequência (informe os dias)', 'deixar sem regra'], None,
                    'clientes fora de todas as faixas não recebem parametrização', aceita_numero=True))
            coberto_ate = max(coberto_ate, b)
        if coberto_ate < INFINITO and final is None:
            maior_freq = max((it.frequencia_dias or 0) for it in rec)
            perguntas.append(Pergunta(
                f'acima:{coberto_ate}', f'Clientes com mais de {coberto_ate} dias sem comprar não se enquadram em '
                'nenhuma regra. O que fazer com eles?',
                ['não agendar (regra final de bloqueio)',
                 f'atender a cada {maior_freq} dias (a maior frequência usada)' if maior_freq else
                 'atender com uma frequência (informe os dias)',
                 'deixar sem regra (o Govendas mantém o que já existir para eles)'], 0,
                'sem uma regra final, esses clientes ficam sem parametrização do GoBR; uma regra sem filtro no fim do '
                'arquivo pega todos os que sobraram', aceita_numero=True))

    # prospects
    tem_prospect = any('prospect' in it.filtros for it in esp.itens)
    if rec and not tem_prospect and final is None:
        perguntas.append(Pergunta(
            'prospects', 'Clientes que nunca compraram (prospects) não entram nas regras de recência. Como atendê-los?',
            ['deixar sem regra', 'não agendar', 'atender com uma frequência (informe os dias)'], 0,
            'regras de recência de compra só pegam quem já comprou', aceita_numero=True))

    # prioridade das regras com condição própria
    for idx, it in enumerate(esp.itens):
        if it.acao in ('frequencia', 'nao_agendar') and it.outras_condicoes and rec:
            perguntas.append(Pergunta(
                f'prioridade:{idx}', f'A regra "{it.nome}" ({"; ".join(it.outras_condicoes)}) pode pegar clientes '
                'que também estão nas faixas de recência. Qual vale para eles?',
                [f'"{it.nome}" vale primeiro', 'as regras de recência valem primeiro'], 0,
                'só a 1ª regra que pega o cliente vale (manual 7.6); a regra mais específica costuma vir antes'))

    rev.perguntas = [p for p in perguntas if p.id not in decisoes]
    return rev


# ---------------------------------------------------------------- respostas

_ACEITE = re.compile(r'^\s*(ok|okay|sim|s|pode|pode seguir|segue|seguir|aceito|aceita|aceitar|concordo|'
                     r'tudo certo|todas?|as sugest(õ|o)es|usar as sugest(õ|o)es|manda ver)\b', re.I)


def interpretar_respostas(texto: str, perguntas: Sequence[Pergunta]) -> Tuple[Dict[str, Decisao], bool]:
    """Lê respostas no formato "1a, 2: 21 dias, 3b" ou um aceite geral ("ok", "pode seguir").

    Devolve as decisões reconhecidas e se o texto foi um aceite das sugestões para o que não foi respondido.
    """
    decisoes: Dict[str, Decisao] = {}
    for m in re.finditer(r'(\d+)\s*[-:=)]?\s*(?:([a-z])\b|(\d+)\s*dias?)', texto.lower()):
        n = int(m.group(1)) - 1
        if not 0 <= n < len(perguntas):
            continue
        p = perguntas[n]
        if m.group(2):
            i = ord(m.group(2)) - ord('a')
            if 0 <= i < len(p.opcoes):
                decisoes[p.id] = Decisao(opcao=i, explicita=True)
        elif m.group(3) and p.aceita_numero:
            decisoes[p.id] = Decisao(numero=int(m.group(3)), explicita=True)
    aceite = bool(_ACEITE.match(texto)) or bool(re.search(r'\b(resto|demais|outras)\b.*\bsugest', texto.lower()))
    return decisoes, aceite


def aplicar_sugestoes(perguntas: Sequence[Pergunta], decisoes: Dict[str, Decisao]) -> List[str]:
    """Usa a sugestão em toda pergunta ainda sem decisão. Devolve as que ficaram sem resposta (sem sugestão)."""
    pendentes = []
    for p in perguntas:
        if p.id in decisoes:
            continue
        if p.sugestao is None:
            pendentes.append(p.id)
        else:
            decisoes[p.id] = Decisao(opcao=p.sugestao)
    return pendentes


# ---------------------------------------------------------------- plano

def _opcao(decisoes: Dict[str, Decisao], chave: str) -> Optional[int]:
    d = decisoes.get(chave)
    return None if d is None else d.opcao


def planejar(esp: Especificacao, decisoes: Dict[str, Decisao]) -> Tuple[List[BlocoPlano], str, str, List[str]]:
    """Blocos na ordem de aplicação, nome do time, seleção de vendedores e avisos do plano."""
    avisos: List[str] = []
    equipe = esp.equipe
    if equipe == 'nao_informado':
        equipe = {0: 'televendas', 1: 'campo', 2: 'todos'}.get(_opcao(decisoes, 'equipe'), 'televendas')
    nome_time = esp.nome_time or NOME_TIME_PADRAO[equipe]
    vendedores = VENDEDORES_POR_EQUIPE[equipe]

    bloqueios: List[BlocoPlano] = []
    especificos: List[BlocoPlano] = []
    prospects: List[BlocoPlano] = []
    recencia: List[Tuple[Tuple[int, int], BlocoPlano]] = []
    finais: List[BlocoPlano] = []

    filtros_bloqueados = set()
    if _opcao(decisoes, 'baixados') == 0:
        bloqueios.append(BlocoPlano('Não agendar clientes baixados na Receita Federal', 'bloqueio', 'nao_agendar',
                                    filtros=['baixado_receita'], origem='sugestao'))
        filtros_bloqueados.add('baixado_receita')
    if _opcao(decisoes, 'inadimplentes') == 1:
        bloqueios.append(BlocoPlano('Não agendar inadimplentes', 'bloqueio', 'nao_agendar', filtros=['inadimplente'],
                                    origem='sugestao'))
        filtros_bloqueados.add('inadimplente')

    ordem_bloqueio = {'baixado_receita': 0, 'inadimplente': 1, 'rota_semana': 2, 'prospect': 3}
    for idx, it in enumerate(esp.itens):
        if it.acao != 'nao_agendar':
            continue
        conflito = next((k for k, d in decisoes.items() if k.startswith('conflito:') and d.opcao == 1
                         and set(esp.itens[int(k.split(':')[1])].filtros) & set(it.filtros)), None)
        if conflito:
            avisos.append(f'"{it.nome}" não foi criado: o analista decidiu agendar esses clientes')
            continue
        b = BlocoPlano(it.nome, 'bloqueio', 'nao_agendar', None, it.comprou_nos_ultimos_dias,
                       it.sem_comprar_ha_mais_de_dias, list(it.filtros), [], list(it.outras_condicoes),
                       texto_original=it.texto_original)
        if not it.tem_recencia and not it.filtros and not it.outras_condicoes:
            b.secao = 'fallback'
            finais.append(b)
            continue
        if it.tem_recencia and not it.filtros and not it.outras_condicoes:
            b.secao = 'agendamento'  # bloqueio por faixa de recência fica junto das faixas, na ordem dos dias
            recencia.append((faixa(it), b))
            continue
        bloqueios.append(b)
        filtros_bloqueados.update(it.filtros)

    # exceções promovidas a bloqueio único
    for chave, d in decisoes.items():
        if chave.startswith('excecao:') and d.opcao == 0:
            f = chave.split(':', 1)[1]
            if f not in filtros_bloqueados:
                bloqueios.append(BlocoPlano(f'Não agendar {DESCRICAO_FILTRO[f]}', 'bloqueio', 'nao_agendar',
                                            filtros=[f], origem='sugestao'))
                filtros_bloqueados.add(f)
    bloqueios.sort(key=lambda b: min([ordem_bloqueio.get(f, 9) for f in b.filtros] or [9]))

    for idx, it in enumerate(esp.itens):
        if it.acao != 'frequencia':
            continue
        freq = it.frequencia_dias
        d = decisoes.get(f'frequencia:{idx}')
        if not freq and d is not None:
            freq = d.numero or {0: 7, 1: 14, 2: 28}.get(d.opcao)
        if not freq:
            avisos.append(f'"{it.nome}" ficou fora do arquivo: falta a frequência de atendimento')
            continue
        nao = [f for f in it.exceto if f not in filtros_bloqueados]
        b = BlocoPlano(it.nome, 'agendamento', 'frequencia', freq, it.comprou_nos_ultimos_dias,
                       it.sem_comprar_ha_mais_de_dias, list(it.filtros), nao, list(it.outras_condicoes),
                       texto_original=it.texto_original)
        if it.outras_condicoes:
            primeiro = _opcao(decisoes, f'prioridade:{idx}') != 1
            (especificos if primeiro else finais).append(b)
            if not primeiro:
                b.secao = 'agendamento'
        elif 'prospect' in it.filtros:
            prospects.append(b)
        elif it.tem_recencia:
            recencia.append((faixa(it), b))
        elif not it.filtros:
            b.secao = 'fallback'
            finais.append(b)
        else:
            especificos.append(b)

    # faixas que nenhuma regra cobria, decididas pelo analista, entram junto das demais faixas
    for chave, d in decisoes.items():
        if chave.startswith('buraco:') and (d.opcao == 0 or d.numero):
            a, b_ = (int(x) for x in chave.split(':')[1:])
            bloco = BlocoPlano(f'Clientes entre {a + 1} e {b_} dias sem comprar', 'agendamento',
                               'nao_agendar' if d.opcao == 0 else 'frequencia', d.numero,
                               comprou_nos_ultimos_dias=b_, sem_comprar_ha_mais_de_dias=a if a >= 0 else None,
                               origem='sugestao')
            recencia.append(((a, b_), bloco))

    # faixas da mais recente para a mais antiga; numa sobreposição, se o analista escolheu a 2ª regra, ela vem antes
    recencia.sort(key=lambda fb: (fb[0][1], fb[0][0]))
    ordenados = [b for _, b in recencia]
    for chave, d in decisoes.items():
        if chave.startswith('sobreposicao:') and d.opcao == 1:
            i1, i2 = (esp.itens[int(x)] for x in chave.split(':')[1:])
            n1 = next((k for k, b in enumerate(ordenados) if b.nome == i1.nome), None)
            n2 = next((k for k, b in enumerate(ordenados) if b.nome == i2.nome), None)
            if n1 is not None and n2 is not None and n2 > n1:
                ordenados.insert(n1, ordenados.pop(n2))

    # decisões sobre quem sobrou
    for chave, d in decisoes.items():
        if chave.startswith('acima:') and not finais:
            if d.opcao == 0:
                finais.append(BlocoPlano('Clientes que não se enquadraram nas regras anteriores', 'fallback',
                                         'nao_agendar', origem='sugestao'))
            elif d.opcao == 1 or d.numero:
                freq = d.numero or max((b.frequencia_dias or 0) for b in ordenados) or None
                if freq:
                    finais.append(BlocoPlano('Clientes que não se enquadraram nas regras anteriores', 'fallback',
                                             'frequencia', freq, origem='sugestao'))
        if chave == 'prospects' and (d.opcao == 1 or d.numero):
            prospects.append(BlocoPlano('Prospects', 'agendamento', 'nao_agendar' if d.opcao == 1 else 'frequencia',
                                        d.numero, filtros=['prospect'], origem='sugestao'))

    blocos = bloqueios + especificos + prospects + ordenados + finais
    nomes_unicos(blocos)
    return blocos, nome_time, vendedores, avisos


def explicar_ordem(blocos: Sequence[BlocoPlano]) -> str:
    return ('Ordem dos blocos: a 1ª regra que pega o cliente vale (manual 7.6), então os bloqueios vêm primeiro, '
            'depois as regras com público próprio (prospects e condições específicas), as faixas de recência da mais '
            'recente para a mais antiga e, por último, a regra final para quem sobrou.')
