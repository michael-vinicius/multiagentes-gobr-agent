# Geração de Explicações de Parametrizações GoBR

Atividade da disciplina de **Multiagentes**: geração de explicações (regras de negócio) a partir das parametrizações.

Este projeto converte cada bloco `parametros` escrito na DSL **GoBR** em uma explicação em linguagem de negócio, mantendo o bloco original para rastreabilidade. As explicações são a base para a etapa seguinte do projeto: embeddings, recuperação de exemplos semelhantes (RAG) e o agente conversacional.

## Resultado

| Item | Valor |
|---|---|
| Arquivos `.gobr` processados | 246 |
| Parametrizações convertidas | 1700 |
| Cláusulas não classificadas | 0 |
| Blocos marcados para revisão | 1 (`regra_032.gobr`: parêntese sem fechamento na fonte) |

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

Metodologia, decisões, validação e inconsistências encontradas estão em [docs/RELATORIO_ATIVIDADE.md](docs/RELATORIO_ATIVIDADE.md).

## Fluxo

```text
Arquivos .gobr
      ↓  separação dos blocos `parametros` (com junção de cláusulas em várias linhas)
Classificação das cláusulas: alvo · filtros temporais · condições · ações
      ↓  conversão da DSL para português de negócio
Explicação detalhada · explicação curta · texto para embedding
      ↓  validação estrutural (não corrige a fonte, apenas sinaliza)
data/  (JSONL completo · JSONL para embeddings · Markdown legível)
```

## Estrutura

```text
src/gerar_explicacoes_gobr.py                 gerador (somente biblioteca padrão do Python)
data/parametrizacoes_explicadas.jsonl         dataset completo: DSL original, alvo, condições, ações, explicações, validação
data/parametrizacoes_para_embeddings.jsonl    versão enxuta (id, arquivo, ordem, nome, texto) para indexação vetorial
data/parametrizacoes_explicadas.md            versão para leitura humana, agrupada por arquivo
docs/RELATORIO_ATIVIDADE.md                   relatório da atividade
```

## Como executar

Requer Python 3 (testado com 3.12) e nenhuma dependência externa.

```bash
python src/gerar_explicacoes_gobr.py <pasta_com_arquivos_gobr>
```

Por padrão as três saídas são gravadas em `data/`. Os caminhos podem ser trocados com `--jsonl`, `--md` e `--embeddings-jsonl`.

> Os arquivos `.gobr` de origem não fazem parte do repositório. O bloco original de cada parametrização está preservado no campo `dsl_original` do JSONL.
