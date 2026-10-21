\# Geração de Explicações de Parametrizações GoBR



\## Atividade



Disciplina de Multiagentes.



Tema: \*\*Geração de explicações (regras de negócio) a partir das parametrizações.\*\*



O objetivo desta etapa é transformar parametrizações escritas na DSL GoBR em descrições compreensíveis de regras de negócio.



Essas descrições serão utilizadas posteriormente como base para embeddings, recuperação de exemplos semelhantes via RAG e construção do agente conversacional.



\## Objetivo



Converter automaticamente parametrizações GoBR em explicações em linguagem de negócio, preservando a relação entre:



\- parametrização original;

\- público-alvo;

\- condições;

\- ações;

\- explicação gerada;

\- arquivo de origem.



\## Fluxo



```text

Arquivos .gobr

&#x20;     ↓

Leitura das parametrizações

&#x20;     ↓

Identificação de alvo, condições e ações

&#x20;     ↓

Conversão para linguagem de negócio

&#x20;     ↓

Validação

&#x20;     ↓

Dataset estruturado

&#x20;     ↓

Preparação para embeddings/RAG

