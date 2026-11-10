"""Fluxo básico de RAG: recupera exemplos e trechos do manual e pede a um modelo de linguagem a regra GoBR.

    pedido ─┬─ exemplos (vetores + BM25) ─→ parametrizações parecidas (E1, E2, …)
            └─ manual   (vetores + BM25) ─→ trechos do manual        (M1, M2, …)
                        ↓
              prompt com o contexto numerado + pedido
                        ↓
              modelo de linguagem ─→ resposta com a regra em ```gobr``` e citações [E#]/[M#]
              (local via Ollama, padrão e gratuito; ou Claude via API Anthropic)
                        ↓
              conferência: estrutura, condições × catálogo (catalogo_gobr.py) e citações
                        ↓
              com problema: uma rodada de correção; vale a tentativa com menos problemas
"""
from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Protocol, Sequence, Tuple

from gerar_explicacoes_gobr import build_record, parse_blocks

if TYPE_CHECKING:
    from catalogo_gobr import Catalogo

BACKENDS = ('ollama', 'anthropic')
MODELO_LOCAL_PADRAO = 'qwen2.5:7b'
MODELO_PADRAO = 'claude-opus-5-5'
ESFORCO_PADRAO = 'medium'
MAX_TOKENS_PADRAO = 16000
# Com "default", uma recusa dos classificadores de segurança é refeita no modelo recomendado pela API.
BETA_FALLBACK = 'server-side-fallback-2026-07-01'

SYSTEM_PROMPT = """\
Você ajuda analistas comerciais a escrever regras de negócio na DSL GoBR (gorules) do Govendas.

Junto com cada pedido você recebe o contexto recuperado de duas fontes:
- exemplos (E1, E2, …): parametrizações reais, cada uma com a explicação em linguagem de negócio e a DSL original;
- manual (M1, M2, …): trechos do manual da linguagem, que é a referência de sintaxe.

Como responder:
- Escreva a regra usando só cláusulas que aparecem no manual ou nos exemplos recebidos, copiando a escrita delas. \
Os exemplos mostram como regras parecidas foram escritas; o manual é a referência: se ele trouxer uma cláusula \
própria para o pedido, use a do manual.
- Toda regra `parametros` começa pela fonte de clientes: do time(…), da carteira(…) ou da segmentacao(…). Os \
filtros (por exemplo curva A, inadimplentes) vêm depois, em `quando` ou `e`, nunca como nome da fonte.
- Se o contexto não trouxer uma cláusula para parte do pedido, não invente sintaxe nem valores: diga o que faltou \
e entregue apenas o que o contexto sustenta.
- Entregue só os blocos necessários (normalmente um bloco `parametros`). Inclua `version`, times ou carteiras \
apenas se o pedido for um arquivo completo.
- Nomes de times, carteiras ou segmentações que o pedido não informa ficam como espaço reservado entre aspas, \
por exemplo da carteira("<nome da carteira>").
- Cite entre colchetes a fonte de cada cláusula que você usar, como [M2] ou [E1, M3]. O analista usa as \
citações para conferir a regra, então toda resposta com regra precisa delas.

Responda em português, neste formato:

<uma ou duas frases dizendo o que a regra faz, com as citações> [E1, M2]

```gobr
parametros "<nome da regra>":
    da carteira("<nome da carteira>")
    quando <filtro>
    <ação>
```

Pontos de atenção:
- <suposição, ambiguidade ou algo que o analista precisa confirmar, com a fonte quando houver> [M1]

Omita "Pontos de atenção" se não houver nenhum.
"""


class Buscador(Protocol):
    def buscar(self, consulta: str, k: int) -> List[Dict]: ...


@dataclass(frozen=True)
class Exemplo:
    ref: str
    id: str
    nome_regra: str
    score: float
    explicacao: str
    dsl: str


@dataclass(frozen=True)
class Trecho:
    ref: str
    id: str
    secao: str
    titulo: str
    paginas: Tuple[int, ...]
    score: float
    texto: str


@dataclass
class Contexto:
    pergunta: str
    exemplos: List[Exemplo]
    trechos: List[Trecho]

    def refs(self) -> List[str]:
        return [e.ref for e in self.exemplos] + [t.ref for t in self.trechos]


@dataclass
class Resposta:
    texto: str
    blocos_gobr: List[str]
    citacoes: List[str]
    citacoes_invalidas: List[str]
    validacao: List[Dict[str, Any]]
    modelo: str
    stop_reason: str
    uso: Dict[str, int] = field(default_factory=dict)
    tentativas: int = 1
    tentativa_escolhida: int = 1
    problemas_por_tentativa: List[List[str]] = field(default_factory=list)

    @property
    def dsl_valida(self) -> bool:
        return bool(self.validacao) and all(v['status'] == 'ok' for v in self.validacao)


class ErroGeracao(RuntimeError):
    """O modelo não produziu uma resposta utilizável (falha de conexão, recusa, resposta truncada ou vazia)."""


# ---------------------------------------------------------------- recuperação

def _corpo_dsl(dsl: str) -> str:
    # o nome da regra (1ª linha) varia entre arquivos com o mesmo conteúdo; a comparação usa só as cláusulas
    return '\n'.join(l.strip() for l in dsl.splitlines()[1:] if l.strip())


class Recuperador:
    """Consulta os dois índices e devolve o contexto numerado que vai para o prompt."""

    def __init__(self, exemplos: Buscador, manual: Buscador, fator_candidatos: int = 4):
        if fator_candidatos < 1:
            raise ValueError('fator_candidatos deve ser >= 1')
        self.exemplos = exemplos
        self.manual = manual
        self.fator_candidatos = fator_candidatos

    def recuperar(self, pergunta: str, k_exemplos: int = 5, k_manual: int = 4) -> Contexto:
        pergunta = pergunta.strip()
        if not pergunta:
            raise ValueError('a pergunta está vazia')
        if k_exemplos < 0 or k_manual < 0:
            raise ValueError('k_exemplos e k_manual não podem ser negativos')
        return Contexto(pergunta, self._exemplos(pergunta, k_exemplos), self._trechos(pergunta, k_manual))

    def _exemplos(self, pergunta: str, k: int) -> List[Exemplo]:
        if k == 0:
            return []
        # 1700 parametrizações, mas só 1208 corpos distintos: a mesma regra aparece em vários arquivos.
        # Busca-se mais candidatos que o necessário para que as repetições não ocupem o contexto.
        vistos, out = set(), []
        for r in self.exemplos.buscar(pergunta, k * self.fator_candidatos):
            dsl = r.get('dsl_original') or ''
            corpo = _corpo_dsl(dsl)
            if r.get('status_validacao') != 'ok' or not corpo or corpo in vistos:
                continue
            vistos.add(corpo)
            out.append(Exemplo(f'E{len(out) + 1}', r['id'], r['nome_regra'], r['score'],
                               r.get('explicacao_detalhada') or '', dsl))
            if len(out) == k:
                break
        return out

    def _trechos(self, pergunta: str, k: int) -> List[Trecho]:
        if k == 0:
            return []
        return [Trecho(f'M{n}', r['id'], r['secao'], r['titulo'], tuple(r['paginas']), r['score'], r['texto'])
                for n, r in enumerate(self.manual.buscar(pergunta, k), 1)]


def carregar_recuperador(dir_indice: Path = Path('index'),
                         explicadas: Path = Path('data/parametrizacoes_explicadas.jsonl'),
                         dir_manual: Path = Path('index/manual'), hibrida: bool = True) -> Recuperador:
    """Carrega os dois índices. Com `hibrida` (padrão), cada um combina a busca vetorial com BM25."""
    from buscar_explicacoes import IndiceExplicacoes
    from buscar_manual import IndiceManual
    from busca_hibrida import BuscaHibrida

    if not (dir_manual / 'manifesto.json').exists():
        raise FileNotFoundError(f'índice do manual não encontrado em {dir_manual}; '
                                'gere com: python src/indexar_manual.py <caminho>/govendas-rules.pdf')
    exemplos, manual = IndiceExplicacoes(dir_indice, explicadas), IndiceManual(dir_manual)
    if not hibrida:
        return Recuperador(exemplos, manual)

    docs_exemplos = []
    for m in exemplos.metadados:
        c = exemplos.completos.get(m['id'], {})
        docs_exemplos.append({**m, 'explicacao_detalhada': c.get('explicacao_detalhada'),
                              'dsl_original': c.get('dsl_original'), '_texto': f"{c.get('texto_embedding', '')}\n"
                                                                              f"{c.get('dsl_original', '')}"})
    textos_exemplos = [d.pop('_texto') for d in docs_exemplos]
    return Recuperador(
        BuscaHibrida(exemplos.buscar, docs_exemplos, textos_exemplos),
        BuscaHibrida(manual.buscar, manual.chunks, [c['texto'] for c in manual.chunks]),
    )


# ---------------------------------------------------------------- prompt

def _attr(valor: Any) -> str:
    return str(valor).replace('&', '&amp;').replace('"', '&quot;')


def formatar_contexto(ctx: Contexto) -> str:
    partes = ['<exemplos>']
    for e in ctx.exemplos:
        partes += [f'<exemplo ref="{e.ref}" nome="{_attr(e.nome_regra)}" similaridade="{e.score:.3f}">',
                   f'<explicacao>{e.explicacao}</explicacao>', '<dsl>', e.dsl, '</dsl>', '</exemplo>']
    if not ctx.exemplos:
        partes.append('(nenhum exemplo recuperado)')
    partes += ['</exemplos>', '', '<manual>']
    for t in ctx.trechos:
        paginas = ', '.join(map(str, t.paginas))
        partes += [f'<trecho ref="{t.ref}" secao="{_attr(t.secao)}" paginas="{paginas}" '
                   f'similaridade="{t.score:.3f}">', t.texto, '</trecho>']
    if not ctx.trechos:
        partes.append('(nenhum trecho recuperado)')
    partes.append('</manual>')
    return '\n'.join(partes)


def montar_mensagem(ctx: Contexto) -> str:
    # contexto longo primeiro e o pedido no fim
    return f'<contexto>\n{formatar_contexto(ctx)}\n</contexto>\n\n<pedido>\n{ctx.pergunta}\n</pedido>'


# ---------------------------------------------------------------- pós-checagens

_BLOCO_RE = re.compile(r'```(?:gobr|gorules)[ \t]*\r?\n(.*?)```', re.S | re.I)
_CITACAO_RE = re.compile(r'\[\s*([EM]\d+(?:\s*[,;]\s*[EM]\d+)*)\s*\]')


def extrair_blocos_gobr(texto: str) -> List[str]:
    return [b.strip('\n') for b in _BLOCO_RE.findall(texto) if b.strip()]


def extrair_citacoes(texto: str) -> List[str]:
    """Referências citadas, na ordem da primeira ocorrência."""
    out: List[str] = []
    for grupo in _CITACAO_RE.findall(texto):
        for ref in re.split(r'\s*[,;]\s*', grupo):
            if ref not in out:
                out.append(ref)
    return out


def validar_dsl(dsl: str, catalogo: Optional[Catalogo] = None) -> List[Dict[str, Any]]:
    """Validação de cada bloco `parametros`, com o mesmo classificador de cláusulas da etapa 1.

    Verifica parênteses, a presença da fonte de clientes (`do time`, `da carteira` ou `da segmentacao`, o 1º passo
    de uma regra de parâmetros no manual, presente nas 1700 regras reais) e de uma ação, e se toda cláusula tem um
    tipo conhecido (alvo, condição, filtro temporal ou ação). Com o `catalogo`, também confere cada condição contra
    as regras reais e o manual e acusa filtro usado como nome de fonte (ver catalogo_gobr.py). Não é um parser da
    gramática: os valores e as ações não são conferidos. Blocos de outros tipos (time, carteira…) não são validados.
    """
    blocos = [b for b in parse_blocks(dsl) if b['type'] == 'parametros']
    if not blocos:
        return [{'bloco': None, 'status': 'sem_bloco_parametros',
                 'problemas': ['nenhum bloco `parametros "<nome>":` encontrado'], 'clausulas_nao_classificadas': []}]
    out = []
    for i, b in enumerate(blocos, 1):
        r = build_record('resposta', i, b)
        problemas = list(r['problemas_validacao'])
        if not r['alvo']:
            problemas.insert(0, 'nenhuma fonte de clientes (do time / da carteira / da segmentacao)')
        # citações e comentários no estilo de outras linguagens não fazem parte do GoBR (comentário é `#`)
        corpo = re.sub(r'"[^"\n]*"', '""', '\n'.join(b['raw_lines']))
        if _CITACAO_RE.search(corpo) or '//' in corpo:
            problemas.append('citação ou comentário dentro da regra; as citações ficam no texto, fora do bloco ```gobr')
        if catalogo is not None:
            problemas += catalogo.problemas(b['clauses'])
        out.append({'bloco': r['nome_regra'], 'status': 'revisao_necessaria' if problemas else 'ok',
                    'problemas': problemas, 'clausulas_nao_classificadas': r['clausulas_nao_classificadas']})
    return out


# ---------------------------------------------------------------- geração

@dataclass
class SaidaModelo:
    texto: str
    modelo: str
    stop_reason: str
    uso: Dict[str, int]
    # conteúdo do turno do assistente no formato do provedor, para reenviar na rodada de correção. No Claude ele
    # inclui os blocos de raciocínio, que precisam voltar sem alteração; sem ele, reenvia-se só o texto.
    conteudo_assistente: Any = None


Mensagens = List[Dict[str, Any]]


class Backend(Protocol):
    def completar(self, system: str, mensagens: Mensagens) -> SaidaModelo:
        """`mensagens` alterna user/assistant e termina numa mensagem do usuário."""
        ...


def _post_json(url: str, payload: Dict, timeout: float) -> Dict:
    req = urllib.request.Request(url, json.dumps(payload).encode('utf-8'), {'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode('utf-8'))


class BackendOllama:
    """Modelo local servido pelo Ollama (gratuito, sem chave). Padrão do fluxo."""

    def __init__(self, modelo: str = MODELO_LOCAL_PADRAO, url: str = 'http://127.0.0.1:11434',
                 num_ctx: int = 8192, max_tokens: int = 2048, timeout: float = 900,
                 transporte: Callable[[str, Dict, float], Dict] = _post_json):
        self.modelo, self.url, self.num_ctx = modelo, url.rstrip('/'), num_ctx
        self.max_tokens, self.timeout, self.transporte = max_tokens, timeout, transporte

    def completar(self, system: str, mensagens: Mensagens) -> SaidaModelo:
        payload = {
            'model': self.modelo,
            'messages': [{'role': 'system', 'content': system}, *mensagens],
            'stream': False,
            # temperatura 0: a mesma sequência de chamadas reproduz as respostas (o cache de prompt do Ollama pode
            # mudá-las quando a sequência muda; ver o relatório). num_ctx explícito: o padrão do Ollama é pequeno
            'options': {'num_ctx': self.num_ctx, 'num_predict': self.max_tokens, 'temperature': 0},
        }
        try:
            r = self.transporte(f'{self.url}/api/chat', payload, self.timeout)
        except urllib.error.HTTPError as e:
            raise ErroGeracao(f'o Ollama respondeu {e.code}: {e.read().decode("utf-8", "replace")[:300]}') from e
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            raise ErroGeracao(f'sem conexão com o Ollama em {self.url} ({e}); ele está rodando?') from e

        entrada, saida = r.get('prompt_eval_count', 0), r.get('eval_count', 0)
        # o Ollama corta o início do prompt sem avisar quando ele não cabe em num_ctx
        if entrada + saida >= self.num_ctx:
            raise ErroGeracao(f'o prompt ({entrada} tokens) não coube na janela num_ctx={self.num_ctx}')
        if r.get('done_reason') == 'length':
            raise ErroGeracao(f'resposta truncada em max_tokens={self.max_tokens}')
        return SaidaModelo((r.get('message') or {}).get('content', ''), r.get('model', self.modelo),
                           r.get('done_reason', ''), {'input_tokens': entrada, 'output_tokens': saida})


class BackendAnthropic:
    """Claude pela API Anthropic (pago; exige ANTHROPIC_API_KEY)."""

    def __init__(self, client: Any = None, modelo: str = MODELO_PADRAO, esforco: str = ESFORCO_PADRAO,
                 max_tokens: int = MAX_TOKENS_PADRAO):
        if client is None:
            import anthropic
            client = anthropic.Anthropic()
        self.client, self.modelo, self.esforco, self.max_tokens = client, modelo, esforco, max_tokens

    def completar(self, system: str, mensagens: Mensagens) -> SaidaModelo:
        import anthropic
        try:
            msg = self.client.beta.messages.create(
                model=self.modelo,
                max_tokens=self.max_tokens,
                system=system,
                messages=list(mensagens),
                output_config={'effort': self.esforco},
                betas=[BETA_FALLBACK],
                fallbacks='default',
            )
        except anthropic.AuthenticationError as e:
            raise ErroGeracao('credencial da API Anthropic inválida ou ausente (defina ANTHROPIC_API_KEY)') from e
        except anthropic.APIStatusError as e:
            raise ErroGeracao(f'erro da API Anthropic ({e.status_code}): {e.message}') from e
        except anthropic.APIConnectionError as e:
            raise ErroGeracao('sem conexão com a API Anthropic') from e
        if msg.stop_reason == 'refusal':
            detalhe = getattr(msg, 'stop_details', None)
            categoria = getattr(detalhe, 'category', None) if detalhe else None
            raise ErroGeracao(f'o modelo recusou o pedido (categoria: {categoria or "não informada"})')
        if msg.stop_reason == 'max_tokens':
            raise ErroGeracao(f'resposta truncada em max_tokens={self.max_tokens}')
        texto = ''.join(b.text for b in msg.content if b.type == 'text')
        return SaidaModelo(texto, msg.model, msg.stop_reason,
                           {'input_tokens': msg.usage.input_tokens, 'output_tokens': msg.usage.output_tokens},
                           conteudo_assistente=msg.content)


def problemas_da_resposta(resp: Resposta) -> List[str]:
    """O que impede usar a resposta como está, em frases que o próprio modelo consegue corrigir."""
    out: List[str] = []
    if not resp.blocos_gobr:
        out.append('a resposta não traz a regra num bloco ```gobr')
    for v in resp.validacao:
        out += [p for p in v['problemas'] if p != 'há cláusulas não classificadas automaticamente']
        out += [f'cláusula que não é fonte, condição, filtro temporal nem ação conhecida: "{c}"'
                for c in v['clausulas_nao_classificadas']]
    if resp.citacoes_invalidas:
        out.append(f'cita fontes que não existem no contexto: {", ".join(resp.citacoes_invalidas)}')
    if resp.blocos_gobr and not resp.citacoes:
        out.append('não cita as fontes ([E#] ou [M#]) das cláusulas usadas')
    return out


def montar_correcao(problemas: Sequence[str]) -> str:
    itens = '\n'.join(f'- {p}' for p in problemas)
    return (f'A regra foi conferida contra o manual e as regras reais e tem estes problemas:\n{itens}\n\n'
            'Corrija usando só cláusulas que aparecem no contexto, com a mesma escrita. Se o contexto não tiver '
            'cláusula para parte do pedido, diga isso nos pontos de atenção em vez de inventar. As citações ficam '
            'no texto, fora do bloco ```gobr, que deve conter só a regra, sem comentários. '
            'Responda de novo por completo, no mesmo formato.')


class Gerador:
    """Envia o contexto ao modelo, confere a resposta e, se houver problemas, pede uma correção.

    Com `max_tentativas=2` (padrão), uma resposta com problemas (regra ausente, validação, citações) volta ao
    modelo uma vez, com a lista do que corrigir. Devolve a tentativa com menos problemas (no empate, a mais
    recente): a correção às vezes piora a resposta, e ela nunca deve sair pior do que a primeira. Os problemas que
    sobrarem continuam visíveis em `validacao`, `citacoes_invalidas` e `problemas_por_tentativa`.
    """

    def __init__(self, backend: Backend, catalogo: Optional[Catalogo] = None, max_tentativas: int = 2):
        if max_tentativas < 1:
            raise ValueError('max_tentativas deve ser >= 1')
        self.backend, self.catalogo, self.max_tentativas = backend, catalogo, max_tentativas

    def _interpretar(self, ctx: Contexto, saida: SaidaModelo) -> Resposta:
        texto = saida.texto.strip()
        if not texto:
            raise ErroGeracao(f'resposta sem texto (stop_reason={saida.stop_reason})')
        blocos = extrair_blocos_gobr(texto)
        citacoes = extrair_citacoes(texto)
        validas = set(ctx.refs())
        validacao = [v for b in blocos for v in validar_dsl(b, self.catalogo)]
        return Resposta(texto, blocos, citacoes, [c for c in citacoes if c not in validas], validacao,
                        saida.modelo, saida.stop_reason, dict(saida.uso))

    def gerar(self, ctx: Contexto) -> Resposta:
        mensagens: Mensagens = [{'role': 'user', 'content': montar_mensagem(ctx)}]
        uso = {'input_tokens': 0, 'output_tokens': 0}
        historico: List[List[str]] = []
        respostas: List[Resposta] = []
        for tentativa in range(1, self.max_tentativas + 1):
            saida = self.backend.completar(SYSTEM_PROMPT, mensagens)
            for chave in uso:
                uso[chave] += saida.uso.get(chave, 0)
            resp = self._interpretar(ctx, saida)
            problemas = problemas_da_resposta(resp)
            respostas.append(resp)
            historico.append(problemas)
            if not problemas or tentativa == self.max_tentativas:
                break
            conteudo = saida.conteudo_assistente if saida.conteudo_assistente is not None else resp.texto
            mensagens += [{'role': 'assistant', 'content': conteudo},
                          {'role': 'user', 'content': montar_correcao(problemas)}]
        # menos problemas vence; no empate, a mais recente
        escolhida = min(range(len(respostas)), key=lambda i: (len(historico[i]), -i))
        melhor = respostas[escolhida]
        melhor.uso, melhor.tentativas, melhor.tentativa_escolhida = uso, len(respostas), escolhida + 1
        melhor.problemas_por_tentativa = historico
        return melhor


def criar_backend(nome: str, modelo: Optional[str] = None, esforco: str = ESFORCO_PADRAO) -> Backend:
    if nome == 'ollama':
        return BackendOllama(modelo or MODELO_LOCAL_PADRAO)
    if nome == 'anthropic':
        return BackendAnthropic(modelo=modelo or MODELO_PADRAO, esforco=esforco)
    raise ValueError(f'backend desconhecido: {nome}')


def responder(pergunta: str, recuperador: Recuperador, gerador: Gerador,
              k_exemplos: int = 5, k_manual: int = 4) -> Tuple[Contexto, Resposta]:
    ctx = recuperador.recuperar(pergunta, k_exemplos, k_manual)
    return ctx, gerador.gerar(ctx)


# ---------------------------------------------------------------- linha de comando

def _imprimir(ctx: Contexto, resp: Resposta) -> None:
    print(resp.texto)
    print('\n' + '─' * 72)
    citadas = set(resp.citacoes)
    for e in ctx.exemplos:
        print(f'{"*" if e.ref in citadas else " "} {e.ref} [{e.score:.3f}] {e.id} — {e.nome_regra}')
    for t in ctx.trechos:
        print(f'{"*" if t.ref in citadas else " "} {t.ref} [{t.score:.3f}] {t.titulo} — p. {", ".join(map(str, t.paginas))}')
    print('  (* = citado na resposta)')
    if resp.citacoes_invalidas:
        print(f'! citações sem fonte correspondente: {", ".join(resp.citacoes_invalidas)}')
    if not resp.blocos_gobr:
        print('! a resposta não trouxe bloco ```gobr')
    for v in resp.validacao:
        detalhe = '' if v['status'] == 'ok' else ' — ' + '; '.join(v['problemas'] + v['clausulas_nao_classificadas'])
        print(f'validação {v["bloco"] or "-"}: {v["status"]}{detalhe}')
    if resp.tentativas > 1:
        print(f'{resp.tentativas} tentativas, usada a {resp.tentativa_escolhida}ª; problemas da 1ª: '
              + '; '.join(resp.problemas_por_tentativa[0]))
    print(f'modelo {resp.modelo} · {resp.uso.get("input_tokens")} tokens de entrada, '
          f'{resp.uso.get("output_tokens")} de saída')


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description='Escreve uma regra GoBR a partir de uma descrição em linguagem natural, '
                                             'usando exemplos e o manual recuperados (RAG).')
    ap.add_argument('pergunta', help='Regra de negócio ou dúvida em linguagem natural')
    ap.add_argument('-k', '--k-exemplos', type=int, default=5, help='Exemplos de parametrizações no contexto')
    ap.add_argument('--k-manual', type=int, default=4, help='Trechos do manual no contexto')
    ap.add_argument('--backend', default='ollama', choices=BACKENDS,
                    help='ollama: modelo local e gratuito (padrão); anthropic: Claude pela API, pago')
    ap.add_argument('--modelo', help=f'Padrão: {MODELO_LOCAL_PADRAO} (ollama) ou {MODELO_PADRAO} (anthropic)')
    ap.add_argument('--esforco', default=ESFORCO_PADRAO, choices=['low', 'medium', 'high', 'xhigh', 'max'],
                    help='Só para o backend anthropic')
    ap.add_argument('--indice', type=Path, default=Path('index'))
    ap.add_argument('--explicadas', type=Path, default=Path('data/parametrizacoes_explicadas.jsonl'))
    ap.add_argument('--indice-manual', type=Path, default=Path('index/manual'))
    ap.add_argument('--busca', choices=['hibrida', 'vetorial'], default='hibrida',
                    help='hibrida: vetores + BM25 (padrão); vetorial: só vetores')
    ap.add_argument('--tentativas', type=int, default=2,
                    help='Rodadas de geração: com 2 (padrão), uma resposta com problemas volta ao modelo uma vez')
    ap.add_argument('--sem-catalogo', action='store_true',
                    help='Não confere as condições contra o catálogo de cláusulas reais e do manual')
    ap.add_argument('--so-contexto', action='store_true', help='Mostra o prompt montado sem chamar o modelo')
    ap.add_argument('--json', action='store_true', help='Imprime contexto e resposta em JSON')
    args = ap.parse_args(argv)

    recuperador = carregar_recuperador(args.indice, args.explicadas, args.indice_manual, args.busca == 'hibrida')
    ctx = recuperador.recuperar(args.pergunta, args.k_exemplos, args.k_manual)
    if args.so_contexto:
        print(f'[system]\n{SYSTEM_PROMPT}\n[user]\n{montar_mensagem(ctx)}')
        return 0

    try:
        from catalogo_gobr import carregar_catalogo
        catalogo = None if args.sem_catalogo else carregar_catalogo(args.explicadas, args.indice_manual / 'chunks.jsonl')
        resp = Gerador(criar_backend(args.backend, args.modelo, args.esforco), catalogo, args.tentativas).gerar(ctx)
    except ErroGeracao as e:
        print(f'erro: {e}')
        return 1

    if args.json:
        print(json.dumps({'contexto': asdict(ctx), 'resposta': asdict(resp)}, ensure_ascii=False, indent=2))
    else:
        _imprimir(ctx, resp)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
