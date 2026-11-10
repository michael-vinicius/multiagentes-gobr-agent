# Atividade — Fluxo básico de busca com RAG

## 1. Objetivo

Construir o fluxo básico de RAG (*Retrieval-Augmented Generation*) do agente GoBR: o usuário descreve uma regra de negócio em linguagem natural, o fluxo **busca** nos dois índices das atividades anteriores o que é relevante (parametrizações parecidas e trechos do manual) e entrega esse material a um modelo de linguagem, que **gera** a regra na DSL GoBR citando de onde tirou cada parte. Antes de devolver, o fluxo **confere** a regra gerada.

O fluxo reaproveita o que já existia: o índice das explicações (etapa 2), o índice do manual (etapa 3) e o classificador de cláusulas da etapa 1. Tudo roda localmente e sem custo; o Claude fica como opção paga.

**Resultado:** nos 11 pedidos do conjunto de teste, separados para medir a generalização e nunca usados para ajustar o fluxo, a versão final acerta a regra inteira em **10** (8 pelo gabarito original, seção 5.6). A versão inicial acertava **4**. A repetição da rodada final reproduziu as 17 respostas exatamente, mas há uma variação de até 2 casos entre rodadas com sequências diferentes de chamadas (seção 5.4).

## 2. O fluxo

```text
pedido em linguagem natural
   │
   ├─→ exemplos: busca híbrida (vetores da etapa 2 + BM25) ──→ E1…E5   (sem duplicatas, só regras "ok")
   └─→ manual:   busca híbrida (vetores da etapa 3 + BM25) ──→ M1…M4   (seção, páginas e texto completo)
   │
   ▼
prompt: instruções fixas (system) + contexto numerado + pedido no fim
   │
   ▼
modelo de linguagem ── local via Ollama (padrão, gratuito)  ou  Claude via API Anthropic (opcional, pago)
   │
   ▼
resposta: o que a regra faz + regra em ```gobr + pontos de atenção, com citações [E#]/[M#]
   │
   ▼
conferência: estrutura da regra · condições × catálogo (regras reais + manual) · citações
   │
   └─ com problema → o modelo recebe a lista do que corrigir (1 vez); vale a tentativa com menos problemas
```

| Arquivo | Responsabilidade |
|---|---|
| `src/rag.py` | `Recuperador` (contexto numerado), prompt, `BackendOllama` / `BackendAnthropic`, conferência, `Gerador` (geração + correção) e linha de comando |
| `src/busca_hibrida.py` | BM25 e fusão por posição (RRF) com a busca vetorial |
| `src/catalogo_gobr.py` | catálogo das cláusulas conhecidas, usado na conferência |
| `src/avaliar_rag.py` | avaliação ponta a ponta (ajuste e teste), só da busca (`--so-busca`) e reavaliação de rodadas salvas |

## 3. Como foi feito

### 3.1 Recuperação

**Deduplicação dos exemplos.** As 1700 parametrizações têm só **1208 corpos distintos**: a mesma regra aparece em vários arquivos, às vezes com outro nome (uma delas se repete 53 vezes). Sem tratamento, o top-5 podia trazer a mesma regra cinco vezes. O recuperador busca 4× mais candidatos que o necessário e descarta os que têm as mesmas cláusulas, ignorando o nome. Exemplos marcados para revisão na etapa 1 também ficam de fora.

**Busca híbrida.** A primeira versão usava só os vetores das etapas 2 e 3. A avaliação mostrou o ponto fraco: um único vetor representa o pedido inteiro e fica dominado pela parte mais marcante dele. Em “clientes **inativos** da carteira de campo recebem visita **quinzenal**”, os exemplos recuperados eram regras de carteira de campo, sem `inativos para o vendedor` (usada em 85 regras) nem `quinzenal()`. Aumentar o número de trechos do manual de 4 para 8 não mudou nada.

A busca passou a combinar os vetores com o **BM25**, a busca clássica por palavra-chave, que pontua cada termo separadamente e recupera justamente as cláusulas que o usuário escreveu de forma literal (“sem venda”, “prospect”, “choque”). As duas listas são combinadas por **Reciprocal Rank Fusion** (cada lista contribui 1/(60 + posição)), que junta rankings de escalas incomparáveis sem calibração. Os parâmetros são os usuais da literatura (k1 = 1,5, b = 0,75, k = 60, pesos iguais) e não foram ajustados nos casos de avaliação. O BM25 foi implementado no próprio projeto (≈ 40 linhas) para não acrescentar dependência; a normalização tira acentos e plurais simples e ignora palavras sem poder de discriminação, mantendo “sem” e “não”, que fazem parte de cláusulas. O `score` de cada resultado continua sendo a similaridade de cosseno, para manter o significado no prompt.

Efeito na cobertura (o contexto enviado ao modelo contém todas as cláusulas necessárias?), medido com `--so-busca`:

| Busca | Ajuste (6) | Teste (11) |
|---|---|---|
| só vetorial | 5 | 8 |
| **híbrida** | **6** | **10** |

A híbrida também resolveu uma limitação herdada da etapa 2: nenhum exemplo com `sem choque` aparecia nem no top-60 da busca vetorial (só 13 regras usam a cláusula, e no texto indexado delas a frequência vem antes). O BM25 acha a palavra “choque”.

### 3.2 Montagem do prompt

O contexto vai numerado e delimitado por tags, com o pedido no fim (contexto longo primeiro e pergunta por último):

```text
<contexto>
<exemplos>
<exemplo ref="E1" nome="Não agendar clientes inadimplentes (televendas)" similaridade="0.881">
<explicacao>Para clientes da carteira “carteira televendas”, considerar clientes inadimplentes. …</explicacao>
<dsl>
parametros "Não agendar clientes inadimplentes (televendas)":
    da carteira("carteira televendas")
    quando inadimplentes
    nao agendar
</dsl>
</exemplo>
…
</exemplos>
<manual>
<trecho ref="M1" secao="7.3.4" paginas="40" similaridade="0.861">
Manual GoBR > 7 Regras para parâmetros … > 7.3.4 Exemplo 4 — Remoção de agendamento
…
</trecho>
</manual>
</contexto>

<pedido>
Clientes inadimplentes não devem ser agendados
</pedido>
```

As instruções fixas (`SYSTEM_PROMPT`) pedem ao modelo para:
- usar só cláusulas que aparecem no manual ou nos exemplos, copiando a escrita delas, e preferir a do manual quando ele trouxer uma própria para o pedido;
- começar toda regra pela fonte de clientes (`do time`, `da carteira`, `da segmentacao`), sem usar filtros como nome da fonte;
- não inventar sintaxe nem valores quando o contexto não cobre o pedido, e dizer o que faltou;
- deixar nomes não informados como espaço reservado (`da carteira("<nome da carteira>")`);
- citar a fonte de cada cláusula;
- seguir um molde de resposta.

`python src/rag.py "<pedido>" --so-contexto` mostra o prompt exatamente como seria enviado, sem chamar modelo nenhum.

### 3.3 Geração: modelo local ou Claude

| Backend | Modelo padrão | Custo | Quando usar |
|---|---|---|---|
| `ollama` (padrão) | `qwen2.5:7b`, local | gratuito, sem chave | desenvolvimento, avaliação e uso sem orçamento de API |
| `anthropic` | `claude-opus-5-5` | pago por token (`ANTHROPIC_API_KEY`) | quando a qualidade da resposta for prioridade |

O `qwen2.5:7b` foi escolhido por caber nesta máquina (16 GB de RAM, GPU de 4 GB), ir bem em português e seguir formato razoavelmente para o tamanho.

Cuidados de cada backend:
- **Ollama:** quando o prompt não cabe na janela de contexto, o Ollama **descarta o início sem avisar**, e o modelo perderia as instruções. O backend fixa `num_ctx = 8192` (os prompts ficam em torno de 2,6 mil tokens) e interrompe com erro se a janela estourar. A temperatura é 0.
- **Claude:** usa o fallback do servidor para recusas (`fallbacks: "default"`), trata recusa e resposta truncada e converte os erros da API em mensagens claras. Na rodada de correção, o turno anterior do assistente é reenviado com o conteúdo original, incluindo os blocos de raciocínio: o Claude Opus 5.5 exige que eles voltem sem alteração, e reenviar só o texto contaria como histórico editado.

Nos dois casos, falha de conexão, resposta truncada ou vazia vira `ErroGeracao`, e a linha de comando termina com código 1 e a mensagem do problema.

### 3.4 Conferência da resposta

A resposta não é aceita às cegas. O fluxo:

1. **extrai a regra** dos blocos ```` ```gobr ````;
2. **confere as citações**: toda referência `[E#]`/`[M#]` precisa existir no contexto enviado;
3. **valida a estrutura** de cada bloco `parametros` com o classificador da etapa 1 (parênteses, ação presente, toda cláusula de tipo conhecido), exige a **fonte de clientes**, primeiro passo de toda regra no manual (seção 7.1) e presente nas 1700 regras reais, e recusa **citações ou comentários `//` dentro da regra**, que não são GoBR e não aparecem em nenhuma regra real;
4. **confere cada condição contra um catálogo** (`src/catalogo_gobr.py`) e acusa **filtro usado como nome da fonte**.

**O catálogo** junta as cláusulas das 1700 regras reais, os moldes das tabelas do manual (`inatividade de <<N>> dias` vira um padrão que aceita qualquer valor) e os exemplos de código do manual. As cláusulas são comparadas pela forma (sem acentos, números → N, textos entre aspas → S) e quebradas nas conjunções “e”. Uma condição que não aparece em nenhuma fonte indica sintaxe inventada, e a mensagem sugere a forma conhecida mais parecida:

```text
condição fora do manual e das regras reais: "quando nao choque na rota e na pasta do time("time campo")"
(a forma conhecida mais parecida é "sem choque na rota com time(S)")
```

O catálogo foi calibrado contra falsos positivos, e duas decisões saíram dessa medição:

| Medição | Resultado |
|---|---|
| 1700 regras reais, catálogo completo | 0 acusadas |
| cláusulas dos 43 exemplos do manual, com um catálogo que **não** conhece esses exemplos | conferindo também as ações: 8 acusadas; só as condições: **0** |
| idem, quebrando também em “ou” | 12 acusadas (pior) |

As ações (frequência, preferência, `sem choque`, `restrito`) são composicionais, com cascatas de alternativas (`frequencia do vendedor ou de qualquer vendedor ou de 35 dias`), e quebrá-las em partes gera pedaços que não existem soltos em lugar nenhum. Por isso o catálogo confere só as condições e os nomes de fonte, onde ele não acusou nenhuma cláusula válida, e foi onde o modelo errou.

### 3.5 Rodada de correção

Se a conferência encontrar problemas (regra ausente, validação, citações inválidas ou ausentes), a resposta volta ao modelo **uma vez**, com a lista do que corrigir e as sugestões do catálogo. A conversa fica assim: pedido → 1ª resposta → “a regra foi conferida e tem estes problemas: …” → 2ª resposta.

Duas proteções saíram da observação dos casos de ajuste:
- **Vale a tentativa com menos problemas, não a última.** Num caso, a 1ª resposta estava certa e só faltava citar. Na correção, o modelo pôs comentários (`// Exemplo E1`) dentro da regra e a quebrou. A correção nunca pode deixar a resposta pior do que a primeira.
- A mensagem de correção diz que as citações ficam fora do bloco `gobr`, que deve conter só a regra.

Os problemas que sobrarem continuam visíveis na resposta (`validacao`, `citacoes_invalidas`, `problemas_por_tentativa`), e o custo das duas chamadas é somado em `uso`.

## 4. Testes

`python -m pytest`: **118 testes passando e 1 `xfail` esperado** (106 sem modelos nem rede e 13 de integração com os índices locais). Os unitários usam dublês no lugar dos índices e dos modelos.

| Arquivo | O que cobre |
|---|---|
| `tests/test_rag.py` | recuperação (numeração, deduplicação, filtros, entradas inválidas), prompt, extração de blocos e citações, validação, os dois backends (requisição, resposta, recusa, truncamento, janela estourada, servidor fora do ar, modelo não baixado, credencial inválida), rodada de correção (quando dispara, mensagem, melhor tentativa, custo somado) e linha de comando |
| `tests/test_busca_hibrida.py` | tokenização, BM25, RRF e a combinação com a busca vetorial |
| `tests/test_catalogo_gobr.py` | forma das cláusulas, padrões do manual, condição inventada, filtro como nome, ações não conferidas e as 1700 regras reais sem nenhuma acusação |
| `tests/test_avaliar_rag.py` | critérios da avaliação e **o próprio gabarito**: cada alternativa aceita precisa existir nas regras reais ou no manual, e os conjuntos de ajuste e teste não se sobrepõem |
| `tests/test_rag_integracao.py` | recuperação com os índices reais (pulado se o índice do manual não existir) |

Um `xfail` estrito documenta que a busca **só vetorial** continua sem achar o `sem choque`. Se ela passar a achar, a suíte falha para que o registro seja revisto.

## 5. Avaliação ponta a ponta

### 5.1 Desenho

`src/avaliar_rag.py` roda o fluxo completo em 17 pedidos escritos como o analista escreveria:

- **Ajuste (6):** usados para diagnosticar e calibrar o fluxo (prompt, busca, conferência).
- **Teste (11):** escritos antes das melhorias e **nunca usados para ajustá-las**; medem a generalização.

Cada pedido define as cláusulas que a regra precisa ter, cada uma com as formas equivalentes aceitas (por exemplo `frequencia quinzenal()` ou `frequencia de 15 dias`). Um teste automatizado garante que toda forma aceita existe nas regras reais ou no manual.

Um caso é **aprovado** quando a resposta tem regra, a regra passa na conferência, cita fontes, não cita fonte inexistente e contém todas as cláusulas esperadas. A conferência das cláusulas é por palavra inteira (`adimplentes` não casa dentro de `inadimplentes`), sem acentos e ignorando o texto entre aspas: um filtro usado como nome, como `da carteira("curva A com a empresa")`, não conta.

A mesma conferência é feita no **contexto** enviado ao modelo, comparando a forma da cláusula (o número vem do pedido, não do contexto). Isso separa falha de busca (a cláusula não chegou ao modelo) de falha de geração (chegou e não foi usada).

**Mesma régua para todas as versões.** O gabarito e a conferência mudaram ao longo do trabalho (seção 5.6). Para que as versões sejam comparáveis, `--reavaliar` recalcula a nota de uma rodada salva com o gabarito e a conferência atuais, sem gerar de novo. Todos os números abaixo foram calculados assim.

### 5.2 Resultados (modelo local `qwen2.5:7b`)

Três versões, cada uma acrescentando uma melhoria (a do meio é uma ablação, para separar o efeito da busca do efeito da correção):

| Versão | Ajuste (6) | **Teste (11)** |
|---|---|---|
| inicial: busca vetorial, sem catálogo, sem correção | 3 | 4 |
| + busca híbrida | 4 | 7 |
| **+ catálogo e rodada de correção (final)** | **4** | **10** |
| final, repetição | 4 | 10 |

Métricas do conjunto de teste:

| Métrica (teste, 11 casos) | Inicial | + híbrida | Final |
|---|---|---|---|
| contexto contém as cláusulas necessárias | 8 | 10 | 10 |
| regra com as cláusulas certas | 8 | 9 | 10 |
| regra aprovada na conferência | 11 | 10 | 11 |
| citou fontes | 7 | 9 | **11** |
| **aprovados** | 4 | 7 | **10** |

Na versão final, 4 dos 17 casos passaram pela rodada de correção. Três terminaram aprovados: dois por falta de citação e um por uma condição inexistente, que o modelo trocou pela forma do manual (`quando prospects da empresa`) depois da sugestão do catálogo. Tempo por pedido: mediana de 23 s, até 53 s com correção (CPU + GPU de 4 GB, com o modelo já carregado). Prompt: ≈ 2,6 mil tokens.

### 5.3 Os casos que ainda falham (versão final)

| Pedido | Conjunto | Tipo | Diagnóstico |
|---|---|---|---|
| Televendas não podem ligar no mesmo dia da visita do campo | ajuste | geração | `sem choque` estava no contexto (M1 e exemplos), mas o modelo escreveu `quando recencia de visita em 3 dias` / `nao agendar`, uma regra válida e diferente da pedida. O catálogo não pega isso: a sintaxe existe. |
| Curva A com a empresa, preferência na segunda e na terça | ajuste | geração | a conferência acusou o filtro usado como nome da carteira, e a correção explicou o que fazer; o modelo acrescentou `quando curva A com a empresa`, mas manteve `da carteira("curva A com a empresa")`. A regra continua reprovada, corretamente. |
| Ramo de atividade FARMACIA, preferência na terça | teste | busca | `ramo de atividade igual(…)` não chegou ao contexto, e o modelo inventou `da carteira("ramo_farmacia")`. |

### 5.4 Variação entre rodadas

A busca é **determinística**: as mesmas perguntas recuperaram exatamente os mesmos exemplos e trechos em todas as rodadas.

A geração com temperatura 0 é reprodutível **quando a sequência de chamadas é a mesma**: a repetição da rodada final produziu os 17 textos idênticos aos da primeira. Mas ela muda quando a sequência muda. Entre a ablação (só busca híbrida) e a primeira versão com correção, o primeiro prompt de cada caso era o mesmo, mas a segunda rodada intercalava chamadas de correção; ainda assim 10 de 14 textos mudaram e a aprovação virou em 2 casos. A explicação provável é que o Ollama reaproveita o cache do início do prompt deixado pela chamada anterior, e esse estado muda o caminho numérico da execução mista CPU/GPU. É uma hipótese consistente com as duas observações, não verificada isoladamente.

Consequências para a leitura:
- **diferenças de 1 ou 2 casos entre versões estão dentro dessa variação.** É o caso do ajuste (3 → 4 → 4);
- a melhora no teste (4 → 7 → 10) é bem maior que ela, e a busca híbrida, que é determinística, explica sozinha a subida da cobertura do contexto de 8 para 10;
- as versões inicial e intermediária foram rodadas uma vez só.

### 5.5 O que os números dizem

- **A busca híbrida resolveu a maior parte das falhas de recuperação**: a cobertura do contexto foi de 8 para 10 em 11, de forma determinística, e resolveu a limitação do `sem choque` herdada da etapa 2.
- **A conferência com correção fez o modelo citar sempre** (citações 7 → 11 em 11) e corrigiu uma condição inventada. Sem a regra da melhor tentativa, a correção chegou a piorar um caso; com ela, isso não acontece mais.
- **O gargalo que sobra é semântico, do modelo de 7B**: escolher a regra certa entre regras válidas (o `sem choque`) e obedecer a uma correção que pede mudança de estrutura (a curva A). A conferência pega o segundo tipo, mas não tem como pegar o primeiro.
- **O backend do Claude não foi avaliado**, para não ter custo nesta atividade. Está implementado e testado com dublês; a comparação fica pendente: `ANTHROPIC_API_KEY=... python src/avaliar_rag.py --backend anthropic`.

### 5.6 Correções feitas no próprio avaliador

O avaliador também foi revisado ao longo do trabalho. Todas as correções abaixo foram aplicadas igualmente a todas as versões (pela reavaliação), e nenhuma muda a ordem entre elas.

| Problema encontrado | Correção |
|---|---|
| A conferência por substring aceitava um filtro dentro das aspas, como `da carteira("curva A com a empresa")`. | Texto entre aspas é ignorado. |
| `adimplentes` casava dentro de `inadimplentes`. | Comparação por palavra inteira. |
| `frequencia de 15 dias` era reprovada por não ser `quinzenal()`. | Cada cláusula aceita formas equivalentes, e um teste garante que todas existem nas regras reais ou no manual. |
| A busca era medida pelo número da seção do manual, mas a mesma sintaxe aparece em várias seções. | Passou a ser medida pela presença da cláusula no contexto, comparando a forma (`frequencia de # dias`). |
| **Afirmei, na versão anterior deste relatório, que `fora da recencia de positivacao em 90 dias` não existia e que a forma real tinha “do vendedor”.** A consulta usada para checar cortava a listagem, e a forma sem “do vendedor” aparece em 29 regras reais. | Forma incluída no gabarito do ajuste. O modelo estava certo naquele caso. |
| Teste, “pessoa jurídica”: o modelo usou `recencia de positivacao do vendedor entre 30 dias e 60 dias` (forma de 22 regras reais), que o gabarito não previa, embora o caso equivalente do ajuste já aceitasse as variantes “do vendedor” e “global”. | Variantes acrescentadas. **Feita depois de ver o resultado.** |
| Teste, “prospect”: o gabarito exigia `no ciclo de vida prospect com a empresa`, mas o manual tem `prospects da empresa` (6.1, “clientes que nunca compraram com a empresa”). Para evitar viés de seleção, o gabarito do teste **inteiro** foi auditado contra as tabelas do manual, inclusive os casos aprovados, e esta foi a única omissão. | Forma do manual acrescentada. **Feita depois de ver o resultado.** |

Uma brecha do próprio fluxo também apareceu na revisão final, ao executar o exemplo de uso do README: o modelo pôs a citação dentro da regra (`da carteira("carteira televendas")  [E2, M1]`), e a conferência aprovou. A conferência passou a recusar citações e comentários dentro da regra (seção 3.4). Nenhuma resposta das rodadas de avaliação tinha esse problema; reavaliadas, todas mantiveram a nota, então os resultados acima valem para o código final.

As duas últimas linhas da tabela mexem no conjunto de teste depois de ver resultados. Por isso, os números com o **gabarito original** também foram calculados: inicial 4/11, + híbrida 6/11, final **8/11**. A conclusão é a mesma.

## 6. Revisão das etapas anteriores

Como parte da validação, as etapas anteriores foram conferidas de novo:

| Verificação | Resultado |
|---|---|
| Avaliação da busca nas explicações (etapa 2) | 8/12 no 1º lugar e 9/12 no top-5, igual ao relatório da etapa |
| Avaliação da busca no manual (etapa 3) | 21/24 e 24/24, igual ao relatório da etapa |
| Hash da fonte no manifesto do índice da etapa 2 | confere com `data/parametrizacoes_para_embeddings.jsonl` |
| Ids e ordem: dataset da etapa 1 × JSONL de embeddings × metadados do índice | idênticos (1700) |
| Índice do manual: vetores × chunks × manifesto | 99 / 99 / 99 |
| Validação (estrutura + catálogo) nas 1699 regras “ok” da etapa 1 | nenhuma acusada |

A etapa 1 não pôde ser gerada de novo porque os arquivos `.gobr` de origem não fazem parte do repositório.

## 7. Limitações

| Limitação | Efeito | Caminho |
|---|---|---|
| Modelo local de 7B | erros semânticos: escolhe uma regra válida diferente da pedida ou não aplica a correção | modelo maior (backend `anthropic`, ou local maior em máquina com mais memória) |
| Geração do Ollama depende da sequência de chamadas | até 2 casos de diferença entre rodadas com sequências diferentes | repetir as rodadas e reportar a faixa; mais casos de avaliação |
| Conferência das ações | ações inventadas não são acusadas (as condições são) | gramática das ações (frequência, preferência, choque) a partir da seção 10 do manual |
| Catálogo baseado em exemplos | uma condição válida, mas ausente das regras e do manual, seria acusada (não aconteceu nas medições) | mesma gramática acima |
| Pedidos ainda fora do alcance da busca | “ramo de atividade FARMACIA” não recupera a cláusula | decompor o pedido em partes e buscar cada uma |
| Avaliação com 17 casos | resultado indicativo, não estatístico | ampliar os conjuntos, principalmente o de teste |
| Latência local de 20 a 50 s por pedido | uso interativo lento nesta máquina | GPU com mais memória ou modelo hospedado |

## 8. Arquivos de entrega

- `src/rag.py`, `src/busca_hibrida.py`, `src/catalogo_gobr.py`: o fluxo.
- `src/avaliar_rag.py`: avaliação ponta a ponta (`--conjunto`, `--so-busca`, `--reavaliar`, `--busca vetorial`, `--tentativas`, `--sem-catalogo`).
- `tests/` e `pytest.ini`: testes automatizados.
- `requirements.txt`: agora com `anthropic` (backend opcional); `requirements-dev.txt`: `pytest`.
- O Ollama e o modelo `qwen2.5:7b` são instalados à parte (instruções no README).

## 9. Próximo passo

Sugestões, em ordem de impacto segundo a avaliação:

1. Medir o backend do Claude nos mesmos 17 casos, para saber quanto do erro restante é do modelo local.
2. Ampliar o conjunto de teste e repetir cada rodada, para reduzir a margem de ruído.
3. Transformar o fluxo em agente conversacional, mantendo o histórico para que o analista refine a regra em várias rodadas (“agora só para a carteira de campo”).
