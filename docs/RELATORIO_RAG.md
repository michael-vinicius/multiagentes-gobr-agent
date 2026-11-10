# Atividade — Fluxo básico de busca com RAG

## 1. Objetivo

Construir o fluxo básico de RAG (*Retrieval-Augmented Generation*) do agente GoBR: o usuário descreve uma regra de negócio em linguagem natural, o fluxo **busca** nos dois índices das atividades anteriores o que é relevante (parametrizações parecidas e trechos do manual) e entrega esse material a um modelo de linguagem, que **gera** a regra na DSL GoBR citando de onde tirou cada parte.

O fluxo usa só o que já existia: o índice das explicações (etapa 2), o índice do manual (etapa 3) e o classificador de cláusulas da etapa 1, que aqui valida a regra gerada.

## 2. O fluxo

```text
pergunta em linguagem natural
   │
   ├─→ IndiceExplicacoes (etapa 2) ──→ exemplos E1…E5   (sem duplicatas, só regras com validação "ok")
   └─→ IndiceManual (etapa 3) ───────→ trechos M1…M4    (seção, páginas e texto completo)
   │
   ▼
prompt: instruções fixas (system) + contexto numerado + pergunta no fim
   │
   ▼
modelo de linguagem ── local via Ollama (padrão, gratuito)  ou  Claude via API Anthropic (opcional, pago)
   │
   ▼
resposta: explicação curta + regra em ```gobr + pontos de atenção, com citações [E#]/[M#]
   │
   ▼
pós-checagens: citações existem no contexto? a DSL passa na validação estrutural?
```

Tudo está em `src/rag.py`, separado em quatro partes que podem ser testadas e trocadas de forma independente:

| Parte | Responsabilidade |
|---|---|
| `Recuperador` | consulta os dois índices e monta o `Contexto` numerado |
| `montar_mensagem` / `SYSTEM_PROMPT` | transformam o contexto e a pergunta no prompt |
| `BackendOllama` / `BackendAnthropic` | chamam o modelo de linguagem |
| `Gerador` | junta prompt, modelo e pós-checagens e devolve a `Resposta` |

## 3. Como foi feito

### 3.1 Recuperação

A mesma pergunta consulta os dois índices, cada um com o seu modelo de embeddings (MiniLM nos exemplos, e5-large no manual, com o prefixo `query: ` aplicado pela própria classe `IndiceManual`).

**Deduplicação dos exemplos.** As 1700 parametrizações têm só **1208 corpos distintos**: a mesma regra aparece em vários arquivos, às vezes com outro nome (uma delas se repete 53 vezes). Sem tratamento, o top-5 podia trazer a mesma regra cinco vezes e desperdiçar o contexto. O recuperador busca 4× mais candidatos que o necessário e descarta os que têm as mesmas cláusulas, ignorando o nome. Exemplos marcados para revisão na etapa 1 também ficam de fora. Se ainda assim sobrarem menos de `k` exemplos distintos, o contexto vai com menos, em vez de repetir.

### 3.2 Montagem do prompt

O contexto vai numerado e delimitado por tags, com o pedido no fim (contexto longo primeiro e pergunta por último, como recomendado para prompts com documentos):

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

As instruções fixas (`SYSTEM_PROMPT`) dizem ao modelo para:

- usar só cláusulas que aparecem no manual ou nos exemplos, copiando a escrita delas, e preferir a do manual quando ele trouxer uma própria para o pedido;
- começar toda regra pela fonte de clientes (`do time`, `da carteira`, `da segmentacao`), sem usar filtros como nome da fonte;
- não inventar sintaxe nem valores quando o contexto não cobre o pedido, e dizer o que faltou;
- deixar nomes de times e carteiras não informados como espaço reservado (`da carteira("<nome da carteira>")`);
- citar a fonte de cada cláusula (`[M2]`, `[E1, M3]`);
- responder seguindo um molde: o que a regra faz, a regra num bloco `gobr` e os pontos de atenção.

O comando `python src/rag.py "<pergunta>" --so-contexto` mostra o prompt exatamente como seria enviado, sem chamar modelo nenhum. É útil para inspecionar a recuperação.

### 3.3 Geração: modelo local ou Claude

A geração é plugável (`Backend` é qualquer objeto com o método `completar(system, mensagem)`):

| Backend | Modelo padrão | Custo | Quando usar |
|---|---|---|---|
| `ollama` (padrão) | `qwen2.5:7b`, local | gratuito, sem chave | desenvolvimento, avaliação e uso sem orçamento de API |
| `anthropic` | `claude-opus-5-5` | pago por token (`ANTHROPIC_API_KEY`) | quando a qualidade da resposta for prioridade |

A primeira versão usava só o Claude. Como a avaliação com a API teria custo, a geração passou a aceitar um modelo local servido pelo [Ollama](https://ollama.com). O `qwen2.5:7b` foi escolhido por caber nesta máquina (16 GB de RAM e GPU de 4 GB), ir bem em português e seguir formato razoavelmente para o tamanho.

Cuidados de cada backend:

- **Ollama:** a janela de contexto padrão do Ollama é pequena, e quando o prompt não cabe ele **descarta o início sem avisar**. Nesse caso o modelo perderia as instruções e parte do contexto. O backend fixa `num_ctx = 8192` (os prompts medidos ficam em torno de 2,5 mil tokens) e interrompe com erro se o prompt mais a resposta chegarem ao limite. A temperatura é 0, para que a mesma pergunta produza a mesma resposta.
- **Claude:** usa o fallback do servidor para recusas (`fallbacks: "default"`), trata `stop_reason` de recusa e de resposta truncada e converte os erros da API (credencial, conexão, status) em mensagens claras.

Nos dois casos, falha de conexão, resposta truncada ou vazia vira `ErroGeracao`, e a linha de comando termina com código 1 e a mensagem do problema, sem *traceback*.

### 3.4 Pós-checagens

A resposta do modelo não é aceita às cegas. Antes de devolvê-la, o fluxo:

1. **extrai a regra** dos blocos ```` ```gobr ```` (ou ```` ```gorules ````);
2. **confere as citações**: toda referência `[E#]`/`[M#]` citada precisa existir no contexto enviado. Citações inventadas aparecem em `citacoes_invalidas`;
3. **valida a estrutura da DSL** de cada bloco `parametros` com o mesmo classificador de cláusulas da etapa 1: parênteses balanceados, presença de uma ação, toda cláusula com tipo conhecido (alvo, condição, filtro temporal ou ação) e presença da fonte de clientes (`do time`, `da carteira` ou `da segmentacao`).

A última regra foi acrescentada depois do primeiro teste real: o modelo gerou `quando inadimplentes / nao agendar` sem a fonte de clientes, e o validador da etapa 1 não acusava isso. O manual (seção 7.1) põe a fonte de clientes como primeiro passo obrigatório, e as 1700 regras reais têm uma, então a checagem é segura.

A validação é estrutural, não um parser da gramática: uma cláusula de tipo conhecido ainda pode ter um valor inválido. Para garantir que o validador não rejeita regras corretas, um teste roda ele nas 1699 regras reais com validação "ok" e exige que todas passem.

## 4. Testes

`python -m pytest`: **64 testes passando e 1 `xfail` esperado** (57 unitários e 8 de integração).

| Arquivo | O que cobre | Precisa de |
|---|---|---|
| `tests/test_rag.py` | recuperação (numeração, deduplicação, filtros, entradas inválidas), prompt (referências, escape, ordem), extração de blocos e citações, validação da DSL, os dois backends (requisição, resposta, recusa, truncamento, janela estourada, servidor fora do ar, modelo não baixado, credencial inválida), gerador e linha de comando | nada (dublês no lugar dos índices e dos modelos) |
| `tests/test_avaliar_rag.py` | critérios da avaliação ponta a ponta (alternativas, texto entre aspas, cobertura do contexto, reprovações) | nada |
| `tests/test_rag_integracao.py` | recuperação com os índices reais; validador × dataset de referência | índices locais; pulado se o índice do manual não existir |

Os testes unitários não usam rede, modelo de embeddings nem modelo de linguagem, e rodam em segundos. A geração com modelo real é medida na avaliação (seção 5), não nos testes.

**Limitação registrada como `xfail`.** Para “evitar que televendas e campo atendam o mesmo cliente no mesmo dia”, nenhum exemplo com `sem choque` aparece nem no top-60 do índice de explicações. Só 13 das 1700 regras usam essa cláusula, e no texto indexado delas a frequência e a preferência vêm antes. É a limitação já descrita na etapa 2, não um defeito do RAG: o manual traz a seção certa (7.3.8) em 1º lugar, o que é verificado em outro teste. O `xfail` é estrito: se o índice melhorar e o teste passar, a suíte falha para que o registro seja removido.

## 5. Avaliação ponta a ponta

`src/avaliar_rag.py` roda o fluxo completo em 6 pedidos de referência, escritos como o analista escreveria (regras de negócio, não perguntas de sintaxe). Para cada pedido estão definidas as cláusulas que a regra precisa ter, cada uma com as alternativas equivalentes documentadas no manual ou usadas nas regras reais (por exemplo `frequencia quinzenal()` ou `frequencia de 15 dias`).

Um caso é **aprovado** quando a resposta tem regra, a regra passa na validação estrutural, cita fontes, não cita fonte inexistente e contém todas as cláusulas esperadas. A conferência ignora acentos, maiúsculas e o texto entre aspas: um filtro usado como nome, como `da carteira("curva A com a empresa")`, não conta.

A mesma conferência é feita no **contexto** enviado ao modelo. Isso separa as falhas de busca (a cláusula nem chegou ao modelo) das falhas de geração (chegou, mas o modelo não usou). Com `--so-busca`, o script mede só a busca, em segundos.

### 5.1 Resultados com o modelo local (`qwen2.5:7b`, temperatura 0)

Foram duas rodadas: a primeira com o prompt inicial e a segunda depois de uma revisão do prompt (seção 5.3). As duas foram julgadas pelo avaliador final.

| Métrica (6 casos) | Prompt inicial | Prompt revisado |
|---|---|---|
| **Aprovados** | 1 | **2** |
| Contexto contém as cláusulas necessárias | 4 | 4 |
| Regra com as cláusulas certas | 2 | 2 |
| DSL estruturalmente válida | 5 | **6** |
| Citou fontes | 2 | **5** |
| Citou fonte inexistente | 0 | 0 |
| Tempo por resposta (CPU + GPU de 4 GB) | 36–84 s | 49–71 s |
| Tokens por prompt | ≈ 2,5 mil | ≈ 2,5 mil |

Caso a caso, com o prompt revisado:

| Pedido | Resultado | Diagnóstico |
|---|---|---|
| Para o time de televendas, não agendar os clientes que são filiais | ✅ | `quando e o cliente filial` (forma usada em 8 regras reais) + `nao agendar`, com citações |
| Clientes inadimplentes não devem ser agendados | ✅ | usou o espaço reservado `da carteira("<nome da carteira>")`, como pedido |
| Curva A com a empresa, preferência na segunda e na terça | ❌ geração | a cláusula estava no contexto (M1 = 6.7), mas o modelo a usou como nome da carteira, mesmo com a instrução explícita contra isso |
| Televendas não podem ligar no mesmo dia da visita do campo | ❌ geração | a seção 7.3.8 com `sem choque` veio em 1º lugar (M1), mas o modelo escreveu uma cláusula inexistente (`quando nao choque na rota…`) |
| Carteira fixa, sem compra há 90 dias, atender a cada 14 dias | ❌ geração | escreveu `fora da recencia de positivacao em 90 dias`; a forma real é `… do vendedor em 90 dias` |
| Inativos da carteira de campo, visita quinzenal | ❌ busca | nem `inativos para o vendedor` (usada em 85 regras) nem `quinzenal()` chegaram ao contexto; o modelo inventou `inatividade de 15 dias` |

Duas observações sobre a métrica de contexto:

- No caso dos 14 dias, ela marca `frequencia de 14 dias` como ausente porque nenhuma fonte tem essa frase literal: o manual só traz o molde `de <<N>> dias`. É um limite da conferência literal, não uma falha de busca.
- O caso da cláusula inventada `quando nao choque…` mostra o limite da validação estrutural: a linha começa com `quando`, então é classificada como condição e passa, embora não exista no GoBR.

### 5.2 O que os números dizem

- **A busca entrega o material certo na maioria dos casos** (4 de 6, e 5 de 6 descontando o limite da conferência literal). Nos três casos reprovados por geração, a cláusula certa estava no contexto, e duas vezes em 1º lugar.
- **O gargalo é o modelo gerador.** Com 7 bilhões de parâmetros, o qwen segue bem o formato (citações e estrutura melhoraram muito com o prompt revisado), mas erra a semântica: troca filtro por nome e cria cláusulas parecidas com as reais. As pós-checagens pegam parte desses erros (fonte de clientes ausente, citações), mas não todos.
- **Pedidos compostos são o ponto fraco da busca.** Aumentar o número de trechos do manual não ajudou (cobertura 4/6 com `k_manual` = 4, 6 ou 8). O problema é que um único vetor representa a pergunta inteira, e ele fica dominado pela parte mais “marcante” do pedido (“carteira de campo”) em detrimento das outras (“inativos”, “quinzenal”).

O backend do Claude (`--backend anthropic`) está implementado e testado com dublês, mas **não foi avaliado ponta a ponta**, para não ter custo de API nesta atividade. A comparação entre os dois modelos fica pendente:

```bash
ANTHROPIC_API_KEY=... python src/avaliar_rag.py --backend anthropic
```

### 5.3 A revisão do prompt

A primeira rodada mostrou três falhas de instrução: o modelo quase não citava fontes (2/6), omitia a fonte de clientes e preferia um exemplo parecido à cláusula própria do manual. O prompt revisado acrescentou:

- um molde concreto da resposta, já com citações;
- a regra do manual (seção 7.1) de que toda regra `parametros` começa pela fonte de clientes, e de que filtros não são nomes;
- a preferência explícita pela cláusula do manual quando ele trouxer uma própria para o pedido;
- o motivo das citações (o analista confere a regra por elas).

Foi uma única revisão, com instruções genéricas e sem referência aos casos de teste. Com só 6 casos, que serviram tanto para diagnosticar quanto para medir, mais rodadas de ajuste tenderiam a sobreajustar o prompt a esses pedidos. O número absoluto (2/6) deve ser lido como um retrato do modelo local, não como uma estimativa precisa.

### 5.4 Problemas do próprio avaliador, corrigidos antes do resultado final

Na primeira versão, o avaliador conferia as cláusulas por substring na regra inteira e media a busca por números de seção. A análise das respostas mostrou três problemas, corrigidos antes de recalcular as duas rodadas:

1. `da carteira("curva A com a empresa")` passava como se tivesse o filtro, porque o texto estava dentro das aspas. Agora o texto entre aspas é ignorado.
2. `frequencia de 15 dias` era reprovada por não ser `quinzenal()`, embora seja equivalente. Agora cada cláusula aceita alternativas documentadas.
3. A “seção certa do manual” subestimava a busca (2/6), porque a mesma sintaxe aparece em várias seções (`inatividade de 90 dias` está em 6.1 e em todos os exemplos de 7.3). Ela foi trocada pela cobertura das cláusulas no contexto.

## 6. Limitações

| Limitação | Efeito | Caminho |
|---|---|---|
| Uma única consulta vetorial por pedido | pedidos com várias condições perdem cláusulas na busca | decompor o pedido em partes (fonte, filtros, ação) e buscar cada uma; ou combinar com busca por palavra-chave (BM25) |
| Índice de exemplos com cláusulas raras pouco representadas (etapa 2) | `sem choque` não aparece nos exemplos | o manual cobre; melhoria do texto indexado proposta na etapa 2 |
| Validação estrutural, não gramatical | cláusulas inventadas que começam com `quando` passam | validar cada condição contra o catálogo de filtros do manual |
| Modelo local de 7B | erros semânticos (seção 5.2) | modelo maior (Claude pelo backend `anthropic`, ou um local maior em máquina com mais memória) |
| Avaliação com 6 casos | resultado indicativo, não estatístico | ampliar o conjunto de casos, separando casos de ajuste e de medição |
| Latência local de ~1 min por resposta | uso interativo lento nesta máquina | GPU com mais memória ou modelo hospedado |

## 7. Arquivos de entrega

- `src/rag.py`: o fluxo completo (recuperação, prompt, backends, pós-checagens) e a linha de comando.
- `src/avaliar_rag.py`: avaliação ponta a ponta com 6 casos de referência (`--so-busca` mede só a recuperação).
- `tests/`: 65 testes (`pytest`), com `pytest.ini` na raiz.
- `requirements.txt`: agora com `anthropic` (backend opcional). `requirements-dev.txt`: `pytest`.
- O Ollama e o modelo `qwen2.5:7b` são instalados à parte (instruções no README).

## 8. Próximo passo

Sugestões, em ordem de impacto segundo a avaliação:

1. Medir o backend do Claude nos mesmos 6 casos, para saber quanto do erro é do modelo local.
2. Decompor pedidos compostos na busca (seção 6), que é a falha de recuperação observada.
3. Transformar o fluxo em agente conversacional: manter o histórico para que o analista refine a regra em várias rodadas (“agora só para a carteira de campo”) e usar o resultado das pós-checagens para pedir correção ao modelo automaticamente quando a regra não passar na validação.
