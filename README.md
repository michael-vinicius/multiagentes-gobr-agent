# Agente GoBR — Explicações e Indexação de Parametrizações

Projeto da disciplina de **Multiagentes**.

O objetivo final é um agente conversacional que recebe uma regra de negócio descrita em linguagem natural (por exemplo, “clientes sem compra há 90 dias devem ser visitados a cada 14 dias”) e ajuda a escrevê-la na DSL **GoBR**, usando como referência parametrizações reais já existentes.

Para isso o trabalho foi dividido em etapas:

| # | Etapa | Status | Relatório |
|---|---|---|---|
| 1 | Geração de explicações (regras de negócio) a partir das parametrizações | ✅ concluída | [docs/RELATORIO_ATIVIDADE.md](docs/RELATORIO_ATIVIDADE.md) |
| 2 | Indexação das explicações (embeddings + busca semântica) | ✅ concluída | [docs/RELATORIO_INDEXACAO.md](docs/RELATORIO_INDEXACAO.md) |
| 3 | Indexação do manual GoBR (extração do PDF + chunks + busca semântica) | ✅ concluída | [docs/RELATORIO_INDEXACAO_MANUAL.md](docs/RELATORIO_INDEXACAO_MANUAL.md) |
| 4 | Fluxo básico de busca com RAG (exemplos + manual → regra GoBR com o Claude) | ✅ concluída | [docs/RELATORIO_RAG.md](docs/RELATORIO_RAG.md) |
| 5 | Agente conversacional | ⏳ próximo passo | — |

## Fluxo completo

```text
Arquivos .gobr (246)
      ↓  src/gerar_explicacoes_gobr.py
Separação dos blocos `parametros` → alvo, filtros temporais, condições, ações
      ↓
Explicação em linguagem de negócio + validação          (1700 parametrizações)
      ↓
data/parametrizacoes_explicadas.jsonl                   (dataset completo, com DSL original)
data/parametrizacoes_para_embeddings.jsonl              (versão enxuta: id + texto)
      ↓  src/indexar_explicacoes.py
Embeddings multilíngues (384 dim, cosseno)
      ↓
index/                                                  (vetores + metadados + manifesto)
      ↓  src/buscar_explicacoes.py
Consulta em linguagem natural → top-k parametrizações semelhantes (+ blocos vizinhos)

Manual GoBR (govendas-rules.pdf, 62 páginas)
      ↓  src/extrair_manual.py
Títulos, texto, blocos de código e tabelas → 1 chunk por seção (seções longas divididas sem cortar código nem linhas de tabela)
      ↓  src/indexar_manual.py
Embeddings multilíngues para recuperação (1024 dim, cosseno)
      ↓
index/manual/                                           (gerado localmente, fora do repositório)
      ↓  src/buscar_manual.py
Pergunta em linguagem natural → top-k trechos do manual (seção, páginas, texto)

Regra de negócio em linguagem natural
      ↓  src/rag.py
Recuperação nos dois índices → exemplos (E1…E5, sem duplicatas) + trechos do manual (M1…M4)
      ↓
Prompt com o contexto numerado → modelo de linguagem (local via Ollama, gratuito; ou Claude pela API)
      ↓
Regra em ```gobr``` com citações [E#]/[M#] + checagem das citações e validação estrutural da DSL
```

## Etapa 1 — Explicações

Cada bloco `parametros` dos arquivos GoBR foi convertido em uma explicação curta, uma explicação detalhada e um texto próprio para embedding, mantendo a DSL original para rastreabilidade.

- 246 arquivos processados, 1700 parametrizações convertidas, nenhuma cláusula desconhecida.
- 1 bloco marcado para revisão (`regra_032.gobr`, parêntese sem fechamento na fonte).

Exemplo:

```gobr
parametros "Não agendar filiais":
    do time("televendas")
    quando cliente filial
    nao agendar
```

| Campo | Conteúdo gerado |
|---|---|
| `explicacao_detalhada` | Para clientes vinculados ao time “televendas”, considerar clientes que são filiais. Ação: não agendar esses clientes. |
| `explicacao_curta` | Clientes que são filiais: não agendar esses clientes. |
| `texto_embedding` | Não agendar filiais. Clientes que são filiais: não agendar esses clientes. Alvo: clientes vinculados ao time “televendas”. |

## Etapa 2 — Indexação

O campo `texto` das 1700 explicações foi transformado em vetores com o modelo `paraphrase-multilingual-MiniLM-L12-v2`, executado localmente (sem GPU e sem chave de API). A busca compara a consulta do usuário com todos os vetores pela similaridade de cosseno e devolve as regras mais próximas, com a DSL original.

- 1700/1700 textos indexados (≈ 2,9 MB).
- Avaliação com 12 consultas de referência: **8/12 acertos no 1º lugar e 9/12 no top-5**.
- Limitações conhecidas: negação (“atender” × “não agendar”), valores abreviados (`CONS. FINAL`) e intervalos e frequências numéricos. As melhorias propostas estão no relatório.

## Etapa 3 — Indexação do manual

O manual em PDF é extraído preservando a estrutura (títulos, parágrafos, blocos de código com indentação e tabelas célula a célula) e quebrado em um chunk por seção. Seções maiores que a janela do modelo são divididas entre parágrafos, exemplos ou linhas de tabela, repetindo o caminho de títulos e o cabeçalho da tabela.

- 95 seções, 99 chunks (mediana de 193 tokens, máximo de 498).
- Modelo `multilingual-e5-large` (512 tokens): o MiniLM da etapa 2 trunca em 128 tokens, e 72 das 90 seções passariam disso.
- Avaliação com 24 consultas de referência: **21/24 acertos no 1º lugar e 24/24 no top-5** (o mpnet, nas mesmas condições, ficou em 8/24 e 14/24).
- O manual tem direitos reservados e o repositório é público: o PDF e o índice gerado (`index/manual/`) não são versionados. O índice é gerado localmente a partir do PDF.

## Etapa 4 — Fluxo básico de busca (RAG)

`src/rag.py` liga as duas buscas a um modelo de linguagem. A pergunta do usuário consulta os dois índices; os exemplos repetidos são descartados (as 1700 parametrizações têm só 1208 corpos distintos); o contexto vai para o modelo numerado (`E1…` para exemplos, `M1…` para o manual), e a resposta volta com a regra num bloco `gobr`, as fontes citadas e os pontos de atenção. Antes de devolver, o fluxo confere se as citações existem no contexto e valida a estrutura da DSL com o mesmo classificador de cláusulas da etapa 1.

A geração é plugável. O padrão é um modelo **local e gratuito** (`qwen2.5:7b` via [Ollama](https://ollama.com)), sem chave e sem custo. O Claude (`claude-opus-5-5`, pela API Anthropic) é a opção paga: `--backend anthropic`.

- 65 testes automatizados (`pytest`): 57 unitários, sem rede nem modelos, e 8 de integração com os índices reais. Um deles é um `xfail` estrito que registra uma limitação conhecida do índice de exemplos.
- Avaliação ponta a ponta com 6 pedidos de referência (`src/avaliar_rag.py`), com o modelo local: a busca leva as cláusulas necessárias ao contexto em 4 de 6 casos, e **2 de 6** regras geradas saem completamente certas (sintaxe, validação e citações). O gargalo é o modelo de 7B, que erra a semântica mesmo com o material certo no contexto. Detalhes e limitações no [relatório](docs/RELATORIO_RAG.md).

## Como executar

Requer Python 3.10+.

```bash
python -m venv .venv
.venv/Scripts/activate            # Windows  (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt

# Etapa 1 — gerar explicações (precisa da pasta com os arquivos .gobr; as saídas vão para data/)
python src/gerar_explicacoes_gobr.py <pasta_com_arquivos_gobr>

# Etapa 2 — gerar o índice
python src/indexar_explicacoes.py

# Buscar regras semelhantes
python src/buscar_explicacoes.py "clientes sem comprar há mais de 90 dias" -k 5 --contexto 1

# Avaliar a qualidade da busca
python src/avaliar_busca.py

# Etapa 3 — gerar o índice do manual (precisa do govendas-rules.pdf)
python src/indexar_manual.py <caminho>/govendas-rules.pdf

# Buscar no manual e avaliar
python src/buscar_manual.py "como evitar que televendas e campo atendam o cliente no mesmo dia" -k 3
python src/avaliar_busca_manual.py

# Etapa 4 — RAG (precisa dos dois índices)
# modelo local, gratuito: instale o Ollama (Windows: winget install Ollama.Ollama) e baixe o modelo (~4,7 GB)
ollama pull qwen2.5:7b
python src/rag.py "clientes inadimplentes não devem ser agendados"
python src/rag.py "clientes inadimplentes não devem ser agendados" --so-contexto   # só mostra o prompt montado
python src/avaliar_rag.py

# alternativa paga: Claude pela API (defina ANTHROPIC_API_KEY)
python src/rag.py "clientes inadimplentes não devem ser agendados" --backend anthropic

# Testes (os de integração são pulados se o índice do manual não existir)
pip install -r requirements-dev.txt
python -m pytest
```

Na primeira execução os modelos de embeddings são baixados e ficam em cache (≈ 220 MB para as explicações e ≈ 2,2 GB para o manual).

> Os arquivos `.gobr` de origem não fazem parte do repositório. O bloco original de cada parametrização está preservado no campo `dsl_original` do JSONL.

Para usar a busca dentro do agente:

```python
import sys
from pathlib import Path
sys.path.insert(0, 'src')
from buscar_explicacoes import IndiceExplicacoes
from buscar_manual import IndiceManual

indice = IndiceExplicacoes(Path('index'), Path('data/parametrizacoes_explicadas.jsonl'))
for r in indice.buscar('não agendar clientes inadimplentes', k=3):
    print(r['score'], r['nome_regra'], r['dsl_original'])

manual = IndiceManual(Path('index/manual'))
for r in manual.buscar('filtro para clientes inadimplentes', k=2):
    print(r['score'], r['secao'], r['titulo'], r['texto'])

from rag import carregar_recuperador, criar_backend, Gerador, responder
ctx, resp = responder('não agendar clientes inadimplentes', carregar_recuperador(), Gerador(criar_backend('ollama')))
print(resp.texto, resp.blocos_gobr, resp.citacoes, resp.dsl_valida)
```

## Estrutura do repositório

```text
data/           datasets gerados na etapa 1 (JSONL completo, JSONL para embeddings, Markdown)
docs/           relatórios de cada atividade
index/          índice vetorial das explicações (etapa 2)
index/manual/   índice do manual (etapa 3), gerado localmente e fora do controle de versão
src/            scripts de geração, extração, indexação, busca, RAG e avaliação
tests/          testes automatizados (pytest)
```
