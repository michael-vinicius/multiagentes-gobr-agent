# Atividade — Indexação do manual GoBR

## 1. Objetivo

Transformar o manual da linguagem GoBR (`govendas-rules.pdf`, “Guia do Usuário GoBR”) em um índice vetorial pesquisável. O índice das explicações (atividade anterior) devolve **exemplos** de parametrizações parecidas; este índice devolve a **referência da linguagem**: qual cláusula existe, como se escreve e quais restrições ela tem. As duas fontes juntas dão ao agente o contexto para escrever a regra GoBR final.

O enunciado pede atenção especial à quebra dos chunks. Por isso a maior parte do trabalho foi extrair o manual preservando a estrutura dele e quebrar o texto só onde o próprio manual quebra.

## 2. A fonte

O manual tem 62 páginas: capa, índice e 10 capítulos (times, carteiras e segmentações, filtros temporais, filtros de clientes, parâmetros, alertas, tags e a gramática). O conteúdo mistura quatro tipos de elemento:

| Elemento | Como aparece no PDF | Exemplo de conteúdo |
|---|---|---|
| Títulos | Negrito 16pt (capítulo), 12pt (seção) e 9,5pt (subseção), sempre numerados | `6.2 Filtros de recência de visita ou positivação (compra)` |
| Texto | Helvetica 10,5pt, com código inline em Courier | explicações, listas, avisos de “Atenção” |
| Blocos de código | Courier 10pt dentro de um retângulo cinza, com indentação significativa | exemplos completos de regras |
| Tabelas | células desenhadas como retângulos; o cabeçalho tem fundo cinza | cláusula → descrição (filtros, frequências, gatilhos…) |

As tabelas de referência são a parte mais valiosa para o agente e a mais frágil na extração: uma extração de texto comum (por exemplo `pdftotext -layout`) embaralha as duas colunas quando a descrição ocupa várias linhas.

## 3. Como foi feito

### 3.1 Extração estruturada (`src/extrair_manual.py`)

Em vez de extrair o texto corrido, o script lê do PDF (com `pdfplumber`) as palavras com fonte, tamanho e posição e os retângulos desenhados em cada página, e reconstrói os elementos:

1. **Cabeçalho e rodapé** de cada página são descartados pela posição; o número da página impressa é guardado como metadado.
2. **Títulos** são reconhecidos por estarem inteiramente em negrito, num dos três tamanhos de título, e começarem por numeração. Títulos quebrados em duas linhas são juntados.
3. **Blocos de código** são os retângulos cinza recuados. A indentação é recalculada pela posição horizontal de cada linha (cada caractere Courier ocupa 6pt) e as linhas em branco pelo espaçamento vertical, para que o exemplo saia igual ao do manual.
4. **Tabelas** são montadas célula a célula a partir dos retângulos, de modo que cada linha da tabela fica com a cláusula e a descrição corretas, mesmo quando o texto ocupa várias linhas dentro da célula.
5. **Texto** é agrupado em parágrafos e itens de lista pelo espaçamento e pelo recuo. Trechos em Courier no meio do texto são marcados como código (`` `assim` ``).
6. **Continuações entre páginas** são emendadas: tabelas que seguem na página seguinte sem repetir o cabeçalho, blocos de código e parágrafos interrompidos.

Problemas encontrados durante a conferência da extração e como foram resolvidos:

| Problema | Correção |
|---|---|
| A seta “→” usa a fonte Symbol e é lida como a ligadura “ﬁ” | Caracteres da fonte Symbol são convertidos para “→” |
| Linhas de código longas ultrapassam a borda direita do bloco cinza, e o trecho excedente saía fora do código | Pertence ao bloco tudo o que está na faixa vertical dele, sem limite à direita |
| Tabelas de uma coluna ocupam a largura toda e eram confundidas com blocos de código | Código é só o retângulo cinza recuado (x = 94pt); tabelas começam na margem (x = 72pt) |
| Linhas com a seta ficam mais espaçadas e partiam o parágrafo em dois | Espaçamento maior é aceito como continuação quando a frase anterior não terminou |
| Palavras hifenizadas e URLs quebradas no fim da linha ganhavam um espaço (“pré- calculada”) | A junção não insere espaço depois de hífen colado à palavra ou de “/” |
| Código inline quebrado entre linhas virava dois trechos (`` `"vendedor` `avulso"` ``) | Os trechos são unidos na emenda das linhas |

O resultado foi conferido seção a seção contra o PDF. O script também gera `index/manual/manual_extraido.md`, o manual inteiro em Markdown, para facilitar essa conferência.

### 3.2 Quebra em chunks

A unidade de chunk é a **seção do manual** (o título de menor nível, por exemplo `7.3.8 Exemplo 8 — Evitando conflitos entre televendas e campo`). Cada seção trata de um único assunto, então ela é o pedaço natural para responder a uma pergunta.

Regras aplicadas:

1. **Cada chunk começa com o caminho de títulos**, por exemplo `Manual GoBR > 6 Regras para filtros de clientes > 6.2 Filtros de recência…`. Assim, um trecho isolado continua dizendo de que parte do manual veio, e o caminho entra no embedding.
2. **Nada é cortado no meio.** As unidades indivisíveis são o parágrafo, o item de lista, o bloco de código (junto com a frase que o introduz, quando ela termina em “:”) e a linha de tabela.
3. **Seções só são divididas quando não cabem na janela do modelo** (500 tokens, com margem dentro dos 512). A divisão acontece entre unidades, e cada parte repete o caminho de títulos e o cabeçalho da tabela.
4. Títulos sem texto próprio (por exemplo `7.3 Exemplos de uso`, cujo conteúdo está nas subseções) não geram chunk.

Formato de um chunk que continua uma tabela:

```text
Manual GoBR > 6 Regras para filtros de clientes > 6.11 Outros filtros úteis

| Filtro | Descrição |
|---|---|
| `…` | … |
```

Cada chunk guarda `id`, `secao`, `titulo`, `caminho`, `paginas`, `parte` (por exemplo `1/2`), `tokens` e `texto`.

### 3.3 Por que não o modelo da indexação das explicações

O índice das explicações usa `paraphrase-multilingual-MiniLM-L12-v2`, que trunca a entrada em **128 tokens**. Os textos das explicações são curtos e cabem nesse limite; o manual, não:

| Medida (seções inteiras, tokenizador XLM-R) | Valor |
|---|---|
| Seções com conteúdo | 90 |
| Mediana de tokens por seção | 189 |
| Seções acima de 128 tokens | **72** |
| Seções acima de 512 tokens | 9 |

Com o MiniLM, 72 das 90 seções seriam truncadas, e tudo o que passa de 128 tokens ficaria fora do embedding sem aviso. Mesmo quebrando as seções em pedaços de até 128 tokens, 10 unidades indivisíveis (exemplos de código completos) passam do limite. O indexador valida isso e interrompe a execução quando algum chunk passaria do limite do modelo, em vez de gerar um índice truncado.

Foi escolhido o `intfloat/multilingual-e5-large`, que aceita 512 tokens, cobre o português e foi treinado especificamente para recuperação (consulta curta → passagem longa). Ele exige os prefixos `query: ` na consulta e `passage: ` nos documentos, que ficam registrados no manifesto e são aplicados automaticamente na busca.

### 3.4 Armazenamento e busca

O formato é o mesmo do índice das explicações: matriz de vetores normalizados (`embeddings.npy`), metadados alinhados linha a linha (`chunks.jsonl`) e um manifesto com o modelo, os prefixos, o limite de tokens, as estatísticas dos chunks e o hash SHA-256 do PDF. Com 99 vetores, a busca exaustiva por produto escalar leva milissegundos.

A classe `IndiceManual` (`src/buscar_manual.py`) carrega o índice e devolve os `k` trechos mais próximos com seção, páginas e texto completo, pronta para ser usada pelo agente.

## 4. Resultado

| Item | Valor |
|---|---|
| Seções extraídas | 95 (90 com texto próprio) |
| Chunks indexados | **99** (9 seções longas divididas em 2 partes) |
| Tokens por chunk | mínimo 55, mediana 193, máximo 498 |
| Chunks com exemplo de código | 26 |
| Chunks com tabela | 52 |
| Modelo | `intfloat/multilingual-e5-large` (1024 dimensões, cosseno) |
| Tamanho do índice | ≈ 0,6 MB (sem contar o modelo, ≈ 2,2 GB baixados na primeira execução) |
| Tempo de indexação | ≈ 2,5 min em CPU |
| Tempo por consulta | ≈ 80 ms (mais ≈ 5 s para carregar o modelo uma vez) |

Exemplo de busca (`python src/buscar_manual.py "clientes da curva A" -k 3 --resumo`):

```text
1. [0.883] 6.7 Filtros de curva ABC e ciclo de vida — p. 28, 29
2. [0.835] 6.2 Filtros de recência de visita ou positivação (compra) — p. 23, 24
3. [0.833] 6.11 Outros filtros úteis (parte 1/2) — p. 31, 32, 33
```

Para a pergunta “como faço para o cliente não ser visitado no mesmo dia pelo televendas e pelo campo?”, o 1º resultado é a seção `7.3.8 Exemplo 8 — Evitando conflitos entre televendas e campo`, com o exemplo completo da cláusula `sem choque` e as opções de refinamento.

## 5. Avaliação

Foi criado um conjunto de 24 consultas de referência (`src/avaliar_busca_manual.py`), misturando perguntas de sintaxe (como o agente consultaria o manual) e descrições de negócio (como o usuário escreveria). Um resultado conta como acerto quando vem da seção que contém a resposta; quando a resposta aparece em mais de um lugar (a tabela de referência e um exemplo de uso), todos contam.

### Modelos

Todos com a mesma extração e a mesma quebra (chunks de até 500 tokens):

| Modelo | Janela | Tamanho | Acerto@1 | Acerto@5 |
|---|---|---|---|---|
| `paraphrase-multilingual-MiniLM-L12-v2` | 128 | 0,22 GB | — | — |
| `paraphrase-multilingual-mpnet-base-v2` | 512 | 1,0 GB | 8/24 | 14/24 |
| `multilingual-e5-large` (padrão) | 512 | 2,2 GB | **21/24** | **24/24** |

O MiniLM não foi avaliado porque o índice seria truncado (seção 3.3). O mpnet aceita 512 tokens, mas ficou muito abaixo do e5. A causa provável é que os modelos *paraphrase* foram treinados com pares de frases curtas, enquanto o e5 foi treinado para encontrar passagens longas a partir de consultas.

### Tamanho dos chunks

Com o e5, variando só o tamanho máximo do chunk:

| Tamanho máximo | Chunks | Acerto@1 | Acerto@5 |
|---|---|---|---|
| 256 tokens | 135 | 20/24 | 24/24 |
| 350 tokens | 110 | 21/24 | 23/24 |
| 500 tokens (padrão) | 99 | 21/24 | 24/24 |

As diferenças são de no máximo uma consulta, então o tamanho foi decidido pelo princípio da seção 3.2: dividir uma seção só quando ela não cabe na janela do modelo. Com 500 tokens, cada resultado entrega ao agente a seção completa (tabela inteira, ou exemplo de código com a explicação), e a quebra só acontece nas 9 seções maiores. O caso que mais oscilou mostra o risco de quebrar demais: com 350 tokens, a tabela da seção 6.5 foi dividida em 3 partes, e a linha `cliente filial` ficou num trecho dominado por filtros de CNAE e Receita Federal, caindo para o 17º lugar na consulta “não atender clientes que são filiais”. Com 500 tokens, a mesma consulta acerta no 1º lugar.

### Erros no 1º lugar e causas

| Consulta | 1º resultado | Posição da resposta esperada | Observação |
|---|---|---|---|
| “clientes que não compram há mais de 90 dias” | `6.10 Filtros de ruptura` | 3º (`6.2`; `6.1` em 4º) | Resultado vizinho: a seção 6.10 também filtra clientes por dias sem compra (`em ruptura global do semestre`), mas em faixas fixas. |
| “aplicar a regra apenas na primeira semana do mês” | `7.5 Restrição de semana (restrito)` | 2º (`5.4`) | São conceitos diferentes com palavras quase iguais: `na primeira semana` (filtro temporal, quando a regra executa) e `restrito ate a primeira semana` (quando o cliente pode entrar na agenda). |
| “em que formato escrevo uma data na regra” | `7.4.1 Frequência fixa por período` | 2º (`6.13`) | A seção 7.4.1 mostra datas no formato `'dd-mm-yyyy'` dentro de `quinzenal(...)`, mas não explica o formato. |

Nos três casos a resposta esperada está no top-3, e o 1º resultado é um trecho relacionado. O segundo caso mostra uma ambiguidade real da linguagem: a descrição do usuário serve para duas cláusulas diferentes, e só o contexto decide qual é a certa.

As similaridades do e5 ficam numa faixa estreita (de 0,825 a 0,900 no top-5 de todas as consultas), por isso o valor absoluto não serve como corte. O que importa é a ordem dos resultados.

## 6. Inconsistências encontradas no manual

A conferência da extração encontrou duas falhas de diagramação no próprio PDF. O extrator não corrige o conteúdo da fonte, apenas evita que essas falhas quebrem a estrutura:

1. **Tabela da seção 6.11 (p. 32–33):** uma linha tem uma terceira célula contendo apenas a letra “s”, e a linha seguinte (já na p. 33) tem três células em vez de duas. O conteúdo excedente é anexado à última coluna, para nada ser perdido.
2. **Tabela da seção 6.12 (p. 35):** a linha `há <<N>> anos atras` aparece duas vezes. A duplicata foi mantida como está na fonte.

## 7. O manual fora do repositório

O manual traz o aviso “©2026 Govendas • ALL RIGHTS RESERVED” e o repositório é público. Por isso o PDF e tudo o que contém o texto dele (`index/manual/`: chunks, vetores e o Markdown extraído) ficam no `.gitignore`. O repositório contém apenas os scripts, que geram o índice em cerca de 2,5 minutos a partir do PDF:

```bash
python src/indexar_manual.py <caminho>/govendas-rules.pdf
```

O hash SHA-256 do PDF fica no manifesto, o que permite saber se o índice local foi gerado a partir da mesma versão do manual (`v. 0.89.0`).

## 8. Arquivos de entrega

- `src/extrair_manual.py`: extração estruturada do PDF (títulos, texto, código e tabelas) e quebra em chunks.
- `src/indexar_manual.py`: gera o índice (`index/manual/`), validando que nenhum chunk passa do limite do modelo.
- `src/buscar_manual.py`: busca pela linha de comando e classe `IndiceManual`, reutilizável pelo agente.
- `src/avaliar_busca_manual.py`: 24 consultas de referência e métricas de acerto.
- `requirements.txt`: dependências, agora com `pdfplumber` e `tokenizers`.

## 9. Próximo passo

Usar `IndiceManual.buscar()` junto com `IndiceExplicacoes.buscar()` no agente conversacional: os exemplos recuperados mostram como regras parecidas foram escritas, e os trechos do manual confirmam a sintaxe e as restrições de cada cláusula antes de o agente gerar a regra GoBR final.
