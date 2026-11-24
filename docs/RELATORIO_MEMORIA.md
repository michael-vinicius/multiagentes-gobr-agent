# Atividade — Construção de um agente com memória de contexto

## 1. Objetivo e interpretação

A atividade pede **um agente com memória de contexto**. O texto do enunciado no Turing não estava disponível para este trabalho (a página exige login e o enunciado não foi copiado), então o escopo foi definido a partir do título, do trabalho da disciplina (o agente GoBR das etapas anteriores) e do livro da disciplina (Dibia, *Designing Multi-Agent Systems*, cap. 4: seções 4.7 *Adding Memory*, 4.8 *Agent-Managed Memory* e 4.12 *Context Engineering*). Se o enunciado pedir algo diferente, ele prevalece sobre esta interpretação.

Interpretação adotada: o agente conversacional da etapa 5 deve

1. **lembrar o contexto da conversa** (memória de curto prazo): entender referências ao que foi dito antes ("volta como estava", "a mesma coisa para os inativos"), responder perguntas sobre o que fez e sobreviver ao fechamento do programa;
2. **lembrar entre conversas** (memória de longo prazo): a mesma empresa ou o mesmo analista não repete o que já decidiu;
3. **gerir a janela de contexto**: uma conversa longa não pode estourar a janela do modelo local (8.192 tokens) nem perder o que foi combinado.

**Resultado, com o código entregue** (seção 6):
- Em 5 cenários de várias sessões, escritos antes de rodar o modelo, o agente com memória chegou ao arquivo esperado (100% das decisões iguais) nos 5 e passou nas 6 checagens.
- O agente da etapa 5, nos mesmos cenários, chegou ao arquivo esperado em 1 de 4 e passou em 1 de 5 checagens: "volta como estava" não desfez, a sessão fechada recomeçou do zero, e uma sessão nova da mesma empresa ou de outra empresa perdeu o que tinha sido decidido.
- Numa conversa de 21 mensagens depois do arquivo, a compactação manteve o prompt abaixo de 3.800 tokens. Sem ela, o prompt chegou a 8.181 tokens, numa janela de 8.192, e estourou a janela em 3 rodadas.
- A regressão da etapa 5 continua em 10 de 10.

## 2. O ponto de partida: o que faltava no agente da etapa 5

| Lacuna | Consequência |
|---|---|
| estado da sessão só na RAM (`InMemorySaver`) | fechou o programa, perdeu a sessão, inclusive com perguntas pendentes |
| depois do arquivo, só "ajuste" ou "fim" | "volta como estava", "por que a rota vem primeiro?" e "o que muda se…" viravam pedidos de ajuste |
| as chamadas ao modelo não viam o histórico | referências à conversa não eram resolvidas |
| nada passava de uma sessão para outra | a mesma empresa ou o mesmo analista respondia tudo de novo |
| janela do modelo sem gestão | um prompt maior que 8.192 tokens só dava erro |

## 3. Os três tipos de memória, nos termos do livro

| Livro | Aqui | Onde |
|---|---|---|
| memória de curto prazo (4.7.1): o histórico da sessão | estado do grafo LangGraph (`historico`, `versoes`, especificação, decisões, plano), salvo a cada passo por um **checkpointer SQLite**; a sessão é retomada pelo id | `agente.py` (`Estado`, `abrir_memoria`, `conversar`) |
| memória de longo prazo (4.7.2), de **conhecimento** | o RAG das etapas 2–4: regras reais explicadas e manual indexados com embeddings | `rag.py` (já existia) |
| memória de longo prazo, **episódica e de preferências** | **LangGraph Store** em SQLite, com namespaces por empresa (arquivo aprovado, especificação, decisões, pedidos da sessão) e por analista (preferências e notas) | `memoria.py` (`MemoriaLonga`) |
| seleção do que lembrar (4.7.3): manual, automática ou híbrida | **híbrida**: no fim da sessão o agente propõe os candidatos e o analista confirma | nó `memorizar` |
| memória gerida pelo agente (4.8) | "lembre que …" grava na hora; "o que você lembra?" e "esqueça …" mostram e apagam | nó `conversa` |
| gestão de contexto (4.12): compactação, isolamento, filtragem | compactação **cabeça + cauda** com orçamento de tokens; **isolamento**: interpretação e redação não veem o chat, só o estado estruturado; **filtragem**: o arquivo GoBR das versões antigas sai do histórico | `memoria.montar_historico`, `filtrar_turno` |

O princípio que já guiava a etapa 5 (o modelo faz o que exige linguagem; o que exige exatidão é código) vale também para a memória: **o que foi decidido vive no estado estruturado, não no texto do chat**. É isso que permite cortar o histórico sem perder nada combinado, e retomar uma sessão sem reinterpretar a descrição.

## 4. O fluxo

```text
ler_entrada → lembrar ──(empresa lembrada + pedido curto: "partir do arquivo anterior?")──→ ajustar → revisar …
                └──(caso comum)──→ interpretar → revisar ⇄ perguntar → planejar → redigir ⇄ verificar → montar
                                                                                                     ↓
                     ajustar ◄──(ajuste, ou "aplica" depois de uma simulação)──┐                  responder
                     conversa ◄──(pergunta, simulação, desfazer, comparar,     │                     ↓
                                  lembrar, esquecer, "o que você lembra?")─────┼── entender ◄── aguardar ⇄ analista
                     memorizar ◄──(fim: propõe o que guardar)──────────────────┘
```

Nós novos (os da etapa 5 continuam iguais):

| Nó | Papel | Modelo? |
|---|---|---|
| `lembrar` | reconhece a empresa na entrada; com um pedido curto, oferece partir do arquivo aprovado antes (o pedido vira ajuste e nada é perguntado de novo); com uma descrição completa, as respostas daquela sessão viram sugestões | não |
| `entender` | classifica a mensagem depois do arquivo: regras de palavras para desfazer, comparar, simular, perguntar, ajustar, lembrar, esquecer, fim; o modelo só entra quando a mensagem tem referência à conversa ("a mesma coisa", "aquela") e não é uma pergunta comum; então reescreve o pedido com o histórico compactado. Um ajuste que não muda o arquivo não cria versão | só com referência |
| `conversa` | responde perguntas (modelo + arquivo atual + ordem dos blocos + trechos do manual + histórico compactado); simula mudanças **com o simulador**, sem aplicar ("aplica" aplica); desfaz; compara versões; lembra, mostra e esquece | só nas perguntas e na simulação (para editar a especificação) |
| `memorizar` | no fim, propõe guardar o arquivo e as decisões da empresa e as preferências que o analista escolheu explicitamente; grava o que ele confirmar | não |

## 5. Decisões e alternativas

| Decisão | Alternativas | Por quê |
|---|---|---|
| **checkpointer SQLite** para a sessão | `InMemorySaver` (etapa 5); Postgres | arquivo local, sem servidor, custo zero; o LangGraph salva o estado a cada passo e `get_state` devolve a pergunta pendente, então retomar é só continuar o grafo |
| **LangGraph Store** (SQLite) para o longo prazo | arquivos JSON/Markdown geridos pelo modelo (o `MemoryTool` do livro, 4.8); índice vetorial | o Store é a peça do próprio LangGraph para memória entre threads, com namespaces; as consultas aqui são por chave (empresa, analista), não por semelhança, então um índice vetorial não acrescentaria nada; a busca por semelhança já existe no RAG |
| empresa reconhecida pelo **nome no texto** | pedir o nome da empresa; busca semântica | o título da regra traz o nome ("Regra Maxlub") e o analista o escreve ao pedir uma mudança; a busca é por palavra inteira normalizada (sem acento, sem "regra"/"comercial") |
| seleção **híbrida** do que lembrar | guardar tudo automaticamente; só a pedido | guardar tudo mistura decisões de uma empresa com preferências gerais; só a pedido depende de o analista lembrar de pedir; o agente propõe o que faz sentido (o arquivo aprovado e as preferências que o analista escolheu, não as que só aceitou) e o analista confirma |
| **memória sugere, analista decide** | aplicar a preferência sem perguntar | uma decisão de outra sessão pode não valer para esta empresa; a pergunta continua, com a sugestão lembrada e o motivo ("lembrado: você escolheu … em 23/11, escolhida em …"); só quando o analista escolhe partir do arquivo anterior as decisões daquela empresa valem sem perguntar |
| **intenção por regras de palavras**, modelo só com referência | classificar tudo com o modelo | a maioria das mensagens tem marcas claras ("volta como estava", "o que muda se", "?"); regras são instantâneas e não erram nelas; o modelo de 7B fica para o que precisa do histórico ("a mesma coisa para os inativos"). Uma pergunta com "mesmo" ("quando duas regras pegam o mesmo cliente?") continua pergunta: na dúvida, errar para pergunta não muda o arquivo, e errar para ajuste muda (seção 6.4) |
| **simulação pelo simulador** | pedir ao modelo uma opinião sobre o efeito | "o que muda se…" tem resposta exata: aplica-se a mudança numa cópia, monta-se o plano com os moldes e compara-se com o arquivo atual em 6.432 clientes sintéticos; a resposta lista as faixas que mudam |
| **versões do arquivo no estado** | só o arquivo atual | desfazer e comparar viram operações sobre o estado, sem modelo; a versão restaurada é exatamente a anterior, não uma regeneração; um ajuste sem efeito não vira versão, para o "volta como estava" seguinte desfazer o que mudou de fato |
| **compactação cabeça + cauda** com resumo determinístico | janela deslizante simples; resumo pelo modelo | a cabeça (o pedido inicial) diz o que se está fazendo, a cauda diz onde se parou (livro 4.12.3); o meio vira uma linha do tempo com os pedidos do analista numerados, sem modelo (barato e sem risco de inventar); as decisões não dependem do histórico porque estão no estado |
| **filtragem** do arquivo das versões antigas | histórico com tudo | cada versão do arquivo tem ~600–1.500 tokens; repetir todas estoura a janela; o arquivo atual entra uma vez, nas instruções |
| **isolamento**: interpretação e redação não veem o chat | passar o histórico a todos os nós | é o padrão de isolamento do livro (4.12.3): os nós que mais gastam tokens (redação com RAG) recebem só o pedido do bloco; o histórico só entra onde ele é necessário (perguntas e referências) |
| **reaproveitar blocos** iguais de versões anteriores | redigir o arquivo inteiro a cada ajuste | um ajuste costuma mudar uma regra; o bloco idêntico já aceito volta sem chamar o modelo e passa de novo pela verificação semântica (memória de trabalho da sessão) |
| estimativa de tokens por caracteres | o tokenizador do qwen | evita uma dependência a mais; a estimativa (3 caracteres por token) é conservadora para português e foi conferida contra o `prompt_eval_count` do Ollama (seção 6) |

## 6. Avaliação

### 6.1 Método

`src/avaliar_memoria.py` roda cenários de uma ou mais sessões.

- **Usuário simulado.** Um analista simulado responde às perguntas e manda as mensagens da conversa, todas roteirizadas no cenário.
- **Arquivo final.** É comparado com o esperado pelo simulador semântico das etapas anteriores: 6.432 clientes sintéticos, % de decisões iguais.
- **Checagens.** Cada cenário tem uma checagem do que a memória deveria fazer. Exemplos:
  - a pergunta foi respondida e não tratada como ajuste;
  - a 2ª sessão não refez as perguntas;
  - a sugestão veio com o motivo lembrado.
- **Tokens.** São lidos do `prompt_eval_count` do Ollama, em todas as chamadas.
- **Escrito antes de rodar.** Os 5 cenários e o resultado esperado de cada um estão em `data/cenarios_memoria.json`, escritos antes da primeira rodada.
- **Diálogos salvos.** O diálogo inteiro fica salvo, e `--remedir` recalcula as checagens a partir dele sem chamar o modelo.

| Cenário | O que testa | Sessões |
|---|---|---|
| A — referência e desfazer (Maxlub) | ajuste, "volta como estava", pergunta sobre a ordem dos blocos | 1 |
| B — retomar a sessão (Infinitto) | o programa fecha no meio das perguntas e a sessão é retomada pelo id | 1, interrompida |
| C — mesma empresa, sessão nova (Maxlub) | pedido curto ("Maxlub: …") numa sessão nova parte do arquivo aprovado | 2 |
| D — preferência entre empresas | o que o analista escolheu para uma empresa vira sugestão, com motivo, para outra | 2 |
| E — conversa longa (Infinitto) | 21 mensagens depois do arquivo: simulações, "aplica", "compara", desfazer, 14 perguntas e, no fim, "qual foi a primeira pergunta que eu fiz?" | 1 |

Braços:
- **memória:** o agente desta etapa.
- **base:** `--sem-memoria`, o comportamento da etapa 5, nos cenários A–D.
- **sem compactação:** `--sem-compactacao`, ablação no cenário E. Tem memória e histórico, mas o histórico vai inteiro ao modelo.

### 6.2 Resultados com o código entregue

| Cenário | Memória: arquivo · checagens · perguntas por sessão · maior prompt · tempo | Base (etapa 5) |
|---|---|---|
| A | **100%** · 2/2 · [2] · 3.261 · 632 s | 99,1% · 1/2: "volta como estava" virou ajuste e não desfez (61–90 dias ficou em 10); a pergunta virou ajuste e regenerou o arquivo · 4.417 s |
| B | **100%** · 1/1: retomou com 1 interpretação · [3] · 2.236 · 185 s | 100% · 0/1: recomeçou do zero, 2 interpretações · 224 s |
| C | **100%** · 1/1: 0 perguntas na 2ª sessão · [2, 0] · 2.312 · 528 s | 50% · 0/1: sem o arquivo anterior, montou outro a partir do pedido curto, com 3 perguntas · 69 s |
| D | **100%** · 1/1: a sugestão veio com "lembrado: você escolheu …" · [3, 1] · 2.429 · 382 s | 75% · 0/1: sem a preferência, inadimplentes ficaram agendados · 150 s |
| E | **100%** · 1/1 · [3] · 3.696 · 0 estouros · 1.011 s (repetição: 100% · 1/1 · 3.730 · 909 s) | sem compactação: 100% · 0/1 (indicou a 2ª pergunta) · 7.691 · 1 estouro · 2.009 s |

Totais:
- **Memória:** 5/5 arquivos a 100%; 6/6 checagens.
- **Base:** 1/4 arquivos a 100%; 1/5 checagens.

Qual código gerou cada linha:
- **A:** commit `e408906`. O último commit (`e4328ed`) não muda o que o cenário A exercita: nenhuma das mensagens dele tem palavra de referência, e o ajuste muda o arquivo.
- **B–D:** commit `94f053f`. Os commits seguintes mexem só na compactação e na classificação de mensagens com referência, e esses cenários não passam por elas.
- **E:** o código final (`e4328ed`), rodado duas vezes.
- **Base:** rodada uma vez (23/11). O caminho `--sem-memoria` não passou pelo código alterado depois.

### 6.3 Cenário E, rodada a rodada

O cenário E foi o que mais ensinou. Cada rodada expôs um defeito, a correção entrou com teste, e o cenário rodou de novo:

| Rodada | Código | Com compactação: arquivo · lembrou a 1ª pergunta · maior prompt | Sem compactação: arquivo · lembrou · maior prompt · estouros |
|---|---|---|---|
| 1 (23/11) | `22b5af5` | 100% · ✗ (o resumo descartou o começo) · 5.860 | 100% · ✗ (não coube) · 8.149 · 4 |
| 2 | `b5fb4d7` | 100% · ✓ · 3.644 | 61,4% · ✗ · 8.181 · 5 |
| 3 | `94f053f` | 100% · ✗ (indicou a 14ª pergunta) · 3.562 | 100% · ✗ (indicou a 2ª) · 7.691 · 1 |
| 4 | `e408906` | **61,4%** · ✓ · 3.702 | — |
| 4b | `e408906` | 100% · ✗ (indicou a transcrição do PDF) · 3.671 | — |
| 5 | `e4328ed` | 100% · ✓ · 3.696 | — |
| 5b | `e4328ed` | 100% · ✓ · 3.730 | — |

**Com compactação:**
- Arquivo certo em 6 de 7 rodadas.
- A 1ª pergunta foi lembrada em 4 de 7 rodadas: 3 de 4 desde que os pedidos passaram a ser numerados, e 2 de 2 com o código final.
- O prompt ficou entre 3.562 e 3.730 tokens desde a rodada 2.

**Sem compactação:**
- Arquivo certo em 2 de 3 rodadas.
- A 1ª pergunta não foi lembrada em nenhuma das 3.
- O prompt ficou entre 7.691 e 8.181 tokens, e estourou a janela em todas as rodadas.

Prompt da conversa, turno a turno, na rodada 1: com compactação, de 2.035 a 5.860 tokens; sem compactação, de 2.749 a 8.149, e os 4 últimos turnos estouraram a janela. O teto de 2.500 tokens para o histórico (rodada 2) segurou o crescimento.

### 6.4 O que cada rodada mostrou e o que mudou

| Depois da rodada | Defeito (achado lendo o diálogo inteiro) | Correção |
|---|---|---|
| 1, cenário A | a checagem da base passava porque a base tratou a pergunta como ajuste e o arquivo regenerado traz o texto "Ordem dos blocos…" | resposta que é o arquivo regenerado não conta; recalculado (`22b5af5`). Base: 2/2 → 1/2 |
| 1, cenário E | o resumo do trecho compactado descartava os pedidos **mais antigos** quando crescia, e a 1ª pergunta sumiu | o resumo vira uma linha do tempo que guarda começo e fim e marca "[arquivo gerado ou alterado]"; teto de 2.500 tokens para o histórico (`b5fb4d7`) |
| 1, cenário E | "qual é a diferença entre recência em 60 dias e fora da recência…" caiu em "comparar versões" | "comparar" só quando a mensagem fala de versões (`b5fb4d7`) |
| 1, cenário E | ao mostrar um bloqueio de rota, o modelo inventou a cláusula `quando rota na semana` | as cláusulas certas dos filtros entram nas instruções das respostas (`b5fb4d7`) |
| 1, sem compactação | o computador suspendeu durante a noite com uma chamada aberta | a avaliação impede a suspensão enquanto roda (`b5fb4d7`) |
| 2 | o modelo copiava do histórico o rodapé "Peça uma mudança…", que saía duplicado | o rodapé é retirado da resposta do modelo e o histórico guarda a resposta sem ele (`94f053f`) |
| 3 | com memória, "qual foi a primeira pergunta?" foi respondida com a 14ª, e a checagem passou porque só pedia "prospect" | checagem endurecida para "antes dos ativos" e recalculada nas rodadas 1–3; a linha do tempo numera os pedidos ("1º pedido: …") (`e408906`) |
| 4 | "como o GoBR decide qual regra vale quando duas pegam o mesmo cliente?" tem "mesmo", foi ao modelo como possível referência e virou ajuste; a versão nova era idêntica à anterior, e o "volta como estava" seguinte desfez essa versão vazia, não a de 21 dias | uma mensagem que começa como pergunta e não pede mudança é pergunta, mesmo com "mesmo/esse/isso"; um ajuste que não muda o arquivo não cria versão (`e4328ed`) |

A rodada 4 corrigiu uma leitura minha. Na rodada 2, o mesmo erro tinha aparecido **só** sem compactação, e eu o atribuí ao contexto longo (*context rot*). A rodada 4 mostrou o erro **com** compactação. A causa era a regra de palavras, que mandava ao modelo uma pergunta comum, e o modelo errou a classificação. Com o código final, a mensagem não passa mais pelo modelo. Errar para "pergunta" não muda o arquivo; errar para "ajuste" mudava.

O que a memória guardou foi conferido no checkpointer SQLite da avaliação. Na rodada 3, a linha do tempo compactada trazia a 1ª pergunta, logo depois de "[arquivo gerado ou alterado]". A memória guardou a pergunta; o modelo de 7B leu a linha do tempo errado. O mesmo vale para a rodada 4b: as rodadas 4 e 4b usaram o mesmo código e deram respostas diferentes.

### 6.5 Ressalvas da avaliação

- **Duas checagens foram endurecidas depois de ver resultados:** a do cenário A na rodada 1 e a do cenário E na rodada 3.
  - Nas duas vezes a checagem ficou mais difícil de passar. A do A tirou um acerto da base; a do E tirou um acerto do próprio agente, na rodada 3.
  - As duas foram recalculadas em todas as rodadas, a partir dos diálogos salvos (`--remedir`).
  - A do E está anotada no próprio cenário, no campo `nota`.
- **Poucas repetições.** O cenário E rodou 7 vezes com compactação e 3 sem; os demais, de 1 a 3 vezes. Com `temperature=0`, o modelo ainda varia entre rodadas iguais (rodadas 4 e 4b). As taxas acima são contagens, não estimativas.
- **Base de uma rodada só.** A linha de base de cada cenário rodou uma vez.
- **Tempos.** A máquina tem uma GPU de 4 GB.
  - O braço sem compactação da rodada 1 marcou 52.711 s, porque o computador suspendeu com uma chamada aberta (14 h). Sem essa chamada, foram ~2.351 s.
  - A base do cenário A (4.417 s) inclui três reescritas da especificação inteira, uma para cada mensagem que virou ajuste, e uma chamada de 57 min sem causa identificada.

### 6.6 Estimativa de tokens

Os orçamentos usam 3 caracteres por token. A estimativa foi conferida contra o `prompt_eval_count` do Ollama:

| Amostra | Caracteres | Tokens reais | Caracteres/token | Estimativa |
|---|---|---|---|---|
| arquivo GoBR (Maxlub) | 1.690 | 507 | 3,33 | 564 (111%) |
| resposta do agente | 6.000 | 1.933 | 3,10 | 2.000 (103%) |
| relatório em prosa | 6.000 | 1.954 | 3,07 | 2.000 (102%) |

O template de chat acrescenta 29 tokens. A estimativa fica 2–11% acima do real, então o orçamento nunca é subestimado.

### 6.7 Regressão da etapa 5

`src/avaliar_agente.py` rodou com o código final, nos mesmos casos da etapa 5: os 3 exemplos do professor como PDF e como imagem (OCR), e os cenários C1–C4.

- **10/10 arquivos com 100%** das decisões iguais às do gabarito, e estrutura certa em todos.
- **61 de 63 blocos** foram escritos pelo modelo com RAG; na etapa 5 tinham sido 62. O bloco a mais que veio do molde é o "Risco" do C4: a correção do modelo divergiu de novo no simulador, então entrou o molde determinístico, com aviso.
  - Na etapa 5, a mesma correção tinha passado, com outra cláusula.
  - O código de redação não mudou nesta etapa; só ganhou telemetria.
  - A regressão anterior desta etapa, com o código de `22b5af5`, deu o mesmo resultado: 10/10 e o mesmo bloco no molde.
- **Tempo:** de 4 a 9 minutos por caso, como na etapa 5.

## 7. Testes

`python -m pytest`: **220 testes passando** (1 xfail registrado na etapa 4); 46 novos em `tests/test_memoria.py`, com dublês do modelo, do RAG e do OCR:

| Grupo | O que cobre |
|---|---|
| memória de longo prazo | chave da empresa, lembrar/achar/descrever/esquecer, preferências por analista, "lembre que …" → preferência, alinhamento das opções lembradas com as perguntas da revisão, sugestão lembrada com motivo |
| contexto | compactação dentro do orçamento com cabeça, cauda e resumo; resumo guarda o começo, numera os pedidos e marca o arquivo; filtragem do arquivo das versões antigas; teto do histórico só com compactação; estimativa de tokens |
| intenção | 19 mensagens típicas → fim, desfazer, comparar, simular, perguntar, ajustar, lembrar, esquecer, memória, aplicar; pedido com referência à conversa vai ao modelo; pergunta com "mesmo"/"aquela" continua pergunta |
| versões | ajuste que não muda o arquivo não cria versão, e o "volta como estava" seguinte desfaz o ajuste de verdade |
| curto prazo no grafo | desfazer e comparar com reaproveitamento de blocos; pergunta com histórico e arquivo nas instruções; simulação sem aplicar e "aplica"; referência reescrita pelo modelo; **sessão retomada de um SQLite sem refazer a interpretação** (o dublê do modelo fica sem respostas: se a interpretação rodasse de novo, o teste quebraria) |
| longo prazo no grafo | empresa lembrada parte do arquivo anterior sem perguntar de novo e só redige o bloco alterado; preferência passa para outra empresa como sugestão; lembrar, "o que você lembra?" e esquecer na conversa; `--sem-memoria` mantém a etapa 5 |
| ordem | "por que X vem antes de Y?" verificado no simulador (com e sem efeito) |
| resposta | o rodapé sai uma vez, mesmo quando o modelo o copia, e fica fora do histórico |
| avaliador | trocas no gabarito, respostas roteirizadas, resposta a um turno |

## 8. Limitações

- **Enunciado não lido.** O escopo é uma interpretação do título e do livro; se o enunciado pedir outra coisa (por exemplo, memória vetorial de conversas), o trabalho cobre só parte dele.
- **Empresa reconhecida pelo nome.** Se o analista escrever o nome de outro jeito ("Max Lub"), a empresa não é achada; não há busca aproximada.
- **Memória sem validade.** O que foi lembrado não expira nem é revisado; uma regra comercial que mudou continua sugerida até o analista apagar ("esqueça …") ou escolher outra opção.
- **Respostas do modelo.** As perguntas livres continuam sendo respondidas pelo qwen de 7B; as de ordem e as de "o que muda se" são verificadas no simulador, as demais não. Uma cláusula inventada foi vista na avaliação e mitigada (as cláusulas corretas entram nas instruções), não eliminada.
- **Classificação da intenção.**
  - Uma mensagem com "mesmo", "esse", "isso" etc. vai ao modelo, que reescreve o pedido com o histórico.
  - Antes, isso valia também para perguntas comuns ("quando duas regras pegam o mesmo cliente?"). O modelo classificou uma delas como ajuste em 2 das 8 execuções do cenário E feitas antes da correção, uma com e uma sem compactação (seção 6.4).
  - Com o código final, uma pergunta só vai ao modelo quando também pede mudança. Um ajuste que não muda o arquivo não cria versão.
  - Continua o risco em mensagens que não começam como pergunta ("isso aí vale para os inativos também"): o modelo ainda decide se é pergunta ou ajuste.
- **Compactação sem modelo.** O resumo do trecho compactado guarda os pedidos do analista e os momentos em que o arquivo mudou, não as respostas do agente; uma pergunta sobre "o que você respondeu no início" depende do que ficou na cauda.
- **A memória guarda; quem lê é o modelo de 7B.** Desde a 2ª rodada do cenário E, a 1ª pergunta estava no contexto em todas as rodadas, e mesmo assim o modelo indicou outra em 2 delas (3ª e 4b). Numerar os pedidos ajudou (3 de 4 acertos depois disso), mas não garante. Uma pergunta sobre a ordem da conversa poderia ser respondida por código, direto da linha do tempo; aqui ela é respondida pelo modelo.
- **Avaliação pequena.**
  - 5 cenários, usuário simulado, um modelo.
  - Poucas repetições: o cenário E rodou 7 vezes com compactação e 3 sem; os demais, de 1 a 3 vezes.
  - O tempo depende da GPU (4 GB), e um braço teve a medição de tempo contaminada por uma suspensão do computador (seção 6.5).
  - Duas checagens foram endurecidas depois de ver resultados. As duas estão registradas e foram recalculadas em todas as rodadas.
- **Um bloco a mais no molde.** Na regressão da etapa 5, 1 dos 63 blocos que o modelo escrevia passou a vir do molde determinístico. O arquivo continua 100% (seção 6.7).
- **Um analista por processo.** As preferências são por analista (`--analista`), mas não há autenticação: quem rodar com o nome de outro vê e altera as preferências dele.

## 9. Como usar

```bash
pip install -r requirements.txt          # inclui langgraph-checkpoint-sqlite
ollama pull qwen2.5:7b

# conversa com memória (bancos SQLite em memoria/)
python src/agente.py caminho/RegraCliente.pdf --analista ana
#   o programa mostra o id da sessão; fechou no meio? retome com:
python src/agente.py --sessao sessao-20261123-190000 --analista ana

# outra sessão, mesma empresa: parte do arquivo aprovado antes
python src/agente.py "Maxlub: prospects agora a cada 7 dias" --analista ana

# comportamento da etapa 5 (linha de base) e ablação da compactação
python src/agente.py regra.pdf --sem-memoria
python src/agente.py regra.pdf --sem-compactacao

# avaliação
python src/avaliar_memoria.py --exemplos <pasta .pdf + .gobr>
```

Depois do arquivo, o analista pode escrever: um ajuste ("muda a de risco para 10 dias"), uma pergunta ("por que a rota vem primeiro?"), uma simulação ("o que muda se os inativos forem atendidos a cada 21 dias?", depois "aplica"), "desfazer"/"volta como estava", "comparar", "lembre que …", "o que você lembra?", "esqueça …" ou "fim".

## 10. Arquivos

| Arquivo | O que mudou |
|---|---|
| `src/memoria.py` | novo: memória de longo prazo (Store), preferências, compactação do histórico, estimativa de tokens |
| `src/agente.py` | nós `lembrar`, `entender`, `conversa`, `memorizar`; histórico e versões no estado; checkpointer SQLite; retomada; reaproveitamento de blocos; CLI `--sessao`, `--memoria`, `--analista`, `--sem-memoria`, `--sem-compactacao` |
| `src/rag.py`, `src/llm_json.py` | telemetria de tokens por chamada (o Ollama informa `prompt_eval_count`) |
| `src/lacunas.py` | `Decisao.explicita`: separa o que o analista respondeu do que só aceitou como sugestão |
| `src/avaliar_memoria.py` | novo: avaliação de cenários de várias sessões, com linha de base |
| `data/cenarios_memoria.json` | novo: 5 cenários com o resultado esperado, escritos antes de rodar o modelo |
| `tests/test_memoria.py` | novo: testes da memória com dublês do modelo |
