# Atividade — Construção de um agente com memória de contexto

## 1. Objetivo e interpretação

A atividade pede **um agente com memória de contexto**. O texto do enunciado no Turing não estava disponível para este trabalho (a página exige login e o enunciado não foi copiado), então o escopo foi definido a partir do título, do trabalho da disciplina (o agente GoBR das etapas anteriores) e do livro da disciplina (Dibia, *Designing Multi-Agent Systems*, cap. 4: seções 4.7 *Adding Memory*, 4.8 *Agent-Managed Memory* e 4.12 *Context Engineering*). Se o enunciado pedir algo diferente, ele prevalece sobre esta interpretação.

Interpretação adotada: o agente conversacional da etapa 5 deve

1. **lembrar o contexto da conversa** (memória de curto prazo): entender referências ao que foi dito antes ("volta como estava", "a mesma coisa para os inativos"), responder perguntas sobre o que fez e sobreviver ao fechamento do programa;
2. **lembrar entre conversas** (memória de longo prazo): a mesma empresa ou o mesmo analista não repete o que já decidiu;
3. **gerir a janela de contexto**: uma conversa longa não pode estourar a janela do modelo local (8.192 tokens) nem perder o que foi combinado.

⟨RESULTADO⟩

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
| `entender` | classifica a mensagem depois do arquivo: regras de palavras para desfazer, comparar, simular, perguntar, ajustar, lembrar, esquecer, fim; o modelo só entra quando a mensagem tem referência à conversa ("a mesma coisa", "aquela") e então reescreve o pedido com o histórico compactado | só com referência |
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
| **intenção por regras de palavras**, modelo só com referência | classificar tudo com o modelo | a maioria das mensagens tem marcas claras ("volta como estava", "o que muda se", "?"); regras são instantâneas e não erram nelas; o modelo de 7B fica para o que precisa do histórico ("a mesma coisa para os inativos") |
| **simulação pelo simulador** | pedir ao modelo uma opinião sobre o efeito | "o que muda se…" tem resposta exata: aplica-se a mudança numa cópia, monta-se o plano com os moldes e compara-se com o arquivo atual em 6.432 clientes sintéticos; a resposta lista as faixas que mudam |
| **versões do arquivo no estado** | só o arquivo atual | desfazer e comparar viram operações sobre o estado, sem modelo; a versão restaurada é exatamente a anterior, não uma regeneração |
| **compactação cabeça + cauda** com resumo determinístico | janela deslizante simples; resumo pelo modelo | a cabeça (o pedido inicial) diz o que se está fazendo, a cauda diz onde se parou (livro 4.12.3); o meio vira uma linha com os pedidos do analista, sem modelo (barato e sem risco de inventar); as decisões não dependem do histórico porque estão no estado |
| **filtragem** do arquivo das versões antigas | histórico com tudo | cada versão do arquivo tem ~600–1.500 tokens; repetir todas estoura a janela; o arquivo atual entra uma vez, nas instruções |
| **isolamento**: interpretação e redação não veem o chat | passar o histórico a todos os nós | é o padrão de isolamento do livro (4.12.3): os nós que mais gastam tokens (redação com RAG) recebem só o pedido do bloco; o histórico só entra onde ele é necessário (perguntas e referências) |
| **reaproveitar blocos** iguais de versões anteriores | redigir o arquivo inteiro a cada ajuste | um ajuste costuma mudar uma regra; o bloco idêntico já aceito volta sem chamar o modelo e passa de novo pela verificação semântica (memória de trabalho da sessão) |
| estimativa de tokens por caracteres | o tokenizador do qwen | evita uma dependência a mais; a estimativa (3 caracteres por token) é conservadora para português e foi conferida contra o `prompt_eval_count` do Ollama (seção 6) |

## 6. Avaliação

⟨AVALIACAO⟩

## 7. Testes

⟨TESTES⟩

## 8. Limitações

⟨LIMITACOES⟩

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
