# Atividade — Indexação das explicações

## 1. Objetivo

Transformar as 1700 explicações de regras de negócio geradas na atividade anterior em um índice vetorial pesquisável. Com ele, dada uma regra descrita em linguagem natural pelo usuário, o agente recupera as parametrizações GoBR semanticamente mais próximas, que servem de exemplo (RAG) para montar a resposta.

## 2. Como foi feito

1. **Entrada:** o campo `texto` de `data/parametrizacoes_para_embeddings.jsonl`, que já combina nome da regra, condições, ações e alvo em uma frase de negócio.
2. **Validação prévia:** antes de gerar vetores, o script verifica ids duplicados e textos vazios e interrompe a execução se encontrar algum, para não produzir um índice incompleto sem aviso.
3. **Embeddings:** cada texto foi convertido em um vetor de 384 dimensões com o modelo multilíngue `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, executado localmente via [fastembed](https://github.com/qdrant/fastembed) (ONNX, sem GPU e sem chave de API).
4. **Normalização:** os vetores foram normalizados (norma 1), de modo que a similaridade de cosseno equivale a um simples produto escalar.
5. **Armazenamento:** vetores e metadados foram salvos em `index/`, alinhados linha a linha, junto com um manifesto que registra o modelo usado e o hash SHA-256 da fonte.
6. **Busca:** a consulta do usuário passa pelo mesmo modelo, e as `k` parametrizações com maior similaridade são devolvidas com a explicação detalhada e a DSL original.
7. **Contexto sequencial:** como no GoBR a ordem dos blocos importa (um cliente capturado por uma regra anterior não é reprocessado pelas seguintes), a busca pode devolver também os blocos vizinhos do mesmo arquivo (`--contexto N`).

### Por que um índice em arquivo, e não um banco vetorial

Com 1700 vetores de 384 dimensões (≈ 2,6 MB), uma busca exaustiva por produto escalar em NumPy leva milissegundos. Um banco vetorial (Chroma, FAISS, Qdrant) só traria ganho com centenas de milhares de vetores. O formato atual é simples de versionar, inspecionar e migrar depois, se o volume crescer.

## 3. Resultado

| Item | Valor |
|---|---|
| Textos indexados | **1700/1700** |
| Modelo | `paraphrase-multilingual-MiniLM-L12-v2` |
| Dimensão | 384 |
| Métrica | cosseno |
| Tamanho do índice | ≈ 2,9 MB |

### Estrutura do índice

```text
index/
├── embeddings.npy     # matriz float32 (1700 × 384), vetores normalizados
├── metadados.jsonl    # id, arquivo, ordem_no_arquivo, nome_regra, status_validacao (mesma ordem dos vetores)
└── manifesto.json     # modelo, dimensão, total, hash da fonte, data de geração
```

O hash da fonte no manifesto permite detectar quando `parametrizacoes_para_embeddings.jsonl` mudou e o índice precisa ser gerado novamente. Foi o que aconteceu depois da revisão de qualidade da etapa 1, que mudou o formato da explicação curta e do texto para embedding: o índice foi gerado de novo a partir dos textos corrigidos, e todos os resultados deste relatório são do índice atual.

## 4. Exemplos de busca

**Consulta:** “cliente sem comprar há mais de 90 dias deve ser visitado mensalmente”

```text
1. [0.862] regra_165__param_002 — Clientes há mais de 90 dias sem compra
   | do time("televendas")
   | quando fora da recencia de positivacao em 90 dias
   | frequencia de 7 dias
2. [0.823] regra_235__param_007 — Clientes sem compra em 90 dias
   | do time("felipe")
   | frequencia de 10 dias
   | preferencia nos dias uteis e no sabado
3. [0.797] regra_227__param_005 — Freq. de 10d para clientes sem compra em 90 dias (Inativos)
   | do time("felipe")
   | frequencia de 10 dias
```

O 1º resultado tem exatamente a condição pedida (sem positivação em 90 dias). O 2º e o 3º foram recuperados pelo **nome da regra**, que entra no texto de embedding: a DSL deles não tem a condição de 90 dias, que fica implícita no time `felipe`. São exemplos úteis de frequência e preferência, mas o agente deve conferir a DSL e não confiar só no nome.

**Consulta com contexto sequencial:** “visitar prospects que nunca compraram a cada duas semanas” `-k 3 --contexto 1`

```text
1. [0.609] regra_228__param_004 — Compra com regularidade! (Curva A e B)
2. [0.604] regra_003__param_006 — Prospect ativado: fez um pedido e não comprou mais
   ↳ vizinho #5: Ative este prospect: nunca tirou pedido
   ↳ vizinho #7: Mantenha a regularidade de compra do cliente que teve pedido detectado...
3. [0.597] regra_215__param_002 — Freq. de 7d para 'Prospect ativado'
```

A regra mais adequada (#5 do `regra_003`, prospect com frequência de 14 dias) não ficou no top-3, mas apareceu como vizinha do 2º resultado, o que mostra o valor de recuperar também o contexto do arquivo.

## 5. Avaliação

Foi criado um conjunto de 12 consultas de referência (`src/avaliar_busca.py`). Como existem regras equivalentes em vários arquivos, um resultado conta como acerto quando a DSL recuperada contém o padrão esperado (por exemplo, `fora da recencia de positivacao em 90 dias`), e não quando bate um id específico.

| Modelo | Tamanho | Acerto@1 | Acerto@5 |
|---|---|---|---|
| `paraphrase-multilingual-MiniLM-L12-v2` (padrão) | 0,22 GB | 8/12 | 9/12 |
| `paraphrase-multilingual-mpnet-base-v2` | 1,0 GB | 9/12 | 9/12 |

O mpnet acertou uma consulta a mais no primeiro lugar, mas é 4,5× maior. Com apenas 12 consultas a diferença não é conclusiva, então o MiniLM foi mantido como padrão. A troca exige só `--modelo` na indexação, e a busca lê o modelo do manifesto automaticamente.

### Antes e depois da correção dos textos

Com o MiniLM, o índice gerado a partir dos textos anteriores à revisão da etapa 1 teve o mesmo total (8/12 e 9/12), mas três consultas mudaram de posição:

| Consulta | Textos anteriores | Textos corrigidos |
|---|---|---|
| “não visitar clientes que são filiais” | 1º | 3º |
| “prospect que nunca fez pedido deve ser atendido” | fora do top-5 | 1º |
| “cliente que comprou entre 7 e 30 dias atrás” | 4º | fora do top-5 |

As diferenças de similaridade envolvidas são pequenas (0,737 × 0,759 em “filiais”; 0,516 × 0,514 em “prospect”). Pequenas mudanças de redação no texto indexado já reordenam os primeiros lugares, por isso 12 consultas servem para apontar tipos de falha, e não para comparar versões com segurança.

### Falhas observadas e causas

| Consulta | O que aconteceu | Causa provável |
|---|---|---|
| “prospect que nunca fez pedido deve ser atendido” | Acerto no 1º lugar, mas “Não agendar prospects” ficou em 2º com similaridade quase igual (0,514 × 0,516) | Embeddings capturam mal a **negação**: “atender” e “não agendar” prospects ficam próximos no espaço vetorial. |
| “não visitar clientes que são filiais” | 1º e 2º lugares: regras sem condição que só fazem `nao agendar` (“Clientes fora dos ramos mapeados”); as regras de filiais vêm do 3º lugar em diante | Em regras sem condição, o texto indexado é quase só a ação (“não agendar esses clientes”), que coincide com o “não visitar” da consulta. |
| “atendimento mensal dos clientes” | Nenhuma regra mensal no top-5 | Frequências aparecem como números (“a cada 30 dias”), e o modelo associa mal “mensal” a “30 dias”. |
| “clientes do ramo consumidor final” | Nenhum `CONS. FINAL` no top-5 | O valor está **abreviado** na base (`"CONS. FINAL"`), e o modelo não o liga a “consumidor final”. |
| “cliente que comprou entre 7 e 30 dias atrás” | Nenhum acerto no top-5; 1º lugar: “entre 91 dias e 180 dias” | Intervalos numéricos são pouco distintivos para embeddings: “entre 90 e 180 dias” parece semelhante. |

## 6. Melhorias sugeridas

1. **Busca híbrida:** combinar o cosseno com busca por palavras-chave (BM25) para recuperar termos exatos como `CONS. FINAL`, `fixo` e números de dias.
2. **Enriquecer o texto de embedding** na etapa anterior: escrever “mensalmente (30 dias)” junto às frequências numéricas e expandir abreviações de ramo.
3. **Reordenação (re-ranking):** pedir ao LLM do agente que reordene os top-10 recuperados, o que trata melhor a negação.
4. **Ampliar a avaliação** com consultas reais de usuários antes de decidir a troca de modelo.

## 7. Arquivos de entrega

- `src/indexar_explicacoes.py`: gera o índice (`index/`) a partir do JSONL de embeddings.
- `src/buscar_explicacoes.py`: busca semântica pela linha de comando e classe `IndiceExplicacoes`, reutilizável pelo agente.
- `src/avaliar_busca.py`: conjunto de consultas de referência e métricas de acerto.
- `index/`: índice vetorial gerado (embeddings, metadados e manifesto).
- `requirements.txt`: dependências (`fastembed`, `numpy`).

## 8. Próximo passo

Integrar `IndiceExplicacoes.buscar()` ao agente conversacional: recuperar os exemplos mais próximos da regra descrita pelo usuário, juntar trechos do manual GoBR como segunda fonte de contexto e pedir ao LLM que gere a parametrização GoBR final, citando os exemplos usados.
