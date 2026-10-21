# Atividade — Geração de explicações (regras de negócio) a partir das parametrizações

## 1. Objetivo

Transformar cada bloco `parametros` dos arquivos GoBR em uma descrição de negócio legível e reutilizável como documento de recuperação semântica (RAG). A saída mantém a regra original para rastreabilidade e gera uma versão curta própria para embeddings.

## 2. Como foi feito

1. Foram lidos todos os arquivos `.gobr` da pasta `referencias/`.
2. Cada bloco `parametros "...":` foi separado individualmente.
3. As cláusulas foram classificadas em: alvo (`do time`, `da carteira`, `da segmentacao`), filtros temporais, condições (`quando`/`e`) e ações (`frequencia`, `preferencia`, `nao agendar`, `fixo`, `roteirizavel`, `sem choque`, `restrito`).
4. A DSL foi convertida para uma explicação em português comercial, preservando a semântica original.
5. Cada registro recebeu o bloco GoBR original, uma explicação curta, uma explicação detalhada, um texto próprio para embedding e campos de validação.
6. Foi feita validação estrutural mínima para não esconder problemas existentes na fonte.

## 3. Resultado

- Arquivos GoBR processados: **246**
- Parametrizações convertidas: **1700**
- Parametrizações convertidas sem cláusulas desconhecidas: **1700/1700**
- Blocos marcados para revisão: **1**

### Observação importante sobre ordem

O manual GoBR informa que clientes parametrizados por uma regra anterior não são reprocessados pelas regras seguintes. Portanto, a ordem dos blocos importa. As explicações geradas descrevem fielmente cada bloco e mantêm `arquivo` + `ordem_no_arquivo`, permitindo que o RAG recupere também o contexto sequencial quando necessário.

## 4. Exemplo de conversão

### regra_003__param_001 — Não agendar filiais

**Explicação:** Para clientes vinculados ao time “televendas”, considerar clientes que são filiais. Ação: não agendar esses clientes.

```gobr
parametros "Não agendar filiais":
    do time("televendas")
    quando cliente filial
    nao agendar
```

### regra_003__param_005 — Ative este prospect: nunca tirou pedido

**Explicação:** Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 14 dias.

```gobr
parametros "Ative este prospect: nunca tirou pedido":
    do time("televendas")
    quando no ciclo de vida prospect com a empresa
    frequencia de 14 dias
```

### regra_003__param_007 — Mantenha a regularidade de compra do cliente que teve pedido detectado nos últimos 30d e não foi visitado na semana anterior

**Explicação:** Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa entre 7 e 30 dias atrás. Ação: atender a cada 14 dias.

```gobr
parametros "Mantenha a regularidade de compra do cliente que teve pedido detectado nos últimos 30d e não foi visitado na semana anterior":
    do time("televendas")
    quando recencia de positivacao global entre 7 dias e 30 dias
    frequencia de 14 dias
```

## 5. Inconsistência encontrada na base

Foi encontrado **1 bloco que precisa de revisão**: `regra_032.gobr`, regra **Inativos Curva C (Norte e Nordeste - Corporativo/ Consumidor)**. O bloco possui parêntese aberto sem fechamento e não contém uma ação de parametrização reconhecível. O gerador não corrige esse conteúdo automaticamente; ele apenas o marca para revisão.

```gobr
parametros "Inativos Curva C (Norte e Nordeste - Corporativo/ Consumidor)":
    da carteira("norte_nordeste")
    quando ramo de atividade igual("CONS. FINAL"
```

## 6. Arquivos de entrega

- `parametrizacoes_explicadas.jsonl`: dataset completo, com DSL original, metadados e explicações.
- `parametrizacoes_para_embeddings.jsonl`: versão enxuta pronta para a etapa de embeddings/RAG.
- `parametrizacoes_explicadas.md`: versão humana agrupada por arquivo.
- `gerar_explicacoes_gobr.py`: script reprodutível para gerar novamente as saídas.

## 7. Próximo passo

Indexar o campo `texto` de `parametrizacoes_para_embeddings.jsonl` com embeddings e armazenar os metadados (`arquivo`, `ordem_no_arquivo`, `nome_regra`, `id`). Durante a busca, recuperar os exemplos semanticamente mais próximos da regra descrita pelo usuário e usar o manual GoBR como uma segunda fonte de contexto para montar a resposta final.
