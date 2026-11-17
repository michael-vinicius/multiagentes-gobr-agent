"""Especificação estruturada das regras de negócio: o que o agente entendeu, antes de escrever GoBR.

    descrição (texto ou transcrição da imagem)
        ↓ interpretar()            modelo de linguagem com saída estruturada (JSON Schema)
    Especificacao  ─ itens com ação, frequência, faixa de recência, filtros e exceções
        ↓ conferir_numeros()       todo número precisa estar no texto do ramo de onde veio (sem número inventado)
        ↓ lacunas.py               pontos falhos e perguntas ao analista
        ↓ planejar()               blocos na ordem certa (a 1ª regra que pega o cliente vale; manual 7.6)
    BlocoPlano  ─→ molde()         GoBR determinístico para os filtros conhecidos (referência e rede de segurança)

O modelo só faz a parte que exige linguagem natural (entender a descrição). Ordem, cobertura das faixas e verificação
são determinísticas, porque o modelo local de 7B erra justamente nessas partes (relatório da etapa 4).
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Sequence

ACOES = ('frequencia', 'nao_agendar', 'agendar', 'fora_do_escopo')
FILTROS = ('prospect', 'inadimplente', 'baixado_receita', 'rota_semana')
EQUIPES = ('televendas', 'campo', 'todos', 'nao_informado')

VENDEDORES_POR_EQUIPE = {'televendas': 'todostelevendas', 'campo': 'todosdecampo', 'todos': 'todos'}
NOME_TIME_PADRAO = {'televendas': 'televendas', 'campo': 'campo', 'todos': 'todos'}

# Cláusulas GoBR de cada filtro conhecido: as formas do manual (seção 6) e as mais usadas nas regras reais.
CLAUSULA_FILTRO = {
    'prospect': 'no ciclo de vida prospect com a empresa',
    'inadimplente': 'inadimplentes',
    'baixado_receita': 'status na receita federal definido como baixada',
    'rota_semana': 'data da rota na semana',
}
DESCRICAO_FILTRO = {
    'prospect': 'clientes que nunca compraram (prospects)',
    'inadimplente': 'clientes inadimplentes',
    'baixado_receita': 'clientes baixados na Receita Federal',
    'rota_semana': 'clientes com rota de visita na semana',
}


@dataclass
class Item:
    """Uma regra da descrição do analista (um ramo do mapa mental)."""
    nome: str
    acao: str
    ramo: int = 0
    frequencia_dias: Optional[int] = None
    comprou_nos_ultimos_dias: Optional[int] = None  # comprou há no máximo N dias  (d ≤ N)
    sem_comprar_ha_mais_de_dias: Optional[int] = None  # está há mais de N dias sem comprar (d > N)
    filtros: List[str] = field(default_factory=list)
    exceto: List[str] = field(default_factory=list)
    outras_condicoes: List[str] = field(default_factory=list)
    texto_original: str = ''
    origem: str = 'descricao'  # 'descricao' (veio do analista) ou 'sugestao' (proposta pelo agente e aceita)

    @property
    def tem_recencia(self) -> bool:
        return self.comprou_nos_ultimos_dias is not None or self.sem_comprar_ha_mais_de_dias is not None


@dataclass
class Especificacao:
    titulo: str = ''
    equipe: str = 'nao_informado'
    nome_time: str = ''
    itens: List[Item] = field(default_factory=list)
    avisos: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'Especificacao':
        itens = [Item(**i) for i in d.get('itens', [])]
        return cls(d.get('titulo', ''), d.get('equipe', 'nao_informado'), d.get('nome_time', ''), itens,
                   list(d.get('avisos', [])))


# ---------------------------------------------------------------- interpretação pelo modelo

SCHEMA_ITEM = {
    'type': 'object',
    'properties': {
        'ramo': {'type': 'integer'},
        'nome': {'type': 'string'},
        'acao': {'type': 'string', 'enum': list(ACOES)},
        'frequencia_dias': {'type': ['integer', 'null']},
        'comprou_nos_ultimos_dias': {'type': ['integer', 'null']},
        'sem_comprar_ha_mais_de_dias': {'type': ['integer', 'null']},
        'filtros': {'type': 'array', 'items': {'type': 'string', 'enum': list(FILTROS)}},
        'exceto': {'type': 'array', 'items': {'type': 'string', 'enum': list(FILTROS)}},
        'outras_condicoes': {'type': 'array', 'items': {'type': 'string'}},
    },
    'required': ['ramo', 'nome', 'acao', 'frequencia_dias', 'comprou_nos_ultimos_dias',
                 'sem_comprar_ha_mais_de_dias', 'filtros', 'exceto', 'outras_condicoes'],
}
SCHEMA_ESPECIFICACAO = {
    'type': 'object',
    'properties': {
        'titulo': {'type': 'string'},
        'equipe': {'type': 'string', 'enum': list(EQUIPES)},
        'itens': {'type': 'array', 'items': SCHEMA_ITEM},
    },
    'required': ['titulo', 'equipe', 'itens'],
}

SYSTEM_INTERPRETAR = """\
Você é o analista que lê a descrição de regras comerciais de agendamento de clientes (sistema Govendas) e a \
converte em uma especificação estruturada. A descrição vem numerada: cada número é um ramo (uma regra).

Para cada ramo, preencha um item:
- ramo: o número do ramo.
- nome: o nome da regra, como está no ramo.
- acao: "frequencia" (atender a cada N dias), "nao_agendar" (bloquear o agendamento), "agendar" (permitir o \
agendamento sem frequência definida) ou "fora_do_escopo" (não é regra de quem agendar nem com que frequência, \
por exemplo metas, capacidade de atendimento ou observações gerais).
- frequencia_dias: o intervalo de atendimento em dias, quando houver ("14 dias" → 14).
- comprou_nos_ultimos_dias: o limite de recência da última compra, quando o cliente COMPROU nos últimos N dias \
("compraram nos últimos 90", "com pedido nos últimos 30 dias", "compra entre 0 e 60 dias" → o maior número).
- sem_comprar_ha_mais_de_dias: quando o cliente está há MAIS de N dias sem comprar ("estão a 60 dias sem comprar", \
"sem pedidos a mais de 45 dias", "pedidos entre 60 e 90 dias" → o menor número, 60).
- filtros: condições conhecidas que selecionam os clientes da regra: "prospect" (nunca comprou, ciclo de vida \
prospect), "inadimplente", "baixado_receita" (baixado/inativo na Receita Federal), "rota_semana" (cliente na rota de \
visita da semana ou na rota do vendedor externo).
- exceto: condições conhecidas que EXCLUEM clientes da regra ("somente clientes que não estão na rota da semana" → \
"rota_semana"; "exceto inadimplentes" → "inadimplente").
- outras_condicoes: outras condições do público, em texto curto, que não se encaixam nos campos acima.

E no topo:
- titulo: o título da descrição.
- equipe: "televendas", "campo" ou "todos", se a descrição disser quem atende; senão "nao_informado".

Regras:
- Use só números que aparecem no ramo. Não invente valores; deixe null o que não estiver escrito.
- Um ramo sem dias de compra não tem recência: deixe os dois campos de recência null.
- Um ramo de bloqueio ("não agendar …") tem acao "nao_agendar" e o público em filtros.
"""

EXEMPLO_ENTRADA = """\
Título: Regra Distribuidora Exemplo
1. Frequentes → Clientes que compraram nos últimos 20 dias → 10 dias
2. Esfriando → Compraram nos últimos 50 dias mas estão há 20 dias sem comprar → 5 dias → Exceto inadimplentes
3. Perdidos → Sem compras há mais de 50 dias → 30 dias → Apenas clientes que não estão na rota do vendedor externo
4. Novos → Nunca compraram → 10 dias
5. Não ligar para quem está na rota do vendedor externo nesta semana (televendas)
6. Curva A → Clientes curva A com a empresa → 7 dias
7. Meta: 400 ligações por mês"""

EXEMPLO_SAIDA = """\
{"titulo": "Regra Distribuidora Exemplo", "equipe": "televendas", "itens": [
{"ramo": 1, "nome": "Frequentes", "acao": "frequencia", "frequencia_dias": 10, "comprou_nos_ultimos_dias": 20, \
"sem_comprar_ha_mais_de_dias": null, "filtros": [], "exceto": [], "outras_condicoes": []},
{"ramo": 2, "nome": "Esfriando", "acao": "frequencia", "frequencia_dias": 5, "comprou_nos_ultimos_dias": 50, \
"sem_comprar_ha_mais_de_dias": 20, "filtros": [], "exceto": ["inadimplente"], "outras_condicoes": []},
{"ramo": 3, "nome": "Perdidos", "acao": "frequencia", "frequencia_dias": 30, "comprou_nos_ultimos_dias": null, \
"sem_comprar_ha_mais_de_dias": 50, "filtros": [], "exceto": ["rota_semana"], "outras_condicoes": []},
{"ramo": 4, "nome": "Novos", "acao": "frequencia", "frequencia_dias": 10, "comprou_nos_ultimos_dias": null, \
"sem_comprar_ha_mais_de_dias": null, "filtros": ["prospect"], "exceto": [], "outras_condicoes": []},
{"ramo": 5, "nome": "Não ligar para quem está na rota do externo", "acao": "nao_agendar", "frequencia_dias": null, \
"comprou_nos_ultimos_dias": null, "sem_comprar_ha_mais_de_dias": null, "filtros": ["rota_semana"], "exceto": [], \
"outras_condicoes": []},
{"ramo": 6, "nome": "Curva A", "acao": "frequencia", "frequencia_dias": 7, "comprou_nos_ultimos_dias": null, \
"sem_comprar_ha_mais_de_dias": null, "filtros": [], "exceto": [], "outras_condicoes": ["curva A com a empresa"]},
{"ramo": 7, "nome": "Meta: 400 ligações por mês", "acao": "fora_do_escopo", "frequencia_dias": null, \
"comprou_nos_ultimos_dias": null, "sem_comprar_ha_mais_de_dias": null, "filtros": [], "exceto": [], \
"outras_condicoes": []}]}"""


def numerar_descricao(texto: str) -> str:
    """Garante uma linha numerada por ramo; texto livre do analista vira uma regra por linha não vazia."""
    linhas = [l.strip() for l in texto.strip().splitlines() if l.strip()]
    if any(re.match(r'^\d+[.)]\s', l) for l in linhas):
        return '\n'.join(linhas)
    # texto corrido: uma regra por frase (a frase seguinte começa com maiúscula)
    linhas = [f.strip() for l in linhas for f in re.split(r'(?<=[.;!?])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ])', l) if f.strip()]
    out, n = [], 0
    for l in linhas:
        if l.lower().startswith('título:'):
            out.append(l)
        else:
            n += 1
            out.append(f'{n}. {l.lstrip("-•* ")}')
    return '\n'.join(out)


def ramos_da_descricao(texto: str) -> Dict[int, str]:
    out = {}
    for l in texto.splitlines():
        m = re.match(r'^\s*(\d+)[.)]\s+(.*)', l)
        if m:
            out[int(m.group(1))] = m.group(2)
    return out


def interpretar(backend: Any, descricao: str) -> Especificacao:
    from llm_json import pedir_json
    descricao = numerar_descricao(descricao)
    usuario = (f'Exemplo de descrição:\n<descricao>\n{EXEMPLO_ENTRADA}\n</descricao>\nEspecificação do exemplo:\n'
               f'{EXEMPLO_SAIDA}\n\nAgora a descrição real:\n<descricao>\n{descricao}\n</descricao>')
    bruto = pedir_json(backend, SYSTEM_INTERPRETAR, usuario, SCHEMA_ESPECIFICACAO)
    ramos = ramos_da_descricao(descricao)
    titulo = next((l.split(':', 1)[1].strip() for l in descricao.splitlines() if l.lower().startswith('título:')), '')
    esp = Especificacao(bruto.get('titulo') or titulo, bruto.get('equipe', 'nao_informado'))
    for i in bruto['itens']:
        esp.itens.append(Item(
            nome=i['nome'].strip() or f'Regra {i["ramo"]}', acao=i['acao'], ramo=i['ramo'],
            frequencia_dias=i['frequencia_dias'], comprou_nos_ultimos_dias=i['comprou_nos_ultimos_dias'],
            sem_comprar_ha_mais_de_dias=i['sem_comprar_ha_mais_de_dias'],
            filtros=sorted(set(i['filtros'])), exceto=sorted(set(i['exceto'])),
            outras_condicoes=[c for c in i['outras_condicoes'] if c.strip()],
            texto_original=ramos.get(i['ramo'], '')))
    conferir_especificacao(esp, ramos, descricao)
    return esp


def _numeros(texto: str) -> set:
    return {int(n) for n in re.findall(r'\d+', texto)}


# sinais de que uma linha é regra (tem número ou verbo de ação); "Atendimento feito pelo televendas." não tem nenhum
_CARA_DE_REGRA = re.compile(r'\d|agend|frequ|a cada|ligar|bloque', re.I)


def _normalizar(s: str) -> str:
    import unicodedata
    s = unicodedata.normalize('NFKD', s.lower())
    return re.sub(r'\s+', ' ', ''.join(c for c in s if not unicodedata.combining(c))).strip()


def alinhar_ramos(esp: Especificacao, ramos: Dict[int, str]) -> None:
    """Corrige o índice de ramo do modelo pelo nome do item.

    Uma linha sem regra no topo ("Equipe de campo (visitas presenciais)") também é numerada; o modelo de 7B às vezes
    numera os itens a partir da 1ª regra, e cada item passa a ser conferido contra o texto da linha anterior.
    """
    usados = set()
    for it in esp.itens:
        nome = _normalizar(it.nome)
        if not nome:
            continue
        atual = _normalizar(ramos.get(it.ramo, ''))
        if atual.startswith(nome):
            usados.add(it.ramo)
            continue
        candidatos = [n for n, t in ramos.items() if n not in usados and _normalizar(t).startswith(nome)]
        if len(candidatos) == 1:
            it.ramo = candidatos[0]
            it.texto_original = ramos[it.ramo]
            usados.add(it.ramo)


def conferir_especificacao(esp: Especificacao, ramos: Dict[int, str], descricao: str = '') -> None:
    """Correções determinísticas do que o modelo devolveu. Cada correção vira um aviso visível ao analista.

    - o item é ligado ao ramo cujo texto começa com o nome dele (o índice do modelo pode estar deslocado);
    - número que não aparece no texto do ramo é descartado (o modelo não pode inventar valores), salvo quando o
      vizinho (±1) aparece: "entre 60 e 90" lido como 89 volta a ser 90, o número escrito;
    - faixa invertida (limite inferior ≥ superior) é trocada;
    - item sem público, sem número e sem verbo de ação no texto é informação, não regra (fora do escopo);
    - ramo com cara de regra sem item correspondente é acusado;
    - equipe citada no texto ("televendas", "campo") é usada se o modelo não a preencheu.
    """
    alinhar_ramos(esp, ramos)
    for it in esp.itens:
        texto = ramos.get(it.ramo, it.texto_original)
        if not it.texto_original:
            it.texto_original = texto
        disponiveis = _numeros(texto)
        for campo in ('frequencia_dias', 'comprou_nos_ultimos_dias', 'sem_comprar_ha_mais_de_dias'):
            v = getattr(it, campo)
            if v is not None and texto and v not in disponiveis:
                vizinhos = [n for n in (v + 1, v - 1) if n in disponiveis and n not in
                            {getattr(it, c) for c in ('comprou_nos_ultimos_dias', 'sem_comprar_ha_mais_de_dias')}]
                if campo != 'frequencia_dias' and vizinhos:
                    esp.avisos.append(f'"{it.nome}": o valor {v} ({campo}) foi trocado por {vizinhos[0]}, '
                                      f'o número escrito no ramo')
                    setattr(it, campo, vizinhos[0])
                else:
                    esp.avisos.append(f'"{it.nome}": o valor {v} ({campo}) não aparece no texto do ramo e foi '
                                      f'descartado')
                    setattr(it, campo, None)
        a, b = it.sem_comprar_ha_mais_de_dias, it.comprou_nos_ultimos_dias
        if a is not None and b is not None and a >= b:
            it.sem_comprar_ha_mais_de_dias, it.comprou_nos_ultimos_dias = b, a
            esp.avisos.append(f'"{it.nome}": faixa de recência invertida ({a} e {b}); corrigida para {b} a {a} dias')
        if texto:
            conferir_filtros(it, texto, esp.avisos)
        sem_publico = not (it.tem_recencia or it.filtros or it.exceto or it.outras_condicoes)
        if it.acao in ('frequencia', 'nao_agendar', 'agendar') and sem_publico and texto \
                and not _CARA_DE_REGRA.search(texto):
            it.acao = 'fora_do_escopo'
            esp.avisos.append(f'"{it.nome}": a linha não tem público, número nem ação; tratei como informação, '
                              f'não como regra')
    vistos = {it.ramo for it in esp.itens}
    for n, texto in ramos.items():
        if n not in vistos and _CARA_DE_REGRA.search(texto):
            esp.avisos.append(f'o ramo {n} ("{texto}") não foi interpretado; confira se ele é uma regra')
    if esp.equipe == 'nao_informado' and descricao:
        baixo = descricao.lower()
        if 'televendas' in baixo:
            esp.equipe = 'televendas'
        elif re.search(r'\b(campo|externo|presencial)\b', baixo) and 'televendas' not in baixo:
            esp.equipe = 'campo'


MARCADORES_FILTRO = {
    'prospect': re.compile(r'prospect|nunca (?:compr|tir)', re.I),
    'inadimplente': re.compile(r'inadimpl|inadipl', re.I),
    'baixado_receita': re.compile(r'baixad|receita federal|na receita', re.I),
    'rota_semana': re.compile(r'\brota\b', re.I),
}
# negação do público ("somente clientes que não estão na rota", "exceto inadimplentes"); o "não" de "não agendar" é
# a ação do ramo e é retirado antes da busca
_NEGACAO_PUBLICO = re.compile(r'\b(n[ãa]o|exceto|menos|sem|fora d[ao])\b', re.I)
_ACAO_NEGATIVA = re.compile(r'\bn[ãa]o (?:agendar|pode(?:m)? ser agendad[oa]s?|ligar|atender)\b', re.I)


def classificar_filtros(texto: str) -> Dict[str, str]:
    """Para cada filtro conhecido citado no texto do ramo: 'inclui' ou 'exclui' (negado antes do marcador)."""
    out: Dict[str, str] = {}
    for trecho in re.split(r'→|\n', texto):
        limpo = _ACAO_NEGATIVA.sub('', trecho)
        for f, marcador in MARCADORES_FILTRO.items():
            m = marcador.search(limpo)
            if not m:
                continue
            antes = limpo[:m.start()]
            # a negação vale para o marcador se estiver na mesma oração (sem ponto entre os dois)
            negado = bool(_NEGACAO_PUBLICO.search(antes.split('.')[-1]))
            out.setdefault(f, 'exclui' if negado else 'inclui')
    return out


def conferir_filtros(it: Item, texto: str, avisos: List[str]) -> None:
    """Confere filtros e exceções do modelo contra o texto do ramo.

    O modelo local de 7B troca "somente clientes que NÃO estão na rota" por um filtro positivo, o que inverte a regra.
    Aqui um filtro citado no texto vai para `filtros` ou `exceto` conforme a negação, e um filtro que o texto não
    cita é retirado.
    """
    if it.acao == 'fora_do_escopo':
        return
    # condições livres que só repetem um filtro conhecido ou a recência já preenchida saem (senão o bloco perderia
    # o molde e a verificação)
    for c in list(it.outras_condicoes):
        repete_filtro = any(m.search(c) for m in MARCADORES_FILTRO.values())
        repete_recencia = it.tem_recencia and re.search(r'\b(compr|pedido|positiva|dias?)\b', c, re.I) \
            and not re.search(r'curva|ramo|segment|regi|cidade|estado|uf\b|faturamento|ticket', c, re.I)
        if repete_filtro or repete_recencia:
            it.outras_condicoes.remove(c)
            avisos.append(f'"{it.nome}": condição "{c}" já está representada nos campos estruturados')
    citados = classificar_filtros(texto)
    for f in FILTROS:
        lugar = citados.get(f)
        antes = ('filtros' if f in it.filtros else '') or ('exceto' if f in it.exceto else '')
        depois = {'inclui': 'filtros', 'exclui': 'exceto', None: ''}[lugar]
        if it.acao == 'nao_agendar' and depois == 'exceto' and not antes:
            depois = ''  # em bloqueio, só mexe no que o modelo marcou
        if antes == depois:
            continue
        if f in it.filtros:
            it.filtros.remove(f)
        if f in it.exceto:
            it.exceto.remove(f)
        if depois:
            getattr(it, depois).append(f)
            getattr(it, depois).sort()
        acao = {('', 'filtros'): 'incluído no público', ('', 'exceto'): 'incluído como exceção',
                ('filtros', 'exceto'): 'passou de filtro para exceção (o texto nega)',
                ('exceto', 'filtros'): 'passou de exceção para filtro (o texto não nega)',
                ('filtros', ''): 'retirado (o texto não cita)', ('exceto', ''): 'retirado (o texto não cita)'}
        avisos.append(f'"{it.nome}": "{f}" {acao[(antes, depois)]}')


# ---------------------------------------------------------------- plano e molde

@dataclass
class BlocoPlano:
    nome: str
    secao: str  # 'bloqueio', 'agendamento' ou 'fallback'
    acao: str  # 'nao_agendar' ou 'frequencia'
    frequencia_dias: Optional[int] = None
    comprou_nos_ultimos_dias: Optional[int] = None
    sem_comprar_ha_mais_de_dias: Optional[int] = None
    filtros: List[str] = field(default_factory=list)
    nao_filtros: List[str] = field(default_factory=list)  # exceções que não foram para um bloqueio geral
    outras_condicoes: List[str] = field(default_factory=list)
    origem: str = 'descricao'
    texto_original: str = ''

    def condicoes_molde(self) -> Optional[List[str]]:
        """Condições em GoBR; None se houver condição sem molde conhecido (fica para o modelo + RAG)."""
        if self.outras_condicoes:
            return None
        conds = [CLAUSULA_FILTRO[f] for f in self.filtros]
        if self.comprou_nos_ultimos_dias is not None:
            conds.append(f'recencia de positivacao em {self.comprou_nos_ultimos_dias} dias')
        if self.sem_comprar_ha_mais_de_dias is not None:
            conds.append(f'fora da recencia de positivacao em {self.sem_comprar_ha_mais_de_dias} dias')
        for f in self.nao_filtros:
            if f == 'inadimplente':
                conds.append('adimplentes')  # forma usada em 220 regras reais
            else:
                return None  # o GoBR não tem negação documentada para os outros filtros
        return conds

    def descricao(self, nome_time: str) -> str:
        """O bloco em linguagem natural: é o pedido que vai para o RAG e para o modelo."""
        publico = []
        for f in self.filtros:
            publico.append(DESCRICAO_FILTRO[f])
        a, b = self.sem_comprar_ha_mais_de_dias, self.comprou_nos_ultimos_dias
        if a is not None and b is not None:
            publico.append(f'clientes que compraram nos últimos {b} dias, mas estão há mais de {a} dias sem comprar')
        elif b is not None:
            publico.append(f'clientes que compraram nos últimos {b} dias')
        elif a is not None:
            publico.append(f'clientes que já compraram, mas estão há mais de {a} dias sem comprar')
        publico += self.outras_condicoes
        publico += [f'exceto {DESCRICAO_FILTRO[f]}' for f in self.nao_filtros]
        alvo = ', '.join(publico) if publico else 'todos os clientes que não se enquadraram nas regras anteriores'
        acao = 'não devem ser agendados' if self.acao == 'nao_agendar' else \
            f'devem ser atendidos com frequência de {self.frequencia_dias} dias'
        return f'Para o time "{nome_time}": {alvo} {acao}.'


def molde(bloco: BlocoPlano, nome_time: str) -> Optional[str]:
    conds = bloco.condicoes_molde()
    if conds is None:
        return None
    linhas = [f'parametros "{bloco.nome}":', f'    do time("{nome_time}")']
    for i, c in enumerate(conds):
        linhas.append(f'    {"quando" if i == 0 else "e"} {c}')
    linhas.append('    nao agendar' if bloco.acao == 'nao_agendar' else f'    frequencia de {bloco.frequencia_dias} dias')
    return '\n'.join(linhas)


def nomes_unicos(blocos: Sequence[BlocoPlano]) -> None:
    """O manual exige nomes distintos para os blocos de parâmetros (7.6)."""
    vistos: Dict[str, int] = {}
    for b in blocos:
        base = b.nome.replace('"', "'").strip() or 'Regra'
        n = vistos.get(base.lower(), 0)
        vistos[base.lower()] = n + 1
        b.nome = base if n == 0 else f'{base} ({n + 1})'


def montar_arquivo(titulo: str, nome_time: str, vendedores: str, blocos_gobr: Sequence[str],
                   secoes: Sequence[str]) -> str:
    """Arquivo completo: versão, time e os blocos agrupados por seção, na ordem do plano."""
    nomes_secao = {'bloqueio': 'Bloqueios (vêm primeiro: a 1ª regra que pega o cliente vale)',
                   'agendamento': 'Regras de agendamento', 'fallback': 'Regra final (clientes que sobraram)'}
    partes = ['version 1.0', '']
    if titulo:
        partes += [f'# {titulo}', '']
    partes += ['## Definição de times', '', f'time "{nome_time}":', f'    vendedores {vendedores} ativados', '']
    secao_atual = None
    for gobr, secao in zip(blocos_gobr, secoes):
        if secao != secao_atual:
            partes += ['', f'## {nomes_secao.get(secao, secao)}', '']
            secao_atual = secao
        partes += [gobr, '']
    return '\n'.join(partes).rstrip() + '\n'
