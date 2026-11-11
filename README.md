# Agente GoBR — Explicações e Indexação de Parametrizações

Projeto da disciplina de **Multiagentes**.

O objetivo final é um agente conversacional que recebe uma regra de negócio descrita em linguagem natural (por exemplo, “clientes sem compra há 90 dias devem ser visitados a cada 14 dias”) e ajuda a escrevê-la na DSL **GoBR**, usando como referência parametrizações reais já existentes.

Para isso o trabalho foi dividido em etapas:

| # | Etapa | Status | Relatório |
|---|---|---|---|
| 1 | Geração de explicações (regras de negócio) a partir das parametrizações | ✅ concluída | [docs/RELATORIO_ATIVIDADE.md](docs/RELATORIO_ATIVIDADE.md) |
| 2 | Indexação das explicações (embeddings + busca semântica) | ✅ concluída | [docs/RELATORIO_INDEXACAO.md](docs/RELATORIO_INDEXACAO.md) |
| 3 | Agente conversacional com RAG (exemplos + manual GoBR) | ⏳ próximo passo | — |

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
      ↓
Agente (etapa 3): monta a parametrização GoBR usando os exemplos recuperados
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
```

Na primeira execução o modelo de embeddings (≈ 220 MB) é baixado e fica em cache.

> Os arquivos `.gobr` de origem não fazem parte do repositório. O bloco original de cada parametrização está preservado no campo `dsl_original` do JSONL.

Para usar a busca dentro do agente:

```python
import sys
from pathlib import Path
sys.path.insert(0, 'src')
from buscar_explicacoes import IndiceExplicacoes

indice = IndiceExplicacoes(Path('index'), Path('data/parametrizacoes_explicadas.jsonl'))
for r in indice.buscar('não agendar clientes inadimplentes', k=3):
    print(r['score'], r['nome_regra'], r['dsl_original'])
```

## Estrutura do repositório

```text
data/    datasets gerados na etapa 1 (JSONL completo, JSONL para embeddings, Markdown)
docs/    relatórios de cada atividade
index/   índice vetorial gerado na etapa 2
src/     scripts de geração, indexação, busca e avaliação
```
