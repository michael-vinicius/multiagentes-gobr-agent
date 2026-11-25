"""Memória do agente (etapa 6): longo prazo entre sessões e gestão do contexto da conversa.

Termos do livro da disciplina (Dibia, *Designing Multi-Agent Systems*, cap. 4):

- **memória de curto prazo** (4.7.1): o histórico da sessão. Vive no estado do grafo LangGraph (`historico`,
  `versoes`), que um checkpointer SQLite salva a cada passo; a sessão pode ser retomada pelo id depois de fechar o
  programa (agente.py).
- **memória de longo prazo** (4.7.2): o que passa de uma sessão para outra. Dois tipos:
  - conhecimento: o RAG das etapas 2–4 (regras reais e manual), que já existia;
  - episódica e de preferências: `MemoriaLonga`, sobre um LangGraph Store (SQLite), com namespaces por empresa
    (último arquivo aprovado, especificação, decisões) e por analista (preferências e notas).
- **seleção do que lembrar** (4.7.3): híbrida. No fim da sessão o agente propõe os candidatos (arquivo aprovado e
  decisões da empresa, preferências que o analista escolheu) e o analista confirma; "lembre que ..." grava na hora,
  a pedido (memória gerida explicitamente, 4.8).
- **gestão de contexto** (4.12): compactação cabeça + cauda do histórico com orçamento de tokens (`montar_historico`)
  e filtragem de resultados (o arquivo GoBR de versões antigas sai do histórico; o atual entra uma vez, no system).
  As decisões ficam no estado estruturado (especificação, decisões, plano), nunca só no texto do chat: é isso que
  permite cortar o histórico sem perder o que foi combinado.
"""
from __future__ import annotations

import math
import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence, Tuple

# perguntas da revisão (lacunas.py) cuja resposta vale para qualquer empresa: viram preferências do analista
PREFERENCIAS = ('equipe', 'baixados', 'inadimplentes', 'prospects')
# rótulo curto de cada opção, na mesma ordem das opções de lacunas.revisar (um teste confere o alinhamento)
OPCOES_PREFERENCIA = {
    'equipe': ['televendas', 'campo', 'todos os vendedores'],
    'baixados': ['não agendar baixados na Receita', 'agendar baixados na Receita'],
    'inadimplentes': ['agendar inadimplentes normalmente', 'não agendar inadimplentes'],
    'prospects': ['deixar prospects sem regra', 'não agendar prospects', 'atender prospects com uma frequência'],
}

_PALAVRAS_VAZIAS = {'regra', 'regras', 'comercial', 'comerciais', 'parametrizacao', 'de', 'da', 'do', 'das', 'dos',
                    'e', 'a', 'o', 'para', 'nova', 'novo', 'titulo'}


def normalizar(s: str) -> str:
    s = unicodedata.normalize('NFKD', (s or '').lower())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()


def chave_empresa(titulo: str) -> str:
    """"Regra Maxlub" → "maxlub"; "V1 Vidros - Regra Comercial" → "v1-vidros"."""
    return '-'.join(p for p in normalizar(titulo).split() if p not in _PALAVRAS_VAZIAS)


def agora() -> str:
    return datetime.now().strftime('%d/%m/%Y %H:%M')


# ---------------------------------------------------------------- memória de longo prazo

class MemoriaLonga:
    """Memória entre sessões sobre um LangGraph `BaseStore` (InMemoryStore nos testes, SqliteStore no uso real).

    Namespaces:
    - ("empresas",) / <chave da empresa>: última versão aprovada (arquivo, especificação, plano, decisões), data,
      sessão e os pedidos feitos naquela sessão (o episódio);
    - ("analistas", <analista>, "preferencias") / <id da pergunta>: opção escolhida, data e origem;
    - ("analistas", <analista>, "notas") / nota-<timestamp>: lembretes livres ("lembre que ...").
    """

    def __init__(self, store: Any, analista: str = 'analista'):
        self.store = store
        self.analista = normalizar(analista).replace(' ', '-') or 'analista'

    @property
    def _ns_pref(self) -> Tuple[str, ...]:
        return ('analistas', self.analista, 'preferencias')

    @property
    def _ns_notas(self) -> Tuple[str, ...]:
        return ('analistas', self.analista, 'notas')

    # empresas (memória episódica)
    def lembrar_empresa(self, chave: str, valor: Dict[str, Any]) -> None:
        self.store.put(('empresas',), chave, valor)

    def empresa(self, chave: str) -> Optional[Dict[str, Any]]:
        item = self.store.get(('empresas',), chave)
        return item.value if item else None

    def empresas(self) -> List[Tuple[str, Dict[str, Any]]]:
        return [(i.key, i.value) for i in self.store.search(('empresas',), limit=200)]

    def achar_empresa(self, texto: str) -> Optional[Tuple[str, Dict[str, Any]]]:
        """Empresa lembrada cujo nome aparece no texto (a de nome mais longo, se houver mais de uma)."""
        alvo = f' {normalizar(texto)} '
        achadas = [(k, v) for k, v in self.empresas() if k and f' {k.replace("-", " ")} ' in alvo]
        return max(achadas, key=lambda kv: len(kv[0])) if achadas else None

    # preferências e notas do analista
    def lembrar_preferencia(self, pergunta_id: str, opcao: int, origem: str = '') -> str:
        texto = OPCOES_PREFERENCIA[pergunta_id][opcao]
        self.store.put(self._ns_pref, pergunta_id, {'opcao': opcao, 'texto': texto, 'data': agora(),
                                                    'origem': origem})
        return texto

    def preferencias(self) -> Dict[str, Dict[str, Any]]:
        return {i.key: i.value for i in self.store.search(self._ns_pref, limit=100)}

    def lembrar_nota(self, texto: str) -> None:
        self.store.put(self._ns_notas, f'nota-{datetime.now():%Y%m%d%H%M%S%f}', {'texto': texto, 'data': agora()})

    def notas(self) -> List[Tuple[str, Dict[str, Any]]]:
        return [(i.key, i.value) for i in self.store.search(self._ns_notas, limit=100)]

    # o analista vê e apaga o que o agente lembra
    def descrever(self) -> str:
        linhas = []
        for chave, v in sorted(self.empresas()):
            n = len([b for b in (v.get('versao') or {}).get('blocos', [])])
            linhas.append(f'- empresa "{v.get("titulo", chave)}": arquivo de {v.get("data")} ({n} blocos) e '
                          f'{len(v.get("versao", {}).get("decisoes", {}))} decisões')
        for pid, v in sorted(self.preferencias().items()):
            linhas.append(f'- preferência: {v["texto"]} (desde {v["data"]}{", " + v["origem"] if v.get("origem") else ""})')
        for _, v in self.notas():
            linhas.append(f'- nota de {v["data"]}: "{v["texto"]}"')
        if not linhas:
            return 'Ainda não guardei nada sobre você nem sobre empresas.'
        return 'Isto é o que eu lembro de sessões anteriores:\n' + '\n'.join(linhas)

    def esquecer(self, termo: str) -> List[str]:
        """Apaga o que casa com o termo (nome da empresa, assunto da preferência ou texto da nota)."""
        alvo = normalizar(termo)
        tudo = not alvo or alvo in ('tudo', 'todas', 'todos', 'tudo que voce lembra')
        apagados = []
        for chave, v in self.empresas():
            if tudo or chave.replace('-', ' ') in alvo or alvo in normalizar(v.get('titulo', '')):
                self.store.delete(('empresas',), chave)
                apagados.append(f'a empresa "{v.get("titulo", chave)}"')
        for pid, v in self.preferencias().items():
            if tudo or pid in alvo or normalizar(v['texto']) in alvo or alvo in normalizar(v['texto']):
                self.store.delete(self._ns_pref, pid)
                apagados.append(f'a preferência "{v["texto"]}"')
        for chave, v in self.notas():
            if tudo or (alvo and alvo in normalizar(v['texto'])):
                self.store.delete(self._ns_notas, chave)
                apagados.append(f'a nota "{v["texto"]}"')
        return apagados


def preferencia_do_texto(texto: str) -> Optional[Tuple[str, int]]:
    """"lembre que inadimplentes devem sempre ser bloqueados" → ('inadimplentes', 1). Regras de palavras, sem modelo."""
    t = normalizar(texto)
    bloqueia = bool(re.search(r'\b(bloque\w*|nao agend\w*|nao ligar|sem agend\w*|nao atend\w*)', t))
    agenda = not bloqueia and bool(re.search(r'\b(agend\w*|atend\w*|ligar)\b', t))
    if 'inadimpl' in t and (bloqueia or agenda):
        return 'inadimplentes', 1 if bloqueia else 0
    if re.search(r'\bbaixad|receita', t) and (bloqueia or agenda):
        return 'baixados', 0 if bloqueia else 1
    if re.search(r'\b(equipe|time|atendimento|regras?)\b', t):
        for i, nome in enumerate(('televendas', 'campo', 'todos')):
            if re.search(rf'\b{nome}\b', t):
                return 'equipe', i
    return None


def aplicar_lembradas(perguntas: Sequence[Any], lembradas: Dict[str, Dict[str, Any]]) -> List[str]:
    """Respostas lembradas viram a sugestão da pergunta, com o motivo. A pergunta continua sendo feita: a memória
    sugere, o analista decide (uma decisão antiga pode não valer mais). Devolve os ids alterados."""
    alterados = []
    for p in perguntas:
        lem = lembradas.get(p.id)
        if not lem or lem.get('opcao') is None or not 0 <= lem['opcao'] < len(p.opcoes):
            continue
        p.sugestao = lem['opcao']
        de_onde = f', {lem["origem"]}' if lem.get('origem') else ''
        p.motivo = f'lembrado: você escolheu "{p.opcoes[lem["opcao"]]}" em {lem["data"]}{de_onde}'
        alterados.append(p.id)
    return alterados


# ---------------------------------------------------------------- contexto: tokens e compactação

CARACTERES_POR_TOKEN = 3.0  # conservadora: o real no qwen fica entre 3,07 e 3,33 (calibrado contra o Ollama)
# teto do histórico nas chamadas da conversa: o orçamento acompanha o trabalho (livro 4.12.4: 2–3× o que cada passo
# precisa), não a janela inteira; prompts de 5–8 mil tokens custam minutos nesta GPU e pioram a atenção do modelo
ORCAMENTO_HISTORICO = 2500


def estimar_tokens(texto: str) -> int:
    return math.ceil(len(texto or '') / CARACTERES_POR_TOKEN)


_GOBR = re.compile(r'```gobr.*?```', re.S)
MARCA_ARQUIVO = '[arquivo GoBR desta versão; o arquivo atual está nas instruções]'


def filtrar_turno(texto: str, limite: int = 700) -> str:
    """Filtragem de resultados (livro 4.12.3): o arquivo GoBR de cada versão sai do histórico, porque o atual entra
    uma vez nas instruções; turnos longos são cortados."""
    t = _GOBR.sub(MARCA_ARQUIVO, texto or '')
    return t if len(t) <= limite else t[:limite].rstrip() + ' […]'


@dataclass
class Historico:
    mensagens: List[Dict[str, str]]  # alterna user/assistant, começa em user
    tokens: int
    compactados: int  # turnos retirados do meio
    resumo: str = ''


def _juntar(msgs: Sequence[Dict[str, str]]) -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    for m in msgs:
        if out and out[-1]['role'] == m['role']:
            out[-1] = {'role': m['role'], 'content': out[-1]['content'] + '\n\n' + m['content']}
        else:
            out.append(dict(m))
    if out and out[0]['role'] != 'user':
        out.insert(0, {'role': 'user', 'content': '(início da conversa)'})
    return out


def montar_historico(historico: Sequence[Dict[str, str]], orcamento: int, compactar: bool = True,
                     cabeca: int = 1) -> Historico:
    """Histórico da sessão como mensagens de chat, dentro de `orcamento` tokens.

    Compactação cabeça + cauda (livro 4.12.3, HeadTailCompaction): a cabeça (o pedido inicial) diz o que se está
    fazendo; a cauda (os turnos recentes) diz onde a conversa parou; o meio sai e fica um resumo de uma linha por
    pedido do analista, sem modelo (barato e sem risco de inventar). Sem `compactar`, vai tudo, com o texto inteiro:
    é a linha de base da avaliação.
    """
    msgs = [{'role': 'user' if h['papel'] == 'analista' else 'assistant', 'content': h['texto']} for h in historico]
    if not compactar:
        juntas = _juntar(msgs)
        return Historico(juntas, sum(estimar_tokens(m['content']) for m in juntas), 0)
    msgs = [{**m, 'content': filtrar_turno(m['content'], 1200 if i < cabeca else 700)} for i, m in enumerate(msgs)]
    cab, resto = msgs[:cabeca], msgs[cabeca:]
    usado = sum(estimar_tokens(m['content']) for m in cab)
    reserva_resumo = max(250, orcamento // 6)
    cauda: List[Dict[str, str]] = []
    for m in reversed(resto):
        t = estimar_tokens(m['content'])
        if usado + t + reserva_resumo > orcamento:
            break
        cauda.insert(0, m)
        usado += t
    retirados = resto[:len(resto) - len(cauda)]
    resumo = resumir_trecho(retirados, reserva_resumo) if retirados else ''
    if resumo:
        cab = cab[:-1] + [{**cab[-1], 'content': cab[-1]['content'] + '\n\n' + resumo}] if cab else \
            [{'role': 'user', 'content': resumo}]
    juntas = _juntar(cab + cauda)
    return Historico(juntas, sum(estimar_tokens(m['content']) for m in juntas), len(retirados), resumo)


# respostas curtas às perguntas da revisão e confirmações: não dizem nada sobre o que o analista pediu
_TRIVIAL = re.compile(r'^\s*(ok|okay|sim|s|n[aã]o|fim|aplica|[a-d]|\d+\s*[a-d]?\s*([,;]\s*\d+\s*[:a-d][^;]*)*'
                      r'(;?\s*o resto com as sugest\w+)?)\s*[.!]?\s*$', re.I)
_EVENTO_ARQUIVO = re.compile(r'Regras em GoBR|Versão \d+ do arquivo|Voltei à versão|' + re.escape(MARCA_ARQUIVO))


def resumir_trecho(retirados: Sequence[Dict[str, str]], limite: int) -> str:
    """Linha do tempo do trecho compactado, sem modelo: os pedidos do analista, numerados e em ordem, e os momentos
    em que o arquivo foi gerado ou mudou. Se não couber, saem os pedidos do meio (cabeça e cauda também aqui), para
    que o primeiro pedido, que costuma ser referido depois ("o que eu perguntei primeiro?"), não se perca. O número
    é a posição do pedido na conversa e não muda quando o meio sai: o modelo de 7B lê "1º" melhor do que a posição
    numa lista (visto na avaliação: com a lista sem números, ele respondeu a 14ª pergunta como a primeira)."""
    eventos: List[str] = []
    pedidos = 0
    for m in retirados:
        if m['role'] == 'user':
            if not _TRIVIAL.match(m['content']):
                pedidos += 1
                eventos.append(f'{pedidos}º pedido: "{m["content"][:80].replace(chr(10), " ").strip()}"')
        elif _EVENTO_ARQUIVO.search(m['content']) and (not eventos or eventos[-1] != '[arquivo gerado ou alterado]'):
            eventos.append('[arquivo gerado ou alterado]')
    if not eventos:
        return f'[{len(retirados)} turnos anteriores compactados]'

    def montar(itens: Sequence[str]) -> str:
        return (f'[{len(retirados)} turnos anteriores compactados. Linha do tempo desse trecho, em ordem (pedidos do '
                'analista numerados, entre aspas): ' + ' → '.join(itens) + ']')
    if estimar_tokens(montar(eventos)) <= limite:
        return montar(eventos)
    n = len(eventos)
    for manter in range(n - 1, 1, -1):
        ini = (manter + 1) // 2  # o começo tem prioridade: é ele que a cauda do histórico não cobre
        fim = manter - ini
        itens = eventos[:ini] + [f'(… {n - manter} itens omitidos …)'] + (eventos[n - fim:] if fim else [])
        if estimar_tokens(montar(itens)) <= limite:
            return montar(itens)
    return montar(eventos[:1] + [f'(… {n - 1} itens omitidos …)'])


def como_transcricao(h: Historico) -> str:
    return '\n'.join(f'{"Analista" if m["role"] == "user" else "Agente"}: {m["content"]}' for m in h.mensagens)


# ---------------------------------------------------------------- uso de tokens (telemetria)

def registrar_uso(backend: Any, entrada: int, saida: int) -> None:
    """Guarda os tokens de cada chamada (o Ollama informa prompt_eval_count e eval_count)."""
    uso = getattr(backend, 'uso', None)
    if isinstance(uso, list):
        uso.append({'etapa': getattr(backend, 'etapa', ''), 'entrada': entrada, 'saida': saida})
