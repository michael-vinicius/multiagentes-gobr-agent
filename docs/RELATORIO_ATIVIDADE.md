# Atividade — Geração de explicações (regras de negócio) a partir das parametrizações

## 1. Objetivo

Transformar cada bloco `parametros` dos arquivos GoBR em uma descrição de negócio legível e reutilizável como documento de recuperação semântica (RAG). A saída mantém a regra original para rastreabilidade e gera uma versão curta própria para embeddings.

## 2. Como foi feito

1. Foram lidos todos os arquivos `.gobr` da pasta `referencias/`.
2. Cada bloco `parametros "...":` foi separado individualmente, juntando as cláusulas quebradas em várias linhas (argumentos longos, alternativas com `ou` e opções de `preferencia` continuadas com `e`).
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

## 6. Revisão de qualidade das explicações

Uma revisão das 1700 saídas encontrou defeitos no gerador, que foram corrigidos antes de regenerar os dados:

| Defeito | Registros afetados | Correção |
|---|---|---|
| A explicação curta juntava sujeito e ação com ponto, e a ação ficava gramaticalmente atribuída ao cliente: “Clientes que são filiais. devem não agendar esses clientes.” | 1699 | Novo formato `<clientes>: <ações>.`, por exemplo “Clientes que são filiais: não agendar esses clientes.” |
| Opções de `preferencia` continuadas em linhas iniciadas por `e` (`preferencia nos dias uteis` / `e no sabado` / `e no domingo`) eram lidas como **condições** de seleção de clientes, o que mudava o sentido da regra | 5 | As continuações passam a fazer parte da ação de preferência |
| `frequencia de 1 dia` gerava “a cada 1 dias” | 11 | Concordância de número |
| Sem condições, o texto para embedding repetia o alvo (“Clientes da carteira X: … Alvo: clientes da carteira X.”) | 197 | “Alvo” só é acrescentado quando o texto começa pelas condições |

**Como a regeneração foi validada.** Os arquivos `.gobr` originais não estão no repositório, então os registros foram reconstruídos a partir do campo `dsl_original`, que guarda o bloco completo:

1. Com o código **anterior** às correções, a reconstrução reproduziu os três arquivos de `data/` byte a byte, o que prova que o `dsl_original` é suficiente para regenerar tudo.
2. Com o código corrigido, só mudaram os campos ligados aos defeitos acima (`explicacao_curta`, `texto_embedding` e, nos 16 registros dos itens 2 e 3, `acoes`, `condicoes` e `explicacao_detalhada`). Ids, ordem, alvos, DSL e validação ficaram idênticos.
3. O CLI foi executado de ponta a ponta sobre os 246 arquivos `.gobr` reconstruídos e produziu saída idêntica à da regeneração.

## 7. Arquivos de entrega

- `data/parametrizacoes_explicadas.jsonl`: dataset completo, com DSL original, metadados e explicações.
- `data/parametrizacoes_para_embeddings.jsonl`: versão enxuta pronta para a etapa de embeddings/RAG.
- `data/parametrizacoes_explicadas.md`: versão humana agrupada por arquivo.
- `src/gerar_explicacoes_gobr.py`: script reprodutível para gerar novamente as saídas (`python src/gerar_explicacoes_gobr.py <pasta_gobr>`).

## 8. Próximo passo

Indexar o campo `texto` de `parametrizacoes_para_embeddings.jsonl` com embeddings e armazenar os metadados (`arquivo`, `ordem_no_arquivo`, `nome_regra`, `id`). Durante a busca, recuperar os exemplos semanticamente mais próximos da regra descrita pelo usuário e usar o manual GoBR como uma segunda fonte de contexto para montar a resposta final.
