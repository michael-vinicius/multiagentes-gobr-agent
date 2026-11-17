# Atividade — Construção do fluxo agêntico para gerar uma parametrização

## 1. Objetivo

O enunciado pede um agente de conversação que ajude o analista a escrever regras de parametrização do Govendas na DSL GoBR:

- a entrada é uma **imagem ou uma descrição** das regras de negócio;
- o agente deve ser **proativo** e apontar **pontos falhos na modelagem comercial**;
- ao final, devolve o **conjunto de regras em GoBR**;
- dicas: usar as explicações indexadas (etapas 1–2), o manual indexado (etapa 3), atenção aos chunks e um **fluxo LangGraph** para orientar o agente.

Restrição deste trabalho: **custo zero**. O modelo de linguagem é o `qwen2.5:7b` local (Ollama), que **não lê imagens**. O Claude continua disponível como opção paga (`--backend anthropic`), mas não foi usado.

**Resultado:** nos 3 exemplos do professor (como PDF e como imagem) e nos 4 cenários próprios, o arquivo gerado decide igual ao gabarito para **100% dos 6.432 clientes sintéticos** (rodada v2, 10/10 casos). A primeira rodada (v1) deu 100% em 7 de 10 casos e expôs quatro defeitos, corrigidos antes da v2 (seção 5.2). Custo zero: tudo roda localmente, de 3 a 8 minutos por conversa numa GTX 1650.

## 2. O fluxo

```text
imagem / PDF / texto
   │
   ▼ ler_entrada ───────── PDF com texto: pdfplumber · imagem ou PDF escaneado: OCR local (RapidOCR, 2 escalas)
   │                        → reconstrução do mapa mental: um ramo por linha ("Ativos → compra até 60 dias → 14 dias")
   ▼ interpretar ───────── qwen com saída em JSON Schema → especificação estruturada
   │                        + conferências determinísticas (números, faixas, filtros negados)
   ▼ revisar ───────────── pontos falhos → avisos e perguntas com opções, sugestão e motivo
   │      ▲
   │      └── incorporar ◄── perguntar ⇄ analista      (interrupt do LangGraph; "1a, 2: 21 dias" ou "ok")
   ▼ planejar ──────────── blocos na ordem em que o GoBR os aplica (manual 7.6)
   │
   ▼ redigir_bloco ◄─────┐ qwen + RAG da etapa 4 (exemplos reais + manual), um bloco por vez
   ▼ verificar_bloco ────┘ simulador semântico; divergiu → correção com as divergências;
   │                        errou de novo → molde determinístico, com aviso
   ▼ montar → responder → aguardar ⇄ analista ── pedido de ajuste → ajustar → revisar …
                                                └─ "fim" → END
```

Cada nó tem uma responsabilidade e uma ferramenta, e o estado (`Estado` em `src/agente.py`) é o quadro compartilhado entre eles:

| Nó (papel) | Faz | Ferramenta | Modelo? |
|---|---|---|---|
| `ler_entrada` (transcritor) | imagem/PDF → texto estruturado em ramos | `transcrever_entrada.py` | não |
| `interpretar` (analista) | descrição → especificação (ação, frequência, faixa de recência, filtros, exceções) | `especificacao.py` + JSON Schema | **sim** |
| `revisar` (revisor comercial) | pontos falhos → perguntas e avisos | `lacunas.py` | não |
| `perguntar` / `incorporar` | conversa com o analista; texto livre passa pelo modelo | `interrupt`, `lacunas.interpretar_respostas` | só no texto livre |
| `planejar` (planejador) | blocos e ordem de aplicação | `lacunas.planejar` | não |
| `redigir_bloco` (redator GoBR) | escreve cada bloco com exemplos e manual recuperados | `rag.py` (etapa 4) | **sim** |
| `verificar_bloco` (verificador) | confere o bloco cliente a cliente; devolve as divergências ao redator | `simulador_gobr.py` | não |
| `montar` / `responder` | arquivo completo, conferência final, resumo | `especificacao.montar_arquivo`, `rag.validar_dsl` | não |
| `ajustar` | pedidos de mudança depois da resposta | `agente.ajustar_especificacao` | **sim** |

O princípio: **o modelo faz o que exige linguagem natural** (entender a descrição, redigir o bloco a partir de exemplos), e **o que exige exatidão é determinístico** (ordem, cobertura das faixas, verificação). Esse princípio veio da etapa 4: o modelo de 7B erra justamente em escolher a regra certa entre várias válidas e em seguir correções estruturais.

## 3. Como foi feito

### 3.1 Entrada por imagem, sem modelo pago

O qwen local não lê imagens. As alternativas consideradas:

| Alternativa | Custo | Por que (não) |
|---|---|---|
| Claude (lê imagem) | pago | descartada pela restrição de custo; continua como opção |
| modelo de visão local (qwen2.5-vl) | grátis | ~6 GB a mais; numa GPU de 4 GB, minutos por imagem e leitura pior que OCR em texto pequeno |
| **OCR local + reconstrução do layout** | **grátis** | escolhida: as imagens são mapas mentais com texto digitado, que OCR lê bem |

`src/transcrever_entrada.py`:

1. **PDF com camada de texto** (dois dos três exemplos): as palavras e posições vêm do próprio PDF (`pdfplumber`), sem erro de leitura. Palavras da mesma linha separadas por um vão maior que a altura da letra viram caixas diferentes.
2. **Imagem ou PDF escaneado** (o terceiro exemplo não tem texto): OCR com o RapidOCR (detecção PP-OCRv5 e reconhecimento **latino**, porque o modelo padrão chinês/inglês perde os acentos). Ele roda em `onnxruntime`, que já vinha com o `fastembed` da etapa 2.
3. **Reconstrução do mapa mental:** linhas alinhadas e coladas viram uma caixa; o nó isolado à esquerda é o título; a primeira coluna depois dele são os nomes dos ramos; cada detalhe vai para o ramo mais próximo na vertical. Marcas d'água ("Presented with xmind") e marcadores lidos nos conectores ("- 14 dias", "• Clientes") são retirados.

**A escala importa.** O detector perde caixas curtas ("7 dias") numa escala e as encontra em outra. Medição nos 3 exemplos renderizados em 4 resoluções (1×, 1,5×, 2×, 3×), em PNG e JPEG de qualidade 70 (24 imagens), contando as caixas "N dias" lidas corretamente:

| Configuração | Imagens perfeitas | Tempo médio |
|---|---|---|
| escala original + largura de 2400 px | 21/24 | 6,1 s |
| escala original + metade | 22/24 | 5,2 s |
| 3 escalas (original, referência, metade) | 23/24 | 7,1 s |
| **largura de 2400 px + metade dela** (adotada) | **23/24** | **5,7 s** |

A falha restante é um "7 dias" do exemplo Infinitto a 1569 px. O agente não depende do OCR ser perfeito: ele **mostra a transcrição para o analista conferir**, e uma regra sem frequência vira **pergunta** na revisão.

### 3.2 Interpretação: o modelo propõe, regras determinísticas conferem

O qwen recebe a descrição numerada e devolve um JSON restrito a um JSON Schema (o Ollama limita a geração ao schema). Cada ramo vira um item:

```json
{"ramo": 2, "nome": "Risco de Inatividade", "acao": "frequencia", "frequencia_dias": 7,
 "comprou_nos_ultimos_dias": 90, "sem_comprar_ha_mais_de_dias": 60,
 "filtros": [], "exceto": ["rota_semana"], "outras_condicoes": []}
```

O prompt traz um exemplo **inventado** (uma distribuidora fictícia). Os três exemplos do professor não entram no prompt, porque são usados na avaliação.

Medindo a extração nos três exemplos, o modelo acertou o Infinitto e o V1 Vidros, mas no Maxlub cometeu o erro mais perigoso possível: "Somente clientes que **não** estão na rota da semana" virou um **filtro positivo**, o que inverteria a regra (atenderia **só** quem está na rota), e "Prospects" perdeu o filtro de prospect. A etapa 2 já tinha registrado que embeddings e modelos pequenos tropeçam em negação.

Por isso, `conferir_especificacao` corrige o que o modelo devolve, e **cada correção vira um aviso visível ao analista**:

| Conferência | O que faz | Caso real |
|---|---|---|
| ramo certo | o item é ligado à linha cujo texto começa com o nome dele | cenário C2: a 1ª linha ("Equipe de campo") não era regra e o modelo numerou os itens a partir da linha seguinte; todos os valores eram descartados |
| números | todo número precisa aparecer no texto do ramo; o que não aparece é descartado, salvo o vizinho ±1 de um número escrito, que volta ao número escrito | Infinitto: "entre 60 e 90" veio como 89 |
| linha sem regra | item sem público, sem número e sem verbo de ação vira informação (fora do escopo) | cenário C4: "Atendimento feito pelo televendas." virou "não agendar todos" |
| faixa invertida | limite inferior ≥ superior é trocado | Infinitto: "entre 60 e 90" veio como 90/60 |
| filtros por marcadores | cada filtro conhecido citado no ramo vai para `filtros` ou `exceto` conforme haja negação antes do marcador ("não estão", "exceto", "sem"); o "não" de "não agendar" é ação e é ignorado; filtro não citado sai | Maxlub: 6 exceções de rota restauradas, prospect incluído, um "inadimplente" inventado retirado |
| condições repetidas | `outras_condicoes` que só repetem um filtro ou a recência saem (senão o bloco perderia a verificação) | — |
| equipe | "televendas"/"campo" citado no texto preenche a equipe | Maxlub |

Com isso, a especificação ficou correta nos três exemplos.

### 3.3 Revisão: os pontos falhos da modelagem comercial

`src/lacunas.py` examina a especificação. Cada verificação gera um **aviso** (informação) ou uma **pergunta** com opções, uma sugestão e o motivo:

| Verificação | Exemplo de pergunta ou aviso |
|---|---|
| equipe não informada | "Para qual equipe são as regras?" (todo arquivo precisa de um time, manual seção 10) |
| frequência ausente | "A regra 'Perdidos' não informa a frequência…" |
| **buraco entre faixas** | "Nenhuma regra cobre clientes de 31 a 60 dias sem comprar. O que fazer com eles?" |
| **acima da última faixa** | "Clientes com mais de 180 dias sem comprar não se enquadram em nenhuma regra." (falta a regra final) |
| sobreposição de faixas | "Para os clientes que estão nas duas, qual regra vale?" |
| prospects sem regra | regras de recência só pegam quem já comprou |
| **exceção repetida** | "Todas as regras excluem clientes com rota na semana. Posso trocar por um bloqueio único no início?" |
| bloqueio comum ausente | "Devo bloquear clientes baixados na Receita Federal?" (35 regras reais fazem isso) |
| inadimplentes não citados | agendar normalmente ou bloquear? |
| "agendar X" | aviso: agendar é o padrão; conflito se outro ramo bloqueia X |
| fora do escopo | aviso: "Capacidade de atendimento: 35 clientes/dia" não é parametrização |
| prioridade | regra com condição própria (curva A) × faixas de recência: qual vale primeiro? |

As respostas podem vir como "1a, 2b, 3: 21 dias", como "ok" (usar as sugestões) ou em texto livre. O texto livre passa pelo modelo, também com JSON Schema. Perguntas respondidas não voltam; depois de 3 rodadas, o que restar usa a sugestão, com aviso.

### 3.4 Plano: a ordem é semântica

O manual (7.6): *"clientes parametrizados em uma regra anterior não são reprocessados por regras subsequentes. A ordem importa."* A primeira regra que pega o cliente vale. O planejador monta:

1. **bloqueios** (`nao agendar`): baixados, inadimplentes, rota…;
2. regras com **público próprio** (condições específicas, prospects);
3. **faixas de recência**, da mais recente para a mais antiga;
4. **regra final**, sem filtro, para quem sobrou.

Por isso o "bloqueio único no início" substitui a exceção repetida sem mudar o efeito sobre as regras de agendamento.

### 3.5 Redação com RAG e verificação semântica

Cada bloco do plano vira um pedido em linguagem natural ("Para o time "televendas": clientes que compraram nos últimos 90 dias, mas estão há mais de 60 dias sem comprar devem ser atendidos com frequência de 7 dias.") e passa pelo **fluxo RAG da etapa 4**: busca híbrida nos exemplos e no manual, prompt numerado e conferência de estrutura e catálogo. O nome e a fonte de clientes (`do time(...)`) vêm do plano; o modelo escreve as condições e a ação.

Depois, o **verificador** simula o arquivo até aquele bloco e compara com o plano, cliente a cliente:

- igual → aceito;
- diferente → o redator recebe as divergências concretas ("clientes sem flags com 61–90 dias sem compra: esperado "frequencia 7", obtido "sem regra"") e, nessa correção, as cláusulas que o manual documenta para os filtros do pedido;
- diferente de novo → entra o **molde** determinístico do bloco, e a resposta avisa;
- bloco sem molde (condição própria, como curva A): só a conferência de estrutura e catálogo vale, e ele é marcado como "não verificado" se o simulador não o interpretar.

**Um defeito encontrado na primeira execução real.** O modelo escreveu `quando unica compra com o vendedor` para *prospects*. O simulador não conhece essa cláusula, marcou o bloco como "não verificável" e o aceitou. Pior: todos os blocos seguintes passaram a dar "indeterminado" e foram trocados pelo molde sem necessidade. Arquivo final: 50% de concordância com o gabarito, embora o plano estivesse 100% certo. Correções: (1) bloco com molde **precisa** ser verificável; cláusula desconhecida nele é divergência; (2) na referência, um bloco sem molde entra com o próprio texto aceito; (3) se um bloco anterior não é interpretável, os seguintes ficam "não verificáveis" em vez de passarem trivialmente. Os três casos têm testes de regressão.

### 3.6 O simulador semântico

Comparar regras pelo texto engana. `recencia de positivacao em 90 dias` depois de uma regra de 60 dias pega os mesmos clientes que `recencia de positivacao em 90 dias e fora da recencia de positivacao em 60 dias`, e uma regra sem filtro no fim equivale a `fora da recencia … em 90 dias`. Os próprios gabaritos usam formas diferentes para a mesma coisa (`global` ou não, regra final com ou sem filtro).

`src/simulador_gobr.py` aplica as regras como o manual descreve (a 1ª que pega o cliente vale) a **6.432 clientes sintéticos**: dias desde a última compra (nunca comprou, ou 0 a 400) × baixado na Receita × inadimplente × rota na semana × curva A. Duas regras são equivalentes quando decidem igual para todos.

Ele interpreta o subconjunto da linguagem usado em regras comerciais (recência, ciclo de vida/prospect, inadimplência, Receita, rota, curva A, ações `nao agendar` e frequência fixa). Fora disso, a regra é "não verificável", em vez de adivinhada: nas 1700 regras reais, 705 são interpretáveis; o resto usa critérios internos do sistema (`ativos para o vendedor`), ramo de atividade, faturamento etc.

Convenções assumidas (o manual não define os limites): `recencia … em N dias` = comprou há no máximo N dias; `fora da recencia … em N dias` = já comprou, há mais de N dias; prospects não satisfazem filtros de recência; `global` e `do vendedor` são tratados como iguais.

## 4. Testes

`python -m pytest`: **173 testes passando (1 xfail registrado na etapa 4)**. Os novos testes usam dublês no lugar do modelo, do RAG e do OCR:

| Arquivo | O que cobre |
|---|---|
| `tests/test_transcrever_entrada.py` | junção de linhas, título, ramos, marca d'água, união das escalas do OCR, limpeza de marcadores |
| `tests/test_simulador_gobr.py` | primeira regra vale, formas equivalentes, divergências agrupadas por faixa, negação, prospects, condição desconhecida |
| `tests/test_especificacao_lacunas.py` | conferências (número inventado, faixa invertida, filtro negado), cada verificação da revisão, respostas, plano, arquivo montado válido e com as decisões esperadas |
| `tests/test_agente.py` | conversa completa no grafo, correção após divergência, molde depois de dois erros, respostas por número, ajuste depois da resposta, os três casos de regressão da verificação |

## 5. Avaliação

### 5.1 Método

`src/avaliar_agente.py` roda a conversa inteira no grafo com um **usuário simulado** e compara o arquivo final com um gabarito pela simulação semântica (seção 3.6):

- **exemplos do professor** (Infinitto, Maxlub, V1 Vidros): a entrada é o PDF; com `--imagem`, o PDF é renderizado em PNG (1569 a 2268 px) e passa pelo OCR, como uma imagem enviada pelo analista. O usuário simulado responde "ok" (aceita as sugestões). Única exceção: no Infinitto em imagem, o OCR perde o "7 dias" de um ramo, o agente pergunta a frequência e o analista responde "7 dias" (ele está vendo a imagem que enviou);
- **cenários próprios** (`data/cenarios_agente.json`): quatro descrições em texto, com gabarito e respostas do analista escritos **antes** da primeira execução, para medir o que os exemplos não medem: texto corrido (C1), equipe de campo com faixa descoberta e regra sem frequência (C2), condição sem forma conhecida (curva A) com prioridade (C3) e exceção parcial em uma faixa (C4).

Métricas por caso: **arquivo** = decisões do arquivo iguais às do gabarito; **plano** = decisões do plano (os moldes dos blocos planejados) iguais às do gabarito, o que separa erro de entendimento (plano) de erro de redação (arquivo); **estrutura** = blocos aprovados na conferência da etapa 4; **modelo / molde** = blocos escritos pelo modelo × moldes; **corrigidos** = blocos que o modelo acertou depois de receber as divergências.

### 5.2 Rodada v1: quatro defeitos

| Caso | Arquivo | Causa |
|---|---|---|
| Infinitto (PDF) | 61,4% | o modelo leu "entre 60 e 90" como 89; a conferência descartou o 89 (não está no texto) e a faixa ficou aberta, então "Risco" pegou também quem tem mais de 90 dias |
| Infinitto (imagem) | 96,3% | o OCR perdeu o "7 dias"; o agente perguntou a frequência, o usuário simulado só disse "ok" e a pergunta voltou igual três vezes; a regra ficou fora |
| C2 | 92,4% | a 1ª linha ("Equipe de campo (visitas presenciais)") não é regra, mas foi numerada; o modelo numerou os itens a partir da linha seguinte e a conferência comparou cada item com a linha errada, descartando todos os valores |
| C4 | 98,1% | "Atendimento feito pelo televendas." virou a regra "não agendar todos" |
| os outros 6 | 100% | — |

Correções (com testes de regressão): o item é ligado à linha cujo texto começa com o nome dele; o vizinho ±1 de um número escrito volta ao número escrito; linha sem público, número nem ação é informação; a pergunta repetida explica que "ok" não a resolve e que, sem resposta, a regra fica fora. Os cenários C2 e C4 deixaram de ser inéditos depois disso: as correções são gerais (nenhuma cita o cenário), mas foram motivadas por eles.

### 5.3 Rodada v2

| Caso | Entrada | Arquivo | Plano | Estrutura | Modelo / molde | Corrigidos | Perguntas | Tempo |
|---|---|---|---|---|---|---|---|---|
| Infinitto | PDF | 100% | 100% | 5/5 | 5 / 0 | 1 | 3 | 198 s |
| Maxlub | PDF | 100% | 100% | 10/10 | 10 / 0 | 1 | 2 | 429 s |
| V1 Vidros | PDF | 100% | 100% | 5/5 | 5 / 0 | 2 | 1 | 282 s |
| Infinitto | imagem (OCR) | 100% | 100% | 5/5 | 5 / 0 | 1 | 4 | 219 s |
| Maxlub | imagem (OCR) | 100% | 100% | 10/10 | 10 / 0 | 1 | 2 | 447 s |
| V1 Vidros | imagem (OCR) | 100% | 100% | 5/5 | 5 / 0 | 2 | 1 | 295 s |
| C1 texto corrido | texto | 100% | 100% | 6/6 | 6 / 0 | 0 | 1 | 218 s |
| C2 campo, faixa descoberta | texto | 100% | 100% | 7/7 | 6 / 1 | 3 | 4 | 432 s |
| C3 curva A | texto | 100% | — ¹ | 5/5 | 4 / 1 | 1 | 3 | 206 s |
| C4 exceção parcial | texto | 100% | 100% | 5/5 | 5 / 0 | 2 | 1 | 291 s |

¹ O bloco da curva A não tem molde (condição própria), então não há plano completo para simular; o arquivo final foi comparado com o gabarito normalmente.

Leitura:

- **Perguntas proativas** apareceram em todos os casos e são as lacunas reais: no Maxlub, ninguém disse o que fazer com quem está há mais de 180 dias sem comprar, e faltava o bloqueio de baixados na Receita (os dois estão no gabarito); no C2, a faixa de 31 a 60 dias não tinha regra e "Perdidos" não tinha frequência; no C3, a prioridade entre curva A e recência.
- **Avisos** mostram o que o código corrigiu do modelo: no Maxlub, seis exceções de rota que o modelo tinha tornado filtros positivos, o filtro de prospect esquecido, a "capacidade de atendimento" fora do escopo e a exceção repetida trocada por um bloqueio único.
- **O modelo escreveu 61 dos 63 blocos** com RAG; 14 só acertaram depois de receber as divergências do verificador; 2 (C2 e C3) erraram duas vezes e entraram pelo molde, com aviso.

### 5.4 O que esses números não dizem

- **As sugestões foram desenhadas vendo os exemplos.** Os 100% com "ok" nos exemplos do professor eram em parte esperados: a sugestão de bloquear baixados, por exemplo, veio dos três gabaritos (e de 35 regras reais). Os cenários próprios medem a generalização, mas são poucos (4) e dois deles motivaram correções.
- **Usuário simulado.** Ele responde pelo id da pergunta; não testa como um analista real escreve respostas livres (que passam pelo modelo).
- **Variação do modelo entre execuções.** Com temperatura 0, o qwen ainda variou: a faixa "entre 60 e 90" do Infinitto veio invertida (90/60) num teste e como 89 na v1. As conferências determinísticas existem por isso, mas um erro que nenhuma delas cobre pode aparecer numa execução e não em outra.
- **O simulador cobre um subconjunto da linguagem** (705 das 1700 regras reais). Um bloco com condição fora dele (ramo de atividade, faturamento…) passa só pela conferência de estrutura e catálogo.

## 6. Limitações

- **Layout da imagem.** A reconstrução assume um mapa mental da esquerda para a direita (título, ramos, detalhes). Tabelas, fluxogramas e texto manuscrito não foram testados.
- **Cobertura da verificação.** Condições fora do subconjunto do simulador não são verificadas semanticamente; o agente avisa ("não verificado") em vez de esconder.
- **Escopo da geração.** O agente escreve `time` e `parametros` (frequência e bloqueios). Carteiras, alertas e outras partes do GoBR ficam de fora.
- **Convenções de limite.** O manual não define se "em 60 dias" inclui o dia 60; o simulador assume que sim, e os gabaritos são compatíveis com isso.
- **Tempo.** De 3 a 8 minutos por conversa numa GPU de 4 GB, quase todo no modelo (interpretação e redação dos blocos com RAG). Com o Claude (`--backend anthropic`) seria mais rápido, mas pago.
- **Avaliação pequena.** 3 exemplos + 4 cenários, usuário simulado, sugestões desenhadas com os exemplos à vista (seção 5.4).

## 7. Arquivos

| Arquivo | Responsabilidade |
|---|---|
| `src/agente.py` | grafo LangGraph, nós, verificação de blocos, resposta, linha de comando |
| `src/transcrever_entrada.py` | PDF/imagem → texto (pdfplumber ou OCR) e reconstrução do mapa mental |
| `src/especificacao.py` | especificação estruturada, extração com JSON Schema, conferências, molde, montagem do arquivo |
| `src/lacunas.py` | revisão comercial, perguntas, respostas e plano |
| `src/simulador_gobr.py` | simulação semântica e comparação de regras |
| `src/llm_json.py` | pedidos ao modelo com resposta em JSON |
| `src/avaliar_agente.py` | avaliação ponta a ponta com usuário simulado |
| `data/cenarios_agente.json` | cenários próprios com gabarito |

Dependências novas: `langgraph`, `rapidocr` (OCR), `pypdfium2` e `pillow` (renderização de PDF e imagens).
