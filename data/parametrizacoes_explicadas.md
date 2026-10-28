# Explicações de regras de negócio geradas a partir das parametrizações GoBR

- Arquivos `.gobr` processados: **246**
- Blocos `parametros` convertidos: **1700**
- Cláusulas não classificadas automaticamente: **0**

> Cada explicação mantém o bloco GoBR original no JSONL para rastreabilidade. O Markdown agrupa as explicações por arquivo.

## regra_001.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_002.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_003.gobr

### Não agendar filiais

Para clientes vinculados ao time “televendas”, considerar clientes que são filiais. Ação: não agendar esses clientes.

### Não agendar clientes com visita do externo na semana anterior

Para clientes vinculados ao time “televendas”, considerar clientes data da ultima visita do representante na semana anterior. Ação: não agendar esses clientes.

### Não agendar clientes com rota programada com o externo nos próximos 7d

Para clientes vinculados ao time “televendas”, considerar clientes data da rota futura nos proximos 7 dias. Ação: não agendar esses clientes.

### Não agendar clientes com compra em 7d atrás

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa nos últimos 7 dias. Ação: não agendar esses clientes.

### Ative este prospect: nunca tirou pedido

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 14 dias.

### Prospect ativado: fez um pedido e não comprou mais

Para clientes vinculados ao time “televendas”, considerar clientes cadastrados há 60 dias; e unica compra com o vendedor. Ação: atender a cada 14 dias.

### Mantenha a regularidade de compra do cliente que teve pedido detectado nos últimos 30d e não foi visitado na semana anterior

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa entre 7 e 30 dias atrás. Ação: atender a cada 14 dias.

### Garanta regularidade de compra e relacionamento com este cliente! Seu último pedido foi entre 31d e 60d atrás

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa entre 31 e 60 dias atrás. Ação: atender a cada 7 dias.

### Cliente a INATIVAR! Seu último pedido foi entre 61d e 90d atrás

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa entre 61 e 90 dias atrás. Ação: atender a cada 3 dias.

### Cliente estava inativo e foi reativado. Restabeleça relacionamento!

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa nos últimos 14 dias; e cuja última compra/positivação na empresa está fora do intervalo de 15 a 90 dias atrás. Ação: atender a cada 14 dias.

### Ative cliente INATIVO

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação na empresa nos últimos 90 dias. Ação: atender a cada 14 dias.

### REGRA GENÉRICA: Atendimento ao cliente que não se enquadrou nas regras padrão

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 21 dias.

## regra_004.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_005.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_006.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_007.gobr

### Regra Padrao da Nutri Distribuidora: 30 dias para inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: atender a cada 30 dias.

### Regra Padrao da Nutri Distribuidora: 14 dias para ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: atender a cada 14 dias.

### Regra Padrao da Nutri Distribuidora: 7 dias para sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: atender a cada 7 dias.

## regra_008.gobr

### Regra Padrao da NB PI Customizavel: 14 dias para adimplentes (Capital)

Para clientes da carteira “carteira capital”, considerar clientes adimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da NB PI Customizavel: 14 dias para clientes sem venda (Capital)

Para clientes da carteira “carteira capital”, considerar clientes sem venda. Ação: atender a cada 14 dias.

### Regra Padrao da NB PI Customizavel: 30 dias para inadimplentes (Capital)

Para clientes da carteira “carteira capital”, considerar clientes inadimplentes. Ação: atender a cada 30 dias.

### Regra Padrao da NB PI Customizavel: 30 dias para todos os clientes (Interior)

Aplicar a regra a clientes da carteira “carteira interior”. Ação: atender a cada 30 dias.

## regra_009.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_010.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_011.gobr

### Regra Padrao da VetVida Customizavel: Nao agendar clientes ativos (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor. Ação: não agendar esses clientes.

### Regra Padrao da VetVida Customizavel: 14 dias para clientes inativos (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da VetVida Customizavel: 14 dias para clientes sem venda (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes sem venda. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da VetVida Customizavel: Nao agendar clientes inativos inadimplentes (campo)

Para clientes da carteira “carteira campo”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da VetVida Customizavel: 14 dias para clientes ativos (campo)

Para clientes da carteira “carteira campo”, considerar clientes ativos para o vendedor. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da VetVida Customizavel: 14 dias para clientes inativos adimplentes (campo)

Para clientes da carteira “carteira campo”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da VetVida Customizavel: 14 dias para clientes sem venda (campo)

Para clientes da carteira “carteira campo”, considerar clientes sem venda. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

## regra_012.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_013.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_014.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_015.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_016.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_017.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_018.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_019.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_020.gobr

### Regra Padrao da Trenas - Customizavel: Frequencia de 7 dias para todos os clientes

Aplicar a regra a clientes da carteira “empresa toda”. Ação: atender a cada 7 dias.

## regra_021.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_022.gobr

### Regra Padrao da Supergiro - Customizavel: 14 dias para todos os clientes clientes (time televendas)

Aplicar a regra a clientes vinculados ao time “time televendas”. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Supergiro - Customizavel: Nao agendar clientes sem venda (campo)

Para clientes da carteira “carteira campo”, considerar clientes sem venda. Ação: não agendar esses clientes.

### Regra Padrao da Supergiro - Customizavel: 14 dias para clientes ativos ou inativos (campo)

Aplicar a regra a clientes da carteira “carteira campo”. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

## regra_023.gobr

### Regra Padrao da BSB Vet (GYN): 7 dias para clientes sem venda (televendas)

Para clientes da carteira “carteira televendas gyn”, considerar clientes sem vendas. Ação: atender a cada 7 dias.

### Regra Padrao da BSB Vet (GYN): 14 para todos os clientes (televendas)

Aplicar a regra a clientes da carteira “carteira televendas gyn”. Ação: atender a cada 14 dias.

### Regra Padrao da BSB Vet: 7 dias para clientes adimplentes (televendas)

Para clientes da carteira “carteira televendas df”, considerar clientes adimplentes. Ação: atender a cada 7 dias.

### Regra Padrao da BSB Vet: 14 dias para ativos inadimplentes (televendas)

Para clientes da carteira “carteira televendas df”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da BSB Vet: nao agendar inativos inadimplentes (televendas)

Para clientes da carteira “carteira televendas df”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da BSB Vet: 7 dias para clientes sem venda (televendas)

Para clientes da carteira “carteira televendas df”, considerar clientes sem vendas. Ação: atender a cada 7 dias.

### Regra Padrao da BSB Vet: Frequencia de 7 dias para clientes ativos (campo)

Para clientes vinculados ao time “time campo df”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias; marcar a parametrização como fixa.

### Regra Padrao da BSB Vet: Frequencia de 15 dias para clientes inativos (campo)

Aplicar a regra a clientes vinculados ao time “time campo df”. Ação: atender a cada 15 dias; marcar a parametrização como fixa.

## regra_024.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_025.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_026.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_027.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_028.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_029.gobr

### Regra Padrao da Trilha - Customizavel: Nao agedar inativos inadimplentes

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Trilha - Customizavel: 14 dias para todos os clientes

Aplicar a regra a clientes da carteira “empresa toda”. Ação: atender a cada 14 dias.

## regra_030.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_031.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_032.gobr

### Baixados na Receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Prospects

Para clientes da carteira “sul_sudeste_centrooeste”, “norte_nordeste”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 14 dias.

### Ativos Curva A (Sul, Sudeste e Centro-Oeste - Matcon, Ferragista, Agropecuária e Home Center)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("MATCON","FERRAGISTA","AGROPECUARIA","HOME CENTER"); e com a última compra/positivação na empresa nos últimos 120 dias; e média faturada no ano com a empresa maior que R$ 25000. Ação: atender a cada 14 dias.

### Ativos Curva B (Sul, Sudeste e Centro-Oeste - Matcon, Ferragista, Agropecuária e Home Center)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("MATCON","FERRAGISTA","AGROPECUARIA","HOME CENTER"); e com a última compra/positivação na empresa nos últimos 120 dias; e média faturada no ano com a empresa maior que R$ 10000. Ação: atender a cada 21 dias.

### Ativos Curva C (Sul, Sudeste e Centro-Oeste - Matcon, Ferragista, Agropecuária e Home Center)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("MATCON","FERRAGISTA","AGROPECUARIA","HOME CENTER"); e com a última compra/positivação na empresa nos últimos 120 dias. Ação: atender a cada 28 dias.

### Pré-inativos Curva A (Sul, Sudeste e Centro-Oeste - Matcon, Ferragista, Agropecuária e Home Center)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("MATCON","FERRAGISTA","AGROPECUARIA","HOME CENTER"); e com a última compra/positivação na empresa nos últimos 150 dias; e média faturada no ano com a empresa maior que R$ 25000. Ação: atender a cada 14 dias.

### Pré-inativos Curva B (Sul, Sudeste e Centro-Oeste - Matcon, Ferragista, Agropecuária e Home Center)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("MATCON","FERRAGISTA","AGROPECUARIA","HOME CENTER"); e com a última compra/positivação na empresa nos últimos 150 dias; e média faturada no ano com a empresa maior que R$ 10000. Ação: atender a cada 14 dias.

### Pré-inativos Curva C (Sul, Sudeste e Centro-Oeste - Matcon, Ferragista, Agropecuária e Home Center)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("MATCON","FERRAGISTA","AGROPECUARIA","HOME CENTER"); e com a última compra/positivação nos últimos 150 dias. Ação: atender a cada 14 dias.

### Inativos Curva A (Sul, Sudeste e Centro-Oeste - Matcon, Ferragista, Agropecuária e Home Center)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("MATCON","FERRAGISTA","AGROPECUARIA","HOME CENTER"); e média faturada no ano com a empresa maior que R$ 25000. Ação: atender a cada 14 dias.

### Inativos Curva B (Sul, Sudeste e Centro-Oeste - Matcon, Ferragista, Agropecuária e Home Center)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("MATCON","FERRAGISTA","AGROPECUARIA","HOME CENTER"); e média faturada no ano com a empresa maior que R$ 10000. Ação: atender a cada 14 dias.

### Inativos Curva C (Sul, Sudeste e Centro-Oeste - Matcon, Ferragista, Agropecuária e Home Center)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("MATCON","FERRAGISTA","AGROPECUARIA","HOME CENTER"). Ação: atender a cada 14 dias.

### Ativos Curva A (Sul, Sudeste e Centro-Oeste - EPI e Licitação)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("EPI","LICITACAO"); e com a última compra/positivação na empresa nos últimos 120 dias; e média faturada no ano com a empresa maior que R$ 25000. Ação: atender a cada 14 dias.

### Ativos Curva B (Sul, Sudeste e Centro-Oeste - EPI e Licitação)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("EPI","LICITACAO"); e com a última compra/positivação na empresa nos últimos 120 dias; e média faturada no ano com a empresa maior que R$ 10000. Ação: atender a cada 21 dias.

### Ativos Curva C (Sul, Sudeste e Centro-Oeste - EPI e Licitação)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("EPI","LICITACAO"); e com a última compra/positivação na empresa nos últimos 120 dias. Ação: atender a cada 28 dias.

### Pré-inativos Curva A (Sul, Sudeste e Centro-Oeste - EPI e Licitação)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("EPI","LICITACAO"); e com a última compra/positivação na empresa nos últimos 150 dias; e média faturada no ano com a empresa maior que R$ 25000. Ação: atender a cada 14 dias.

### Pré-inativos Curva B (Sul, Sudeste e Centro-Oeste - EPI e Licitação)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("EPI","LICITACAO"); e com a última compra/positivação na empresa nos últimos 150 dias; e média faturada no ano com a empresa maior que R$ 10000. Ação: atender a cada 14 dias.

### Pré-inativos Curva C (Sul, Sudeste e Centro-Oeste - EPI e Licitação)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("EPI","LICITACAO"); e com a última compra/positivação na empresa nos últimos 150 dias. Ação: atender a cada 14 dias.

### Inativos Curva A (Sul, Sudeste e Centro-Oeste - EPI e Licitação)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("EPI","LICITACAO"); e média faturada no ano com a empresa maior que R$ 25000. Ação: atender a cada 14 dias.

### Inativos Curva B (Sul, Sudeste e Centro-Oeste - EPI e Licitação)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("EPI","LICITACAO"); e média faturada no ano com a empresa maior que R$ 10000. Ação: atender a cada 14 dias.

### Inativos Curva C (Sul, Sudeste e Centro-Oeste - EPI e Licitação)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("EPI","LICITACAO"). Ação: atender a cada 14 dias.

### Ativos Curva A (Sul, Sudeste e Centro-Oeste - Atacado/ Distribuidores)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("ATACADO"); e com a última compra/positivação na empresa nos últimos 120 dias; e média faturada no ano com a empresa maior que R$ 50000. Ação: atender a cada 10 dias.

### Ativos Curva B (Sul, Sudeste e Centro-Oeste - Atacado/ Distribuidores)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("ATACADO"); e com a última compra/positivação na empresa nos últimos 120 dias; e média faturada no ano com a empresa maior que R$ 25000. Ação: atender a cada 14 dias.

### Ativos Curva C (Sul, Sudeste e Centro-Oeste - Atacado/ Distribuidores)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("ATACADO"); e com a última compra/positivação na empresa nos últimos 120 dias. Ação: atender a cada 21 dias.

### Pré-inativos Curva A (Sul, Sudeste e Centro-Oeste - Atacado/ Distribuidores)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("ATACADO"); e com a última compra/positivação na empresa nos últimos 150 dias; e média faturada no ano com a empresa maior que R$ 50000. Ação: atender a cada 7 dias.

### Pré-inativos Curva B (Sul, Sudeste e Centro-Oeste - Atacado/ Distribuidores)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("ATACADO"); e com a última compra/positivação na empresa nos últimos 150 dias; e média faturada no ano com a empresa maior que R$ 25000. Ação: atender a cada 10 dias.

### Pré-inativos Curva C (Sul, Sudeste e Centro-Oeste - Atacado/ Distribuidores)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("ATACADO"); e com a última compra/positivação na empresa nos últimos 150 dias. Ação: atender a cada 14 dias.

### Inativos Curva A (Sul, Sudeste e Centro-Oeste - Atacado/ Distribuidores)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("ATACADO"); e média faturada no ano com a empresa maior que R$ 50000. Ação: atender a cada 10 dias.

### Inativos Curva B (Sul, Sudeste e Centro-Oeste - Atacado/ Distribuidores)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("ATACADO"); e média faturada no ano com a empresa maior que R$ 25000. Ação: atender a cada 10 dias.

### Inativos Curva C (Sul, Sudeste e Centro-Oeste - Atacado/ Distribuidores)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("ATACADO"). Ação: atender a cada 21 dias.

### Ativos Curva A (Sul, Sudeste e Centro-Oeste - Corporativo/ Consumidor)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("CONS. FINAL"); e com a última compra/positivação na empresa nos últimos 120 dias; e média faturada no ano com a empresa maior que R$ 15000. Ação: atender a cada 28 dias.

### Ativos Curva B (Sul, Sudeste e Centro-Oeste - Corporativo/ Consumidor)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("CONS. FINAL"); e com a última compra/positivação na empresa nos últimos 120 dias; e média faturada no ano com a empresa maior que R$ 10000. Ação: atender a cada 28 dias.

### Ativos Curva C (Sul, Sudeste e Centro-Oeste - Corporativo/ Consumidor)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("CONS. FINAL"); e com a última compra/positivação na empresa nos últimos 120 dias. Ação: atender a cada 28 dias.

### Pré-inativos Curva A (Sul, Sudeste e Centro-Oeste - Corporativo/ Consumidor)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("CONS. FINAL"); e com a última compra/positivação na empresa nos últimos 150 dias; e média faturada no ano com a empresa maior que R$ 15000. Ação: atender a cada 14 dias.

### Pré-inativos Curva B (Sul, Sudeste e Centro-Oeste - Corporativo/ Consumidor)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("CONS. FINAL"); e com a última compra/positivação na empresa nos últimos 150 dias; e média faturada no ano com a empresa maior que R$ 10000. Ação: atender a cada 14 dias.

### Pré-inativos Curva C (Sul, Sudeste e Centro-Oeste - Corporativo/ Consumidor)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("CONS. FINAL"); e com a última compra/positivação na empresa nos últimos 150 dias. Ação: atender a cada 14 dias.

### Inativos Curva A (Sul, Sudeste e Centro-Oeste - Corporativo/ Consumidor)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("CONS. FINAL"); e média faturada no ano com a empresa maior que R$ 15000. Ação: atender a cada 28 dias.

### Inativos Curva B (Sul, Sudeste e Centro-Oeste - Corporativo/ Consumidor)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("CONS. FINAL"); e média faturada no ano com a empresa maior que R$ 10000. Ação: atender a cada 28 dias.

### Inativos Curva C (Sul, Sudeste e Centro-Oeste - Corporativo/ Consumidor)

Para clientes da carteira “sul_sudeste_centrooeste”, considerar clientes dos ramos de atividade ("CONS. FINAL"). Ação: atender a cada 28 dias.

### Ativos Curva A (Norte e Nordeste - Matcon, Ferragista, Agropecuária e Home Center)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("MATCON","FERRAGISTA","AGROPECUARIA","HOME CENTER"); e com a última compra/positivação na empresa nos últimos 150 dias; e média faturada no ano com a empresa maior que R$ 25000. Ação: atender a cada 14 dias.

### Ativos Curva B (Norte e Nordeste - Matcon, Ferragista, Agropecuária e Home Center)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("MATCON","FERRAGISTA","AGROPECUARIA","HOME CENTER"); e com a última compra/positivação na empresa nos últimos 150 dias; e média faturada no ano com a empresa maior que R$ 10000. Ação: atender a cada 21 dias.

### Ativos Curva C (Norte e Nordeste - Matcon, Ferragista, Agropecuária e Home Center)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("MATCON","FERRAGISTA","AGROPECUARIA","HOME CENTER"); e com a última compra/positivação na empresa nos últimos 150 dias. Ação: atender a cada 28 dias.

### Pré-inativos Curva A (Norte e Nordeste - Matcon, Ferragista, Agropecuária e Home Center)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("MATCON","FERRAGISTA","AGROPECUARIA","HOME CENTER"); e com a última compra/positivação na empresa nos últimos 180 dias; e média faturada no ano com a empresa maior que R$ 25000. Ação: atender a cada 14 dias.

### Pré-inativos Curva B (Norte e Nordeste - Matcon, Ferragista, Agropecuária e Home Center)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("MATCON","FERRAGISTA","AGROPECUARIA","HOME CENTER"); e com a última compra/positivação na empresa nos últimos 180 dias; e média faturada no ano com a empresa maior que R$ 10000. Ação: atender a cada 14 dias.

### Pré-inativos Curva C (Norte e Nordeste - Matcon, Ferragista, Agropecuária e Home Center)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("MATCON","FERRAGISTA","AGROPECUARIA","HOME CENTER"); e com a última compra/positivação na empresa nos últimos 180 dias. Ação: atender a cada 14 dias.

### Inativos Curva A (Norte e Nordeste - Matcon, Ferragista, Agropecuária e Home Center)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("MATCON","FERRAGISTA","AGROPECUARIA","HOME CENTER"); e média faturada no ano com a empresa maior que R$ 25000. Ação: atender a cada 14 dias.

### Inativos Curva B (Norte e Nordeste - Matcon, Ferragista, Agropecuária e Home Center)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("MATCON","FERRAGISTA","AGROPECUARIA","HOME CENTER"); e média faturada no ano com a empresa maior que R$ 10000. Ação: atender a cada 14 dias.

### Inativos Curva C (Norte e Nordeste - Matcon, Ferragista, Agropecuária e Home Center)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("MATCON","FERRAGISTA","AGROPECUARIA","HOME CENTER"). Ação: atender a cada 14 dias.

### Ativos Curva A (Norte e Nordeste - EPI e Licitação)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("EPI","LICITACAO"); e com a última compra/positivação na empresa nos últimos 150 dias; e média faturada no ano com a empresa maior que R$ 25000. Ação: atender a cada 14 dias.

### Ativos Curva B (Norte e Nordeste - EPI e Licitação)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("EPI","LICITACAO"); e com a última compra/positivação na empresa nos últimos 150 dias; e média faturada no ano com a empresa maior que R$ 10000. Ação: atender a cada 21 dias.

### Ativos Curva C (Norte e Nordeste - EPI e Licitação)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("EPI","LICITACAO"); e com a última compra/positivação na empresa nos últimos 150 dias. Ação: atender a cada 28 dias.

### Pré-inativos Curva A (Norte e Nordeste - EPI e Licitação)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("EPI","LICITACAO"); e com a última compra/positivação na empresa nos últimos 180 dias; e média faturada no ano com a empresa maior que R$ 25000. Ação: atender a cada 14 dias.

### Pré-inativos Curva B (Norte e Nordeste - EPI e Licitação)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("EPI","LICITACAO"); e com a última compra/positivação na empresa nos últimos 180 dias; e média faturada no ano com a empresa maior que R$ 10000. Ação: atender a cada 14 dias.

### Pré-inativos Curva C (Norte e Nordeste - EPI e Licitação)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("EPI","LICITACAO"); e com a última compra/positivação na empresa nos últimos 180 dias. Ação: atender a cada 14 dias.

### Inativos Curva A (Norte e Nordeste - EPI e Licitação)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("EPI","LICITACAO"); e média faturada no ano com a empresa maior que R$ 25000. Ação: atender a cada 14 dias.

### Inativos Curva B (Norte e Nordeste - EPI e Licitação)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("EPI","LICITACAO"); e média faturada no ano com a empresa maior que R$ 10000. Ação: atender a cada 14 dias.

### Inativos Curva C (Norte e Nordeste - EPI e Licitação)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("EPI","LICITACAO"). Ação: atender a cada 14 dias.

### Ativos Curva A (Norte e Nordeste - Atacado/ Distribuidores)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("ATACADO"); e com a última compra/positivação na empresa nos últimos 150 dias; e média faturada no ano com a empresa maior que R$ 50000. Ação: atender a cada 10 dias.

### Ativos Curva B (Norte e Nordeste - Atacado/ Distribuidores)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("ATACADO"); e com a última compra/positivação na empresa nos últimos 150 dias; e média faturada no ano com a empresa maior que R$ 25000. Ação: atender a cada 14 dias.

### Ativos Curva C (Norte e Nordeste - Atacado/ Distribuidores)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("ATACADO"); e com a última compra/positivação na empresa nos últimos 150 dias. Ação: atender a cada 21 dias.

### Pré-inativos Curva A (Norte e Nordeste - Atacado/ Distribuidores)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("ATACADO"); e com a última compra/positivação na empresa nos últimos 180 dias; e média faturada no ano com a empresa maior que R$ 50000. Ação: atender a cada 7 dias.

### Pré-inativos Curva B (Norte e Nordeste - Atacado/ Distribuidores)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("ATACADO"); e com a última compra/positivação na empresa nos últimos 180 dias; e média faturada no ano com a empresa maior que R$ 25000. Ação: atender a cada 10 dias.

### Pré-inativos Curva C (Norte e Nordeste - Atacado/ Distribuidores)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("ATACADO"); e com a última compra/positivação na empresa nos últimos 180 dias. Ação: atender a cada 14 dias.

### Inativos Curva A (Norte e Nordeste - Atacado/ Distribuidores)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("ATACADO"); e média faturada no ano com a empresa maior que R$ 50000. Ação: atender a cada 10 dias.

### Inativos Curva B (Norte e Nordeste - Atacado/ Distribuidores)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("ATACADO"); e média faturada no ano com a empresa maior que R$ 25000. Ação: atender a cada 10 dias.

### Inativos Curva C (Norte e Nordeste - Atacado/ Distribuidores)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("ATACADO"). Ação: atender a cada 21 dias.

### Ativos Curva A (Norte e Nordeste - Corporativo/ Consumidor)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("CONS. FINAL"); e com a última compra/positivação na empresa nos últimos 150 dias; e média faturada no ano com a empresa maior que R$ 15000. Ação: atender a cada 28 dias.

### Ativos Curva B (Norte e Nordeste - Corporativo/ Consumidor)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("CONS. FINAL"); e com a última compra/positivação na empresa nos últimos 150 dias; e média faturada no ano com a empresa maior que R$ 10000. Ação: atender a cada 28 dias.

### Ativos Curva C (Norte e Nordeste - Corporativo/ Consumidor)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("CONS. FINAL"); e com a última compra/positivação na empresa nos últimos 150 dias. Ação: atender a cada 28 dias.

### Pré-inativos Curva A (Norte e Nordeste - Corporativo/ Consumidor)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("CONS. FINAL"); e com a última compra/positivação na empresa nos últimos 180 dias; e média faturada no ano com a empresa maior que R$ 15000. Ação: atender a cada 14 dias.

### Pré-inativos Curva B (Norte e Nordeste - Corporativo/ Consumidor)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("CONS. FINAL"); e com a última compra/positivação na empresa nos últimos 180 dias; e média faturada no ano com a empresa maior que R$ 10000. Ação: atender a cada 14 dias.

### Pré-inativos Curva C (Norte e Nordeste - Corporativo/ Consumidor)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("CONS. FINAL"); e com a última compra/positivação na empresa nos últimos 180 dias. Ação: atender a cada 14 dias.

### Inativos Curva A (Norte e Nordeste - Corporativo/ Consumidor)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("CONS. FINAL"); e média faturada no ano com a empresa maior que R$ 15000. Ação: atender a cada 28 dias.

### Inativos Curva B (Norte e Nordeste - Corporativo/ Consumidor)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("CONS. FINAL"); e média faturada no ano com a empresa maior que R$ 10000. Ação: atender a cada 28 dias.

### Inativos Curva C (Norte e Nordeste - Corporativo/ Consumidor)

Para clientes da carteira “norte_nordeste”, considerar clientes dos ramos de atividade ("CONS. FINAL". A parametrização não contém uma ação operacional reconhecida pelo gerador; revisar o bloco original.

### Clientes que hoje não se enquadraram nas regras padrão

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: não agendar esses clientes.

## regra_033.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_034.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_035.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_036.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_037.gobr

### Regra Padrao da Magnavet - Customizavel: 30 dias para todos os clientes

Aplicar a regra a clientes da carteira “carteira”. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

## regra_038.gobr

### Regra Padrao da Gomes - Customizavel: 7 dias para ativos

Para clientes da carteira “carteira todos”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias.

### Regra Padrao da Gomes - Customizavel: 14 dias para inativos adimplentes

Para clientes da carteira “carteira todos”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Gomes - Customizavel: 30 dias para inativos inadimplentes

Para clientes da carteira “carteira todos”, considerar clientes inativos para o vendedor e inadimplentes. Ação: atender a cada 30 dias.

### Regra Padrao da Gomes - Customizavel: 14 dias para sem vendas

Aplicar a regra a clientes da carteira “carteira todos”. Ação: atender a cada 14 dias.

## regra_039.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_040.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_041.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_042.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_043.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Aplicar a regra a clientes da carteira “empresa toda”. Ação: atender a cada 14 dias.

## regra_044.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_045.gobr

### Regra Padrao da Empresa Customizavel: frequencia semanal para clientes da sandra

Aplicar a regra a clientes da carteira “carteira sandra”. Ação: atender semanalmente (a cada 7 dias); dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customisavel: 30 dias para clientes inativos inadimplentes

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor e inadimplentes. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customisavel: 7 dias para clientes inativos adiplentes

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: atender a cada 7 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customisavel: 14 dias para clientes ativos ou adimplentes ou sem venda

Aplicar a regra a clientes da carteira “empresa toda”. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

## regra_046.gobr

### Regra Padrao da Empresa Customizavel: 7 dias para ativos

Para clientes da carteira “carteira todos”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias.

### Regra Padrao da Empresa Customizavel: 14 dias para inativos adimplentes

Para clientes da carteira “carteira todos”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Empresa Customizavel: 30 dias para inativos inadimplentes

Para clientes da carteira “carteira todos”, considerar clientes inativos para o vendedor e inadimplentes. Ação: atender a cada 30 dias.

### Regra Padrao da Empresa Customizavel: 7 dias para sem vendas

Aplicar a regra a clientes da carteira “carteira todos”. Ação: atender a cada 7 dias.

## regra_047.gobr

### Regra Padrao da STO Customizavel: nao agendar CPF

Para clientes da carteira “regra padrao”, considerar clientes pessoa física. Ação: não agendar esses clientes.

### Regra Padrao da STO Customizavel: 7 dias para ativos adimplentes

Para clientes da carteira “regra padrao”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 7 dias.

### Regra Padrao da STO Customizavel: 14 dias para ativos inadimplentes

Para clientes da carteira “regra padrao”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da STO Customizavel: 14 dias para inativos adimplentes

Para clientes da carteira “regra padrao”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da STO Customizavel: nao agendar inativos inadimplentes

Para clientes da carteira “regra padrao”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da STO Customizavel: 14 dias para clientes sem vendas

Para clientes da carteira “regra padrao”, considerar clientes sem vendas. Ação: atender a cada 14 dias.

## regra_048.gobr

### Regra Padrao da Empresa Customizavel: 14 dias para ativos adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Empresa Customizavel: 7 dias para ativos inadimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 7 dias.

### Regra Padrao da Empresa Customizavel: 30 dias para inativos adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 30 dias.

### Regra Padrao da Empresa Customizavel: 60 dias para inativos inadimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor e inadimplentes. Ação: atender a cada 60 dias.

### Regra Padrao da Empresa Customizavel: 30 dias para clientes sem venda (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes sem vendas. Ação: atender a cada 30 dias.

### Regra Padrao da Empresa Customizavel: 30 dias para clientes prospects (televendas)

Aplicar a regra a clientes da carteira “carteira televendas”. Ação: atender a cada 30 dias.

### Regra Padrao da Empresa Customizavel: 7 dias para clientes ativos adimplentes (campo)

Para clientes da carteira “carteira campo”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 7 dias.

### Regra Padrao da Empresa Customizavel: 14 dias para clientes ativos inadimplentes (campo)

Para clientes da carteira “carteira campo”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Empresa Customizavel: 14 dias para clientes inativos ativos (campo)

Para clientes da carteira “carteira campo”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Empresa Customizavel: 30 dias para clientes inativos inadimplentes (campo)

Para clientes da carteira “carteira campo”, considerar clientes inativos para o vendedor e inadimplentes. Ação: atender a cada 30 dias.

### Regra Padrao da Empresa Customizavel: 14 dias para clientes sem venda (campo)

Para clientes da carteira “carteira campo”, considerar clientes sem venda. Ação: atender a cada 14 dias.

### Regra Padrao da Empresa Customizavel: 14 dias para clientes prospects (campo)

Aplicar a regra a clientes da carteira “carteira campo”. Ação: atender a cada 14 dias.

## regra_049.gobr

### Nao agendar baixados receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Clientes Ativos

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: atender a cada 14 dias.

### Risco de Inatividade

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 45 dias; e sem compra/positivação nos últimos 30 dias. Ação: atender a cada 7 dias.

### Inativos

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação nos últimos 45 dias. Ação: atender a cada 14 dias.

### Clientes Prospects

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 7 dias.

## regra_050.gobr

### Regra Padrao da Duferro Customizavel: 7 dias para adimplentes

Para clientes da carteira “empresa toda”, considerar clientes adimplentes. Ação: atender a cada 7 dias.

### Regra Padrao da Duferro Customizavel: 14 dias para ativos inadimplentes

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Duferro Customizavel: Nao agendar inativos inadimplentes

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Duferro Customizavel: 7 dias para clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: atender a cada 7 dias.

## regra_051.gobr

### Regra Padrao da Empresa Customizavel: semanal para clientes ativos e adimplentes

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender semanalmente (a cada 7 dias); dar preferência de atendimento aos dias úteis e ao sábado.

### Regra Padrao da Empresa Customizavel: 14 dias para clientes ativos e inadimplentes

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Regra Padrao da Empresa Customizavel: 14 dias para clientes inativos e adimplentes

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Regra Padrao da Empresa Customizavel: nao agendar clientes inativos e inadimplentes

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Empresa Customizavel: 14 dias para clientes sem venda

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis e ao sábado.

## regra_052.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_053.gobr

### Regra Padrao da Empresa Customizavel: 14 dias para ativos adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Empresa Customizavel: 30 dias para ativos inadimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 30 dias.

### Regra Padrao da Empresa Customizavel: 7 dias para inativos adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 7 dias.

### Regra Padrao da Empresa Customizavel: nao agendar inativos inadimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Empresa Customizavel: 7 dias para sem vendas (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes sem vendas. Ação: atender a cada 7 dias.

### Regra Padrao da Empresa Customizavel: configuracao padrao de inativos

Para clientes da carteira “regra padrao”, considerar clientes inativos para o vendedor. Ação: aplicar frequência de inativos  da empresa; usar a preferência de dias configurada pelo vendedor.

### Regra Padrao da Empresa Customizavel: configuracao padrao de ativos

Para clientes da carteira “regra padrao”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa; usar a preferência de dias configurada pelo vendedor.

### Regra Padrao da Empresa Customizavel: configuracao padrao de sem vendas

Para clientes da carteira “regra padrao”, considerar clientes sem vendas. Ação: usar a frequência média dos clientes inativos da empresa; usar a preferência de dias configurada pelo vendedor.

## regra_054.gobr

### Regra Padrao da Empresa Customizavel: 14 dias para clientes sem venda

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: atender a cada 14 dias.

### Regra Padrao da Empresa Customizavel: 30 dias para adimplentes

Para clientes da carteira “empresa toda”, considerar clientes adimplentes. Ação: atender a cada 30 dias.

### Regra Padrao da Empresa Customizavel: Não agendar inadimplentes

Para clientes da carteira “empresa toda”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

## regra_055.gobr

### Regra Padrao da NB Distribuidora Customizavel: 14 dias para adimplentes

Para clientes da carteira “carteira televendas”, considerar clientes adimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da NB Distribuidora: 30 dias para ativos inadimplentes

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 30 dias.

### Regra Padrao da NB Distribuidora: 30 dias para clientes sem venda

Para clientes da carteira “carteira televendas”, considerar clientes sem venda. Ação: atender a cada 30 dias.

### Regra Padrao da NB Distribuidora: nao agendar inativos inadimplentes

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da NB Distribuidora Customizavel: 30 dias para clientes sem venda (capital)

Para clientes da carteira “carteira capital”, considerar clientes sem venda. Ação: atender a cada 30 dias.

### Regra Padrao da NB Distribuidora Customizavel: 30 dias para clientes inadimplentes (capital)

Para clientes da carteira “carteira capital”, considerar clientes inadimplentes. Ação: atender a cada 30 dias.

### Regra Padrao da NB Distribuidora Customizavel: 14 dias para clientes adimplentes (capital)

Aplicar a regra a clientes da carteira “carteira capital”. Ação: atender a cada 14 dias.

### Regra Padrao da NB Distribuidora Customizavel: 30 dias para todos os clientes (interior)

Aplicar a regra a clientes da carteira “carteira interior”. Ação: atender a cada 30 dias.

## regra_056.gobr

### Regra Padrao da Destra - Customizavel: 30 dias para clientes sem vendas (RCA 50 e 53)

Para clientes da carteira “carteira prospec”, considerar clientes sem vendas. Ação: atender a cada 30 dias; usar a preferência de dias configurada pelo vendedor.

### Regra Padrao da Destra - Customizavel: nao agendar clientes que ja compraram (RCA 50 e 53)

Aplicar a regra a clientes da carteira “carteira prospec”. Ação: não agendar esses clientes.

### Regra Padrao da Destra - Customizavel: 14 dias para Adimplentes ativos

Para clientes da carteira “regra padrao”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 14 dias; usar a preferência de dias configurada pelo vendedor.

### Regra Padrao da Destra - Customizavel: 30 dias para Adimplentes inativos

Para clientes da carteira “regra padrao”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 30 dias; usar a preferência de dias configurada pelo vendedor.

### Regra Padrao da Destra - Customizavel: 30 dias para ativos inadimplentes

Para clientes da carteira “regra padrao”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 30 dias; usar a preferência de dias configurada pelo vendedor.

### Regra Padrao da Destra - Customizavel: nao agendar inativos inadimplentes

Para clientes da carteira “regra padrao”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Destra - Customizavel: 30 dias para clientes sem vendas

Para clientes da carteira “regra padrao”, considerar clientes sem vendas. Ação: atender a cada 30 dias; usar a preferência de dias configurada pelo vendedor.

## regra_057.gobr

### Freq. de 30d para Prospects

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 30 dias.

### Freq. de 25d para Ativos (Adimplentes e Inadimplentes)

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor. Ação: atender a cada 25 dias.

### Freq. de 30d para Inativos (Adimplentes e Inadimplentes)

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 30 dias.

## regra_058.gobr

### Regra Padrao da Otima Atacado: 14 dias para clientes inadimplentes (televendas)

Para clientes da carteira “televendas”, considerar clientes inadimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Otima Atacado: Frequência de atendimento baseada no histórico de vendas, ou até de 14 dias (televendas)

Aplicar a regra a clientes da carteira “televendas”. Ação: aplicar frequência do histórico ou no máximo de 14 dias.

### Regra Padrao da Otima Atacado: 7 dias para clientes adimplentes

Para clientes da carteira “campo”, considerar clientes adimplentes. Ação: atender a cada 7 dias.

### Regra Padrao da Otima Atacado: 14 dias para clientes ativos inadimplentes

Para clientes da carteira “campo”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 14 dias.

### Regra Padrao dda Otima Atacado: 60 dias para clientes inativos inadimplentes

Para clientes da carteira “campo”, considerar clientes inativos para o vendedor e inadimplentes. Ação: atender a cada 60 dias.

### Regra Padrao dda Otima Atacado: 14 dias para clientes sem venda (campo)

Para clientes da carteira “campo”, considerar clientes sem venda. Ação: atender a cada 14 dias.

## regra_059.gobr

### Hospidrogas: Não agendar ramos de atividade específicos

Para clientes vinculados ao time “televendas”, considerar clientes fora dos ramos de atividade ("2","3","4","5","6","7","8","10","11","12","14","15","17","18","19"). Ação: não agendar esses clientes.

### Hospidrogas: Freq. 30d para prospects e ramos de atividade igual 2, 7, 11, 12, 14 ou 19

Para clientes vinculados ao time “televendas”, considerar clientes no ciclo de vida prospect com a empresa e dos ramos de atividade ("2","7","11","12","14","19"). Ação: atender a cada 30 dias.

### Hospidrogas: Freq. 30d para ativos e ramos de atividade igual 3, 4, 6, 8, 15 ou 18

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor e dos ramos de atividade ("3","4","6","8","15","18"). Ação: atender a cada 30 dias.

### Hospidrogas: Freq. 15d para ativos e ramos de atividade igual 7 ou 17

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor e dos ramos de atividade ("7","17"). Ação: atender a cada 15 dias.

### Hospidrogas: Freq. 7d para ativos e ramos de atividade igual 10, 11, 14 ou 19

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor e dos ramos de atividade ("10","11","14","19"). Ação: atender a cada 7 dias.

### Hospidrogas: Freq. 5d para ativos e ramos de atividade igual 2 ou 12

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor e dos ramos de atividade ("2","12"). Ação: atender a cada 5 dias.

### Hospidrogas: Freq. 30d para inativos e ramos de atividade igual 3, 4, 6, 8, 15 ou 18

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("3","4","6","8","15","18"). Ação: atender a cada 30 dias.

### Hospidrogas: Freq. 20d para inativos e ramos de atividade igual 17

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("17"). Ação: atender a cada 20 dias.

### Hospidrogas: Freq. 15d para inativos e ramos de atividade igual 10

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("10"). Ação: atender a cada 15 dias.

### Hospidrogas: Freq. 10d para inativos e ramos de atividade igual 11 ou 19

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("11","19"). Ação: atender a cada 10 dias.

### Hospidrogas: Freq. 5d para inativos e ramos de atividade igual 2, 7, 12 ou 14

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 5 dias.

## regra_060.gobr

### Regra Padrao do goVendas: Frequencia semanal para clientes ativos

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias.

### Regra Padrao do goVendas: Frequencia quinzenal para clientes inativos

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 15 dias.

### Regra Padrao do goVendas: Frequencia de 7 dias para clientes ativos (campo)

Para clientes vinculados ao time “campo”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias; marcar a parametrização como fixa.

### Regra Padrao do goVendas: Frequencia de 14 dias para clientes inativos (campo)

Aplicar a regra a clientes vinculados ao time “campo”. Ação: atender a cada 15 dias; marcar a parametrização como fixa.

## regra_061.gobr

### Regra Padrao da Gesiane Customizavel - Frequencia de 14 dias para clientes inativos da Gesiane

Para clientes da carteira “carteira Gesiane”, considerar clientes inativos para o vendedor. Ação: atender a cada 14 dias.

### Regra Padrao da Gesiane Customizavel - Frequencia de 14 dias para clientes sem venda da Gesiane

Para clientes da carteira “carteira Gesiane”, considerar clientes sem venda. Ação: aplicar frequência de  14 dias.

### Regra Padrao da Gesiane Customizavel - Frequencia de 14 dias para clientes ativos da Gesiane

Para clientes da carteira “carteira Gesiane”, considerar clientes ativos para o vendedor. Ação: atender a cada 14 dias.

### Regra Padrao da Empresa Customizavel - Nao agendar inativos inadimplentes (campo)

Para clientes da carteira “carteira campo”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao do goVendas Customizavel - Frequencia de 14 dias para ativos ou adimplentes (campo)

Aplicar a regra a clientes da carteira “carteira campo”. Ação: atender a cada 14 dias.

### Regra Padrao da Empresa Customizavel - Nao agendar inativos inadimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Empresa Customizavel - Nao agendar clientes sem venda (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes sem venda. Ação: não agendar esses clientes.

### Regra Padrao do goVendas Customizavel - Frequencia de 14 dias para ativos ou adimplentes (televendas)

Aplicar a regra a clientes da carteira “carteira televendas”. Ação: atender a cada 14 dias.

## regra_062.gobr

### Regra Padrao da Royal Pet - Customizavel: Frequencia de 7 dias para ativos adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 7 dias.

### Regra Padrao da Royal Pet -  Customizavel: Frequencia de 14 dias para ativos inadimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Royal Pet - Customizavel: Frequencia de 14 dias para inativos adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Royal Pet - Customizavel: Não agendar inativos inadimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Royal Pet - Customizavel: Frequencia de 14 dias para clientes sem vendas (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes sem venda. Ação: atender a cada 14 dias.

### Regra Padrao da Royal Pet - Customizavel: Frequencia de 7 dias para ativos adimplentes (campo)

Para clientes da carteira “carteira campo”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 7 dias.

### Regra Padrao da Royal Pet -  Customizavel: Frequencia de 14 dias para ativos inadimplentes (campo)

Para clientes da carteira “carteira campo”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Royal Pet - Customizavel: Frequencia de 14 dias para inativos adimplentes (campo)

Para clientes da carteira “carteira campo”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Royal Pet - Customizavel: Frequencia de 30 dias para inativos adimplentes (campo)

Para clientes da carteira “carteira campo”, considerar clientes inativos para o vendedor e inadimplentes. Ação: atender a cada 30 dias.

### Regra Padrao da Royal Pet - Customizavel: Frequencia de 14 dias para clientes sem vendas (campo)

Para clientes da carteira “carteira campo”, considerar clientes sem venda. Ação: atender a cada 14 dias.

## regra_063.gobr

### Regra Padrao da Verteiler - Customizavel: 30 dias para clientes ativos (campo)

Para clientes da carteira “carteira campo”, considerar clientes ativos para o vendedor. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Verteiler - Customizavel: 30 dias para clientes inativos (campo)

Para clientes da carteira “carteira campo”, considerar clientes inativos para o vendedor. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Verteiler - Customizavel: 30 dias para clientes sem venda (campo)

Para clientes da carteira “carteira campo”, considerar clientes sem venda. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Verteiler - Customizavel: 30 dias para clientes ativos (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira); evitar choque/conflito de atendimento no time("time campo").

### Regra Padrao da Verteiler - Customizavel: 30 dias para clientes inativos(televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira); evitar choque/conflito de atendimento no time("time campo").

### Regra Padrao da Verteiler - Customizavel: 30 dias para clientes sem venda (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes sem venda. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira); evitar choque/conflito de atendimento no time("time campo").

## regra_064.gobr

### Regra Padrao da Royal Pet - Customizavel: Frequencia de 7 dias para ativos adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 7 dias.

### Regra Padrao da Royal Pet -  Customizavel: Frequencia de 14 dias para ativos inadimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Royal Pet - Customizavel: Frequencia de 14 dias para inativos adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Royal Pet - Customizavel: Não agendar inativos inadimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Royal Pet - Customizavel: Frequencia de 14 dias para clientes sem vendas (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes sem venda. Ação: atender a cada 14 dias.

### Regra Padrao da Royal Pet - Customizavel: Frequencia de 7 dias para ativos adimplentes (campo)

Para clientes da carteira “carteira campo”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 7 dias.

### Regra Padrao da Royal Pet -  Customizavel: Frequencia de 14 dias para ativos inadimplentes (campo)

Para clientes da carteira “carteira campo”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Royal Pet - Customizavel: Frequencia de 14 dias para inativos adimplentes (campo)

Para clientes da carteira “carteira campo”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Royal Pet - Customizavel: Frequencia de 30 dias para inativos adimplentes (campo)

Para clientes da carteira “carteira campo”, considerar clientes inativos para o vendedor e inadimplentes. Ação: atender a cada 30 dias.

### Regra Padrao da Royal Pet - Customizavel: Frequencia de 14 dias para clientes sem vendas (campo)

Para clientes da carteira “carteira campo”, considerar clientes sem venda. Ação: atender a cada 14 dias.

## regra_065.gobr

### Regra Padrao da Empresa Customizavel: quinzenal para clientes que compram até 30 dias

Para clientes da carteira “televendas”, considerar clientes atividade de 30 dias. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel: mensal para clientes que não compram a mais de 30 dias

Para clientes da carteira “televendas”, considerar clientes inatividade de 30 dias. Ação: atender a cada 28 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel: mensal para clientes que nunca comprou

Aplicar a regra a clientes da carteira “televendas”. Ação: atender a cada 28 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

## regra_066.gobr

### Regra Padrao da Sul Frios - Customizavel: 7 dias para clientes ativos adimplentes (Internos)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 7 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Sul Frios - Customizavel: 14 dias para clientes ativos inadimplentes (Internos)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Sul Frios - Customizavel: 30 dias para clientes inativos adimplentes (Internos)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Sul Frios - Customizavel: Nao agendar clientes inativos inadimplentes (Internos)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Sul Frios - Customizavel: Nao agendar clientes sem vendas (Internos)

Para clientes da carteira “carteira televendas”, considerar clientes sem venda. Ação: não agendar esses clientes.

### Regra Padrao da Sul Frios - Customizavel: 7 dias para clientes ativos (Externos)

Para clientes da carteira “carteira campo”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Sul Frios - Customizavel: 30 dias para clientes inativos adimplentes (Externos)

Para clientes da carteira “carteira campo”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Sul Frios - Customizavel: Nao agendar clientes inativos inadimplentes (Externos)

Para clientes da carteira “carteira campo”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Sul Frios - Customizavel: Nao agendar clientes sem vendas (Externos)

Para clientes da carteira “carteira campo”, considerar clientes sem venda. Ação: não agendar esses clientes.

## regra_067.gobr

### Regra Padrao da NutriPet - Customizavel: 14 dias para clientes ativos (televendas)

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da NutriPet - Customizavel: 30 dias para clientes inativos (televendas)

Para clientes vinculados ao time “televendas”, considerar clientes inativos para o vendedor. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da NutriPet - Customizavel: 7 dias para clientes sem venda (televendas)

Para clientes vinculados ao time “televendas”, considerar clientes sem venda. Ação: atender a cada 7 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da NutriPet - Customizavel: 20 dias para clientes ativos adimplentes (capital)

Para clientes da carteira “capital”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 20 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da NutriPet - Customizavel: 20 dias para clientes ativos inadimplentes (capital)

Para clientes da carteira “capital”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 20 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da NutriPet - Customizavel: 30 dias para clientes inativos adimplentes (capital)

Para clientes da carteira “capital”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da NutriPet - Customizavel: 30 dias para clientes inativos inadimplentes (capital)

Para clientes da carteira “capital”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da NutriPet - Customizavel: 14 dias para clientes sem venda (capital)

Para clientes da carteira “capital”, considerar clientes sem venda. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da NutriPet - Customizavel: 21 dias para clientes ativos (interior)

Para clientes vinculados ao time “interior”, considerar clientes ativos para o vendedor. Ação: atender a cada 21 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da NutriPet - Customizavel: 21 dias para clientes inativos adimplentes (interior)

Para clientes vinculados ao time “interior”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 21 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da NutriPet - Customizavel: 42 dias para clientes inativos inadimplentes (interior)

Para clientes vinculados ao time “interior”, considerar clientes inativos para o vendedor e inadimplentes. Ação: atender a cada 42 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da NutriPet - Customizavel: clientes inativos inadimplentes (interior)

Para clientes da carteira “capital”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da NutriPet - Customizavel: 14 dias para clientes sem venda (interior)

Para clientes vinculados ao time “interior”, considerar clientes sem venda. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

## regra_068.gobr

### Regra Padrao da Playpet Customizavel: nao agendar plano veterinario

Para clientes da carteira “carteira campo”, considerar clientes dos ramos de atividade ("17"). Ação: não agendar esses clientes.

### Regra Padrao da Playpet Customizavel: nao agendar clientes pessoa fisica

Para clientes da carteira “carteira campo”, considerar clientes pessoa física. Ação: não agendar esses clientes.

### Regra Padrao da Playpet Customizavel: 30 dias para ativos adimplentes

Para clientes da carteira “carteira campo”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 30 dias.

### Regra Padrao da Playpet Customizavel: 21 dias para clientes sem venda

Para clientes da carteira “carteira campo”, considerar clientes sem venda. Ação: atender a cada 21 dias.

### Regra Padrao da Playpet Customizavel: nao agendar inadimplentes ou inativos

Aplicar a regra a clientes da carteira “carteira campo”. Ação: não agendar esses clientes.

### Regra Padrao da Playpet Customizavel: Nao agendar inadimplentes

Para clientes da carteira “carteira televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Playpet Customizavel: 14 dias para ativos adimplentes

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Playpet Customizavel: 30 dias quando inativos adimplentes

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 30 dias.

### Regra Padrao da Playpet Customizavel: 14 dias para sem venda

Para clientes da carteira “carteira televendas”, considerar clientes sem venda. Ação: atender a cada 14 dias.

## regra_069.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_070.gobr

### Regra Padrao da Tripet - Customizavel: Nao agendar clientes inativos inadimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Tripet - Customizavel: 14 dias para clientes ativos (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Tripet - Customizavel: 30 dias para clientes inativos adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Tripet - Customizavel: 30 dias para clientes sem venda (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes sem venda. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Tripet - Customizavel: 14 dias para clientes ativos (campo)

Para clientes vinculados ao time “campo”, considerar clientes ativos para o vendedor. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Tripet - Customizavel: 30 dias para clientes inativos (campo)

Para clientes vinculados ao time “campo”, considerar clientes inativos para o vendedor. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Tripet - Customizavel: nao agendar clientes sem venda (campo)

Para clientes vinculados ao time “campo”, considerar clientes sem venda. Ação: não agendar esses clientes.

## regra_071.gobr

### Regra Padrao da Palmed: 14 dias para inativos e inadimplentes

Para clientes da carteira “carteira televendas pi”, “carteira televendas pb”, considerar clientes inativos para o vendedor e inadimplentes. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira); evitar choque/conflito de atendimento na rota com time("campo").

### Regra Padrao da Palmed: Maximo 7 dias - PI

Aplicar a regra a clientes da carteira “carteira televendas pi”. Ação: aplicar frequência do histórico ou no máximo semanal(); dar preferência de atendimento aos dias úteis e ao sábado; evitar choque/conflito de atendimento na rota com time("campo").

### Regra Padrao da Palmed: maximo 7 dias - PB

Aplicar a regra a clientes da carteira “carteira televendas pb”. Ação: aplicar frequência do histórico ou no máximo semanal(); dar preferência de atendimento aos dias úteis (segunda a sexta-feira); evitar choque/conflito de atendimento na rota com time("campo").

### Regra Padrao da Palmed: 14 dias para inativos e inadimplentes - Tocantins

Para clientes da carteira “carteira tocantins”, considerar clientes inativos para o vendedor e inadimplentes. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira); evitar choque/conflito de atendimento na rota com time("campo").

### Regra Padrao da Palmed: semanal para ativos

Aplicar a regra a clientes da carteira “carteira tocantins”. Ação: aplicar frequência do histórico ou no máximo semanal(); dar preferência de atendimento aos dias úteis e ao sábado; evitar choque/conflito de atendimento na rota com time("campo").

### Regra Padrao da Palmed: semanal para ativos e adimplentes (segunda a sexta) - Time Televendas

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor e adimplentes. Ação: aplicar frequência do histórico ou no máximo semanal(); dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Palmed: quinzenal para ativos e inadimplente (segunda a sexta) - Time Televendas

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Palmed: semanal exceto na segunda para inativos adimplentes (terca a sexta) - Time Televendas

Para clientes vinculados ao time “televendas”, considerar clientes inativos para o vendedor e adimplentes. Ação: aplicar frequência do histórico ou no máximo semanal(); definir preferência de atendimento na segunda e na terça e na quarta e na quinta e na sexta.

### Regra Padrao da Palmed: 30 dias para inativos e inadimplentes (terca a sexta) - Time Televendas

Para clientes vinculados ao time “televendas”, considerar clientes inativos para o vendedor e inadimplentes. Ação: atender a cada 30 dias; definir preferência de atendimento na segunda e na terça e na quarta e na quinta e na sexta.

### Regra Padrao da Palmed: 7 dias de terca a sexta - Time Televendas

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: aplicar frequência do histórico ou no máximo semanal(); definir preferência de atendimento na segunda e na terça e na quarta e na quinta e na sexta.

### Regra Padrao da Palmed: 7 dias para todos os clientes - Time de Campo

Aplicar a regra a clientes vinculados ao time “campo”. Ação: atender semanalmente (a cada 7 dias).

## regra_072.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_073.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_074.gobr

### Regra Padrao da Empresa Customizavel: 45 dias para inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: atender a cada 45 dias; usar a preferência de dias configurada pelo vendedor.

### Regra Padrao da Empresa Customizavel: 21 dias para ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: atender a cada 21 dias; usar a preferência de dias configurada pelo vendedor.

### Regra Padrao da Empresa Customizavel: 45 dias quando sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem vendas. Ação: atender a cada 45 dias; usar a preferência de dias configurada pelo vendedor.

## regra_075.gobr

### Regra Padrao da Empresa Customizavel: nao agendar inadimplentes

Para clientes da carteira “carteira televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Empresa Customizavel: 7 dias para ativos adimplentes

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 7 dias.

### Regra Padrao da Empresa Customizavel: 14 dias para inativos adimplentes

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Empresa Customizavel: 14 dias para sem venda

Para clientes da carteira “carteira televendas”, considerar clientes sem venda. Ação: atender a cada 14 dias.

## regra_076.gobr

### Não agendar inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Não agendar bloqueados

Para clientes vinculados ao time “televendas”, considerar clientes bloqueados. Ação: não agendar esses clientes.

### Não agendar inativos

Para clientes vinculados ao time “televendas”, considerar clientes inativos para a empresa. Ação: não agendar esses clientes.

### Tem compra em até 20 dias atrás

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa nos últimos 20 dias. Ação: não agendar esses clientes.

### Agendamento padrão - Rota

Para clientes vinculados ao time “televendas”, considerar clientes data da rota hoje. Ação: atender a cada 1 dia.

### Clientes prospects

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 7 dias.

### Cliente ativado

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com a empresa. Ação: atender a cada 15 dias.

### Compra regularmente

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa nos últimos 30 dias; e frequência histórica menor que 30 dias. Ação: aplicar frequência do histórico ou no mínimo de 5 dias e no máximo de 30 dias.

### Em ruptura

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa entre 31 e 90 dias atrás. Ação: atender a cada 15 dias.

### Fora de rota

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: não agendar esses clientes.

## regra_077.gobr

### Não agendar bloqueados

Para clientes vinculados ao time “televendas”, considerar clientes bloqueados. Ação: não agendar esses clientes.

### Não agendar clientes inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Não agendar clientes com compra nos últimos 30d

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: não agendar esses clientes.

### Freq. de 14d para clientes prospects

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 14 dias.

### Freq. de 7d para clientes ativos

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Ativo na empresa. Ação: atender a cada 7 dias.

### Freq. de 14d para clientes inativos

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 14 dias.

## regra_078.gobr

### Regra Padrao da Empresa Customizavel: quinzenal para clientes ativos mas inadimplentes

Para clientes da carteira “empresa comercial bh”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel: semanal para clientes ativos e adimplentes

Para clientes da carteira “empresa comercial bh”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel: mensal para clientes inativos e inadimplentes

Para clientes da carteira “empresa comercial bh”, considerar clientes inativos para o vendedor e inadimplentes. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel: quinzenal para clientes inativos e adimplentes

Para clientes da carteira “empresa comercial bh”, considerar clientes inativos para o vendedor. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel: quinzenal para clientes sem vendas

Para clientes da carteira “empresa comercial bh”, considerar clientes sem vendas. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

## regra_079.gobr

### Girardi: Não agendar ramos de atividade diferente de 12, 13, 14, 15, 16, 17, 18 e 19

Para clientes vinculados ao time “televendas”, considerar clientes fora dos ramos de atividade ("12","13","14","15","16","17","18","19"). Ação: não agendar esses clientes.

### Girardi: 7d para ramo de atividade 12

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("12"). Ação: atender a cada 7 dias.

### Girardi: 14d para ramos de atividade 13, 14, 15, 16, 17, 18 e 19

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 14 dias.

## regra_080.gobr

### Regra Padrao da Empresa Customizavel: mensal para inativos com cnae do erp que inicia com ("03","47","27")

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor e cnae do erp inicia com("03","47","27"). Ação: atender mensalmente (a cada 30 dias); usar a preferência de dias configurada pelo vendedor.

### Regra Padrao da Empresa Customizavel: 15 dias para inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: atender quinzenalmente (a cada 15 dias); usar a preferência de dias configurada pelo vendedor.

### Regra Padrao da Empresa Customizavel: mensal para ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: atender mensalmente (a cada 30 dias); usar a preferência de dias configurada pelo vendedor.

### Regra Padrao da Empresa Customizavel: 15 dias para inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: atender quinzenalmente (a cada 15 dias); usar a preferência de dias configurada pelo vendedor.

### Regra Padrao da Empresa Customizavel: mensal para clientes sem venda

Para clientes da carteira “empresa toda”, considerar clientes sem vendas. Ação: atender mensalmente (a cada 30 dias); usar a preferência de dias configurada pelo vendedor.

## regra_081.gobr

### Regra Padrao da Empresa Customizavel: semanal para clientes ativos e adimplentes

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: atender semanalmente (a cada 7 dias); dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel: 21 dias para clientes ativos e inadimplentes

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 21 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel: 30 dias para clientes inativos e adimplentes

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel: nao agendar inativos e inadimplentes

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Empresa Customizavel: 30 dias para clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem vendas. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

## regra_082.gobr

### Regra Padrao da Empresa Customizavel: semanal para clientes ativos adimplentes

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender semanalmente (a cada 7 dias); dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel: 14 dias para clientes ativos inadimplentes

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel: 30 dias para clientes inativos adimplentes

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel: nao agendar inativos inadimplentes

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Empresa Customizavel: 30 dias para clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem vendas. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

## regra_083.gobr

### Regra Padrao do goVendas Customizavel - Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel - Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel - Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_084.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_085.gobr

### Regra Padrao da Empresa Customizavel: 7 dias para adimplentes

Para clientes da carteira “empresa perola”, considerar clientes adimplentes. Ação: atender semanalmente (a cada 7 dias).

### Regra Padrao da Empresa Customizavel: 14 dias para ativos e inadimplentes

Para clientes da carteira “empresa perola”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Empresa Customizavel: 30 dias para inativos e inadimplentes

Para clientes da carteira “empresa perola”, considerar clientes inativos para o vendedor e inadimplentes. Ação: atender a cada 30 dias.

### Regra Padrao da Empresa Customizavel: 7 dias para cliente sem vendas

Aplicar a regra a clientes da carteira “empresa perola”. Ação: atender semanalmente (a cada 7 dias); dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

## regra_086.gobr

### Regra Padrao da Taiken Customizavel: 10 dias para ativos adimplentes

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 10 dias.

### Regra Padrao da Taiken Customizavel: 14 dias para ativos inadimplentes

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Taiken Customizavel: 14 dias para inativos adimplentes

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Taiken Customizavel: 90 dias para inativos inadimplentes

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor e inadimplentes. Ação: atender a cada 90 dias.

### Regra Padrao da Taiken Customizavel: 21 dias para clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: atender a cada 21 dias.

## regra_087.gobr

### Regra Padrao da Empresa Customizavel: 14 dias para ativos adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao do Empresa Customizavel: 30 dias para ativos inadimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao do Empresa Customizavel: 30 dias para inativos adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao do Empresa Customizavel: 60 dias para inativos inadimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor e inadimplentes. Ação: atender a cada 60 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao do Empresa Customizavel: 30 dias para clientes sem venda (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes sem venda. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao do Empresa Customizavel: 14 dias para adimplentes (campo)

Para clientes da carteira “carteira campo”, considerar clientes adimplentes. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao do Empresa Customizavel: 30 dias para clientes inadimplentes (campo)

Para clientes da carteira “carteira campo”, considerar clientes inadimplentes. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao do Empresa Customizavel: 30 dias para clientes sem venda (campo)

Para clientes da carteira “carteira campo”, considerar clientes sem venda. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

## regra_088.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_089.gobr

### Freq. de 7d para Prospects

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 7 dias.

### Freq. de 7d para Ativos Adimplentes

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor; e adimplentes. Ação: atender a cada 7 dias.

### Freq. de 14d para Ativos Inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor. Ação: atender a cada 14 dias.

### Freq. de 7d para Inativos Adimplentes

Para clientes vinculados ao time “televendas”, considerar clientes adimplentes. Ação: atender a cada 7 dias.

### Freq. de 14d para Inativos Inadimplentes

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 14 dias.

## regra_090.gobr

### Regra Padrao da Empresa Customizavel: semanal para ativos

Para clientes da carteira “carteira fixa”, considerar clientes ativos para o vendedor. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na segunda e na terça e na quarta e na quinta e na sexta e no sábado.

### Regra Padrao da Empresa Customizavel: 14 dias para inativos

Para clientes da carteira “carteira fixa”, considerar clientes inativos para o vendedor. Ação: atender a cada 14 dias; definir preferência de atendimento na segunda e na terça e na quarta e na quinta e na sexta e no sábado.

### Regra Padrao da Empresa Customizavel: 14 dias para clientes sem venda

Para clientes da carteira “carteira fixa”, considerar clientes sem venda. Ação: atender a cada 14 dias; definir preferência de atendimento na segunda e na terça e na quarta e na quinta e na sexta e no sábado.

## regra_091.gobr

### Regra Padrao da Empresa Customizavel: 14 dias para ativos (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor. Ação: atender a cada 14 dias.

### Regra Padrao da Empresa Customizavel: 60 dias para inativos (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor. Ação: atender a cada 60 dias.

### Regra Padrao da Empresa Customizavel: 14 dias para clientes sem vendas (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes sem vendas. Ação: atender a cada 14 dias.

### Regra Padrao da Empresa Customizavel: 7 dias ativos adimplentes (campo)

Para clientes da carteira “carteira campo”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 7 dias.

### Regra Padrao da Empresa Customizavel: 14 dias para ativos inadimplentes (campo)

Para clientes da carteira “carteira campo”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Empresa Customizavel: 30 dias inativos adimplentes (campo)

Para clientes da carteira “carteira campo”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 30 dias.

### Regra Padrao da Empresa Customizavel: 60 dias para inativos inadimplentes (campo)

Para clientes da carteira “carteira campo”, considerar clientes inativos para o vendedor e inadimplentes. Ação: atender a cada 60 dias.

### Regra Padrao da Empresa Customizavel: 14 dias para clientes sem vendas (campo)

Para clientes da carteira “carteira campo”, considerar clientes sem vendas. Ação: atender a cada 14 dias.

## regra_092.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_093.gobr

### Regra Padrao da Empresa Customizavel - Semanal para ativos adimplentes (time televendas)

Para clientes da carteira “carteira fixa time televendas”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender semanalmente (a cada 7 dias); dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel - 14 dias para ativos inadimplentes (time televendas)

Para clientes da carteira “carteira fixa time televendas”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel - 30 dias para inativos (time televendas)

Para clientes da carteira “carteira fixa time televendas”, considerar clientes inativos para o vendedor. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel - 30 dias pra clientes sem vendas (time televendas)

Para clientes da carteira “carteira fixa time televendas”, considerar clientes sem vendas. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel - semanal para ativos adimplentes (time campo capital)

Para clientes da carteira “carteira fixa time campo capital”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender semanalmente (a cada 7 dias); dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel - 14 dias para ativos inadimplentes (time campo capital)

Para clientes da carteira “carteira fixa time campo capital”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel - 30 dias para inativos (time campo capital)

Para clientes da carteira “carteira fixa time campo capital”, considerar clientes inativos para o vendedor. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel - 30 dias pra clientes sem vendas (time campo capital)

Para clientes da carteira “carteira fixa time campo capital”, considerar clientes sem vendas. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel - 14 dias para ativos (time campo interior)

Para clientes da carteira “carteira fixa time interior”, considerar clientes ativos para o vendedor. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel - 30 dias para inativos (time campo interior)

Para clientes da carteira “carteira fixa time interior”, considerar clientes inativos para o vendedor. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel - 30 dias pra clientes sem vendas (time campo interior)

Para clientes da carteira “carteira fixa time interior”, considerar clientes sem vendas. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

## regra_094.gobr

### Regra Padrao da AHL Customizavel: 30 dias para clientes adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes adimplentes. Ação: atender a cada 30 dias.

### Regra Padrao da AHL Customizavel: 60 dias para clientes inadimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inadimplentes. Ação: atender a cada 60 dias.

### Regra Padrao da AHL Customizavel: 30 dias para clientes sem venda (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes sem venda. Ação: atender a cada 30 dias.

### Regra Padrao da AHL Customizavel: 30 dias para todos os clientes (campo)

Aplicar a regra a clientes da carteira “carteira campo”. Ação: atender a cada 30 dias.

## regra_095.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_096.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_097.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_098.gobr

### Teste CCN 11: 1d para todos os clientes

Aplicar a regra a clientes vinculados ao time “todos”. Ação: atender a cada 1 dia.

## regra_099.gobr

### Regra Padrao da Elluc: 7 dias para clientes sem venda (televendas)

Para clientes vinculados ao time “time televendas”, considerar clientes sem vendas. Ação: atender a cada 7 dias.

### Regra Padrao da Elluc: 30 dias para ativos inadimplentes (televendas)

Para clientes vinculados ao time “time televendas”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 30 dias.

### Regra Padrao da Elluc: nao agendar inativos inadimplentes (televendas)

Para clientes vinculados ao time “time televendas”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Elluc: 7 dias para clientes adimplentes (televendas)

Para clientes vinculados ao time “time televendas”, considerar clientes adimplentes. Ação: atender a cada 7 dias.

### Regra Padrao da Elluc: 30 dias para clientes dos externos

Aplicar a regra a clientes vinculados ao time “time campo”. Ação: atender a cada 30 dias.

## regra_100.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_101.gobr

### Regra Padrao da Propec: Frequencia de 7 dias para clientes ativos (televendas)

Para clientes vinculados ao time “time televendas”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias.

### Regra Padrao da Propec: Frequencia de 30 dias para clientes inativos (televendas)

Para clientes vinculados ao time “time televendas”, considerar clientes inativos para o vendedor. Ação: atender a cada 30 dias.

### Regra Padrao da Propec: Frequencia de 7 dias para clientes sem venda (televendas)

Para clientes vinculados ao time “time televendas”, considerar clientes sem venda. Ação: atender a cada 7 dias.

### Regra Padrao da Propec: Frequencia de 7 dias para clientes ativos (regiao metropolitana)

Para clientes vinculados ao time “time capital”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias.

### Regra Padrao da Propec: Frequencia de 14 dias para clientes inativos adimplentes (regiao metropolitana)

Para clientes vinculados ao time “time capital”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Propec: Nao agendar clientes inativos inadimplentes (regiao metropolitana)

Para clientes vinculados ao time “time capital”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Propec: Frequencia de 14 dias para clientes sem venda (regiao metropolitana)

Para clientes vinculados ao time “time capital”, considerar clientes sem venda. Ação: atender a cada 14 dias.

### Regra Padrao da Propec: Frequencia de 14 dias para clientes ativos (interior)

Para clientes vinculados ao time “time interior”, considerar clientes ativos para o vendedor. Ação: atender a cada 14 dias.

### Regra Padrao da Propec: Frequencia de 30 dias para clientes inativos adimplentes (interior)

Para clientes vinculados ao time “time interior”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 30 dias.

### Regra Padrao da Propec: Nao agendar clientes inativos inadimplentes (interior)

Para clientes vinculados ao time “time interior”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Propec: Frequencia de 30 dias para clientes sem venda (interior)

Para clientes vinculados ao time “time interior”, considerar clientes sem venda. Ação: atender a cada 30 dias.

## regra_102.gobr

### Regra Padrao da Alianca Distribuidora - Customizavel: 30 dias para clientes inativos inadimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor e inadimplentes. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Alianca Distribuidora - Customizavel: 14 dias para clientes ativos ou adimplentes (televendas)

Aplicar a regra a clientes da carteira “carteira televendas”. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Alianca Distribuidora - Customizavel: 30 dias para todos os clientes (campo)

Aplicar a regra a clientes vinculados ao time “campo”. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

## regra_103.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_104.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_105.gobr

### Regra Padrao da Empresa Customizavel: semanal para ativos adimplentes

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender semanalmente (a cada 7 dias); dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel: 14 dias para ativos inadimplentes

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel: 14 dias para inativos adimplentes

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel: nao agendar inativos inadimpletes

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Empresa Customizavel: 14 dias para clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem vendas. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

## regra_106.gobr

### Regra Padrao da Empresa Customizavel: 10 dias para ativos adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 10 dias.

### Regra Padrao da Empresa Customizavel: 21 dias para ativos inadimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 21 dias.

### Regra Padrao da Empresa Customizavel: 14 dias para inativos adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Empresa Customizavel: 60 dias para inativos inadimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor e inadimplentes. Ação: atender a cada 60 dias.

### Regra Padrao da Empresa Customizavel: 30 dias para clientes sem venda (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes sem venda. Ação: atender a cada 30 dias.

### Regra Padrao da Empresa Customizavel: 30 dias para ativos adimplentes (campo)

Para clientes da carteira “carteira campo”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 30 dias.

### Regra Padrao da Empresa Customizavel: 14 dias para inativos adimplentes (campo)

Para clientes da carteira “carteira campo”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Empresa Customizavel: nao agendar inadimplentes (campo)

Para clientes da carteira “carteira campo”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Empresa Customizavel: 30 dias para clientes sem venda (campo)

Para clientes da carteira “carteira campo”, considerar clientes sem venda. Ação: atender a cada 30 dias.

## regra_107.gobr

### Regra Padrao da Empresa Customizavel: 15 dias para inativos

Para clientes da carteira “empresa higicop”, considerar clientes inativos para o vendedor. Ação: atender quinzenalmente (a cada 15 dias); usar a preferência de dias configurada pelo vendedor.

### Regra Padrao da Empresa Customizavel: 15 dias para ativos

Para clientes da carteira “empresa higicop”, considerar clientes ativos para o vendedor. Ação: atender quinzenalmente (a cada 15 dias); usar a preferência de dias configurada pelo vendedor.

### Regra Padrao da Empresa Customizavel: 15 dias para clientes sem vendas

Para clientes da carteira “empresa higicop”, considerar clientes sem vendas. Ação: atender quinzenalmente (a cada 15 dias).

## regra_108.gobr

### Diferpan: Não agendar inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Diferpan: Freq. de 7d para cliente que nunca tirou com o vendedor

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect para o vendedor. Ação: atender a cada 7 dias.

### Diferpan: Freq. de 21d para construtora que comprou uma unica vez com o vendedor

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com o vendedor e dos ramos de atividade ("37"). Ação: atender a cada 21 dias.

### Diferpan: Freq. de 7d para cliente que comprou uma unica vez com o vendedor

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com o vendedor. Ação: atender a cada 7 dias.

### Diferpan: Freq. de 7d para clientes com frequência histórica menor do que 11 dias

Para clientes vinculados ao time “televendas”, considerar clientes frequência histórica menor que 11 dias. Ação: atender a cada 7 dias.

### Diferpan: Freq. de 14d para construtora que comprou com o vendedor entre 60 dias e 89 dias

Para clientes vinculados ao time “televendas”, considerar clientes fora da recência de compra/positivação do vendedor entre 60 dias e 89 dias e dos ramos de atividade ("37"). Ação: atender a cada 14 dias.

### Diferpan: Freq. de 21d para construtora que comprou com o vendedor entre 11 dias e 59 dias

Para clientes vinculados ao time “televendas”, considerar clientes fora da recência de compra/positivação do vendedor entre 11 dias e 59 dias e dos ramos de atividade ("37"). Ação: atender a cada 21 dias.

### Diferpan: Freq. de 21d para clientes que comprou ultima vez com o vendedor a mais de 90 dias

Para clientes vinculados ao time “televendas”, considerar clientes no ciclo de vida inativo com o vendedor. Ação: atender a cada 21 dias.

### Diferpan: Freq. de 7d para clientes que comprou com o vendedor entre 11 dias e 89 dias

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação com o vendedor nos últimos 90 dias. Ação: atender a cada 7 dias.

### Diferpan: Freq. de 7d para demais clientes

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 7 dias.

## regra_109.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_110.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_111.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_112.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_113.gobr

### Regra Padrao da Magalhaes e Massote - Customizavel: 30 dias para clientes sem venda

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Magalhaes e Massote - Customizavel: 30 dias para clientes ativos adimplentes

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Magalhaes e Massote - Customizavel: 60 dias para clientes ativos inadimplentes

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 60 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Magalhaes e Massote - Customizavel: 60 dias para clientes inativos adimplentes

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 60 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Magalhaes e Massote - Customizavel: Nao agendar clientes inativos inadimplentes

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

## regra_114.gobr

### Regra Padrao da Jamile: 15 dias para todos os clientes

Aplicar a regra a clientes vinculados ao time “time jamile”. Ação: atender a cada 15 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra padrão da Jamile: Nao agendar clientes que compraram a menos de 30 dias

Para clientes vinculados ao time “time ruptura jamile”, considerar clientes com a última compra/positivação na empresa entre 0 e 30 dias atrás. Ação: não agendar esses clientes.

### Regra padrão da Jamile: Frequencia de 14 dias para clientes a 30 dias sem comprar

Aplicar a regra a clientes vinculados ao time “time ruptura jamile”. Ação: atender a cada 14 dias.

### Regra padrão da Elizangela: Nao agendar clientes que compraram a menos de 30 dias

Para clientes vinculados ao time “time ruptura elizangela”, considerar clientes com a última compra/positivação na empresa entre 0 e 30 dias atrás. Ação: não agendar esses clientes.

### Regra padrão da Elizangela: Nao agendar clientes bloqueados

Para clientes vinculados ao time “time ruptura elizangela”, considerar clientes bloqueados. Ação: não agendar esses clientes.

### Regra padrão da Elizangela: Frequencia de 14 dias para clientes a 30 dias sem comprar

Aplicar a regra a clientes vinculados ao time “time ruptura elizangela”. Ação: atender a cada 14 dias.

### Regra Padrao da Pet Nobre - Customizavel: Nao agendar inativos inadimplentes (interior)

Para clientes vinculados ao time “time interior”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Pet Nobre - Customizavel: 30 dias para clientes ativos ou adimplentes (interior)

Aplicar a regra a clientes vinculados ao time “time interior”. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Pet Nobre - Customizavel: Nao agendar inativos inadimplentes (capital)

Para clientes vinculados ao time “time capital”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Pet Nobre - Customizavel: 30 dias para clientes ativos inadimplentes (capital)

Para clientes vinculados ao time “time capital”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Empresa Customizavel: 14 dias para adimplentes (capital)

Aplicar a regra a clientes vinculados ao time “time capital”. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Pet Nobre: Quinzenal para clientes ativos (televendas)

Para clientes vinculados ao time “time televendas”, considerar clientes ativos para o vendedor. Ação: atender a cada 15 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Pet Nobre: Semanal para clientes inativos ou prospects (televendas)

Aplicar a regra a clientes vinculados ao time “time televendas”. Ação: atender a cada 7 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

## regra_115.gobr

### Regra Padrao da Frigoforte: 7 dias para atacado (televendas)

Aplicar a regra a clientes vinculados ao time “time atacado”. Ação: atender a cada 7 dias.

### Regra Padrao da Frigoforte: 2 dias para salmao (televendas)

Aplicar a regra a clientes vinculados ao time “time salmao”. Ação: atender a cada 2 dias.

## regra_116.gobr

### Não agendar filiais

Para clientes vinculados ao time “televendas”, “campo”, considerar clientes que são filiais. Ação: não agendar esses clientes.

### Freq. de 7d para todos os clientes (televendas)

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 7 dias; dar preferência de atendimento aos dias úteis e ao sábado; evitar choque/conflito de atendimento no time("campo").

### Freq. de 7d para Ativos Adimplentes (campo)

Para clientes vinculados ao time “campo”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 7 dias.

### Freq. de 14d para Ativos Inadimplentes (campo)

Para clientes vinculados ao time “campo”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 14 dias.

### Freq. de 30d para Inativos Adimplentes (campo)

Para clientes vinculados ao time “campo”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 30 dias.

### Freq. de 60d para Inativos Inadimplentes (campo)

Para clientes vinculados ao time “campo”, considerar clientes inativos para o vendedor e inadimplentes. Ação: atender a cada 60 dias.

### Freq. de 7d para sem vendas (campo)

Para clientes vinculados ao time “campo”, considerar clientes sem venda. Ação: atender a cada 7 dias.

## regra_117.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_118.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_119.gobr

### Regra padrão da Ultrax : Frequencia de 15 dias para clientes ativos adimplentes

Para clientes vinculados ao time “time televendas”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 15 dias.

### Regra padrão da Ultrax: Frequencia de 30 dias para clientes ativos inadimplentes

Para clientes vinculados ao time “time televendas”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 30 dias.

### Regra padrão da Ultrax: Frequencia de 7 dias para clientes inativos adimplentes

Para clientes vinculados ao time “time televendas”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 7 dias.

### Regra padrão da Ultrax: Não agendar clientes inativos inadimplentes

Para clientes vinculados ao time “time televendas”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra padrão da Ultrax: Frequencia de 15 dias para clientes sem compra

Para clientes vinculados ao time “time televendas”, considerar clientes sem vendas. Ação: atender a cada 15 dias.

## regra_120.gobr

### Regra Padrao da IdealPet: Nao agendar clientes de carteira propria para RCA 12

Aplicar a regra a clientes vinculados ao time “Yasmim”. Ação: não agendar esses clientes.

### Regra Padrao da IdealPet - Customizavel: 14 dias para clientes ativos (televendas)

Para clientes da carteira “televendas”, considerar clientes ativos para o vendedor. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da IdealPet - Customizavel: 30 dias para clientes inativos (televendas)

Para clientes da carteira “televendas”, considerar clientes inativos para o vendedor. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da IdealPet - Customizavel: 7 dias para clientes sem venda (televendas)

Para clientes da carteira “televendas”, considerar clientes sem venda. Ação: atender a cada 7 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da IdelPet - Customizavel: 20 dias para clientes ativos adimplentes (capital)

Para clientes da carteira “capital”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 20 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da IdelPet - Customizavel: 20 dias para clientes ativos inadimplentes (capital)

Para clientes da carteira “capital”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 20 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da IdelPet - Customizavel: 30 dias para clientes inativos adimplentes (capital)

Para clientes da carteira “capital”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da IdelPet - Customizavel: 14 dias para clientes sem venda (capital)

Para clientes da carteira “capital”, considerar clientes sem venda. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da IdelPet - Customizavel: 30 dias para clientes inativos inadimplentes (capital)

Para clientes da carteira “capital”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da IdealPet - Customizavel: 21 dias para clientes ativos (interior)

Para clientes da carteira “interior”, considerar clientes ativos para o vendedor. Ação: atender a cada 21 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da IdealPet - Customizavel: 21 dias para clientes inativos adimplentes (interior)

Para clientes da carteira “interior”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 21 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da IdealPet - Customizavel: 30 dias para clientes inativos inadimplentes (interior)

Para clientes da carteira “interior”, considerar clientes inativos para o vendedor e inadimplentes. Ação: atender a cada 42 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da IdealPet - Customizavel: 38 dias para clientes sem venda (interior)

Para clientes da carteira “interior”, considerar clientes sem venda. Ação: atender a cada 38 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da IdealPet - Customizavel: clientes inativos inadimplentes (interior)

Para clientes da carteira “interior”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

## regra_121.gobr

### Não agendar clientes baixados na receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Não agendar Filiais

Para clientes vinculados ao time “televendas”, considerar clientes que são filiais. Ação: não agendar esses clientes.

### Clientes que compraram apenas uma vez após período de inatividade

Para clientes vinculados ao time “televendas”, considerar clientes no ciclo de vida reativado com a empresa. Ação: atender a cada 3 dias.

### Clientes com apenas uma compra

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com a empresa. Ação: atender a cada 3 dias.

### Ativos recorrentes (com compra em 30 dias)

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: aplicar frequência do histórico ou no mínimo de 3 dias e no máximo de 21 dias.

### Ativos (com compra entre 30 e 60 dias)

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 60 dias. Ação: atender a cada 14 dias.

### Ativos (com compra entre 60 e 90 dias)

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 90 dias. Ação: atender a cada 21 dias.

### Ativos (com compra entre 90 e 120 dias)

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 120 dias. Ação: atender a cada 14 dias.

### Clientes que hoje não se enquadraram nas regras padrão

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 7 dias.

## regra_122.gobr

### Regra Padrao da Empresa Customizavel: Não agendar inadimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Empresa Customizavel: 14 dias para ativos adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 14 dias.

### Regra Padrao da Empresa Customizavel: 30 dias para inativos adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 30 dias.

### Regra Padrao da Empresa Customizavel: 14 dias para clientes sem vendas (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes sem vendas. Ação: atender a cada 14 dias.

## regra_123.gobr

### Regra Padrao do goVendas: Frequencia semanal para clientes ativos

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias.

### Regra Padrao do goVendas: Frequencia quinzenal para clientes inativos

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 15 dias.

### Regra Padrao do goVendas: Frequencia semanal para clientes ativos (saude)

Para clientes vinculados ao time “time saude televendas”, considerar clientes ativos para o vendedor e dos ramos de atividade ("1"). Ação: atender a cada 7 dias.

### Regra Padrao do goVendas: Frequencia quinzenal para clientes inativos (saude)

Para clientes vinculados ao time “time saude televendas”, considerar clientes dos ramos de atividade ("1"). Ação: atender a cada 15 dias.

### Regra Padrao do goVendas: Nao agendar ramo de atividade diferente de saude (saude)

Aplicar a regra a clientes vinculados ao time “time saude televendas”. Ação: não agendar esses clientes.

### Regra Padrao do goVendas: Frequencia de 7 dias para clientes ativos (campo)

Para clientes vinculados ao time “campo”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias; marcar a parametrização como fixa.

### Regra Padrao do goVendas: Frequencia de 14 dias para clientes inativos (campo)

Aplicar a regra a clientes vinculados ao time “campo”. Ação: atender a cada 15 dias; marcar a parametrização como fixa.

## regra_124.gobr

### Regra Padrao da Roda Viva: 30 dias para todos os clientes (time externo)

Aplicar a regra a clientes vinculados ao time “time campo”. Ação: atender a cada 30 dias.

### Regra Padrao da Roda Viva: 25 dias para clientes ativos (televendas)

Para clientes vinculados ao time “time televendas”, considerar clientes ativos para o vendedor. Ação: atender a cada 25 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira); evitar choque/conflito de atendimento no time("time campo").

### Regra Padrao da Roda Viva: 25 dias para clientes inativos adimplentes (televendas)

Para clientes vinculados ao time “time televendas”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 25 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira); evitar choque/conflito de atendimento no time("time campo").

### Regra Padrao da Roda Viva: 25 dias para clientes inativos inadimplentes (televendas)

Para clientes vinculados ao time “time televendas”, considerar clientes inativos para o vendedor e inadimplentes. Ação: atender a cada 25 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira); evitar choque/conflito de atendimento no time("time campo").

### Regra Padrao da Roda Viva: 25 dias para clientes sem vendas (televendas)

Para clientes vinculados ao time “time televendas”, considerar clientes sem vendas. Ação: atender a cada 25 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira); evitar choque/conflito de atendimento no time("time campo").

## regra_125.gobr

### Regra Padrao da Cavalo Marinho: 7 dias para clientes ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias.

### Regra Padrao da Cavalo Marinho: 15 dias para clientes inativos adimplentes

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 15 dias.

### Regra Padrao da Cavalo Marinho: nao agendar clientes inativos inadimplentes

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Cavalo Marinho: 20 dias para clientes prospects

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: atender a cada 20 dias.

## regra_126.gobr

### Regra Padrao da Femac: 14 dias para clientes com mais de 31 dias sem compra com a empresa (ruptura global)

Para clientes vinculados ao time “ruptura global”, considerar clientes inatividade global maior que 31 dias. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Femac: Não agendar cliente que compraram a menos de 31 dias (ruptura global)

Aplicar a regra a clientes vinculados ao time “ruptura global”. Ação: não agendar esses clientes.

### Regra Padrao da Femac: 14 dias para ativos adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Femac: 21 dias para ativos inadimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 21 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Femac: 30 dias para inativos adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Femac: Nao agendar inativos inadimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Femac: 30 dias para clientes sem venda (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes sem venda. Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Femac - Frequencia de 7 dias para clientes ativos (campo)

Para clientes da carteira “carteira campo”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias; marcar a parametrização como fixa.

### Regra Padrao da Femac - Frequencia de 15 dias para clientes inativos (campo)

Aplicar a regra a clientes da carteira “carteira campo”. Ação: atender a cada 15 dias; marcar a parametrização como fixa.

## regra_127.gobr

### Regra Padrao do goVendas Customizavel: Frequencia de inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa.

### Regra Padrao do goVendas Customizavel: Frequencia de clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem venda. Ação: usar a frequência média dos clientes inativos da empresa.

## regra_128.gobr

### Não agendar clientes baixados na receita

Para clientes vinculados ao time “tmk_1”, “tmk_2”, “tmk_3”, “tmk_5”, “tmk_6”, “tmk_7”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Prospects / Ext. Niteroi (283) e Rio 2 (279) para Tmk 1 (291)

Para clientes vinculados ao time “tmk_1”, considerar clientes contido na segmentacao("ext_niteroi_rio2_para_tmk1"); e com ciclo de vida Prospect na empresa. Ação: atender a cada 7 dias.

### Ativos (A partir do dia 20 de cada mês) / Ext. Niteroi (283) e Rio 2 (279) para Tmk 1 (291)

Para clientes vinculados ao time “tmk_1”, considerar clientes contido na segmentacao("ext_niteroi_rio2_para_tmk1"); e com a última compra/positivação na empresa nos últimos 60 dias. A parametrização é aplicada somente a partir do dia 16. Ação: atender a cada 5 dias.

### Retenção / Ext. Niteroi (283) e Rio 2 (279) para Tmk 1 (291)

Para clientes vinculados ao time “tmk_1”, considerar clientes contido na segmentacao("ext_niteroi_rio2_para_tmk1"); e com a última compra/positivação na empresa nos últimos 90 dias. Ação: atender a cada 7 dias.

### Recuperação / Ext. Niteroi (283) e Rio 2 (279) para Tmk 1 (291)

Para clientes vinculados ao time “tmk_1”, considerar clientes contido na segmentacao("ext_niteroi_rio2_para_tmk1"). Ação: atender a cada 7 dias.

### Prospects / Ext. Lagos (286) e Norte (284) para Tmk 2 (292)

Para clientes vinculados ao time “tmk_2”, considerar clientes contido na segmentacao("ext_lagos_norte_para_tmk2"); e com ciclo de vida Prospect na empresa. Ação: atender a cada 7 dias.

### Ativos (A partir do dia 20 de cada mês) / Ext. Lagos (286) e Norte (284) para Tmk 2 (292)

Para clientes vinculados ao time “tmk_2”, considerar clientes contido na segmentacao("ext_lagos_norte_para_tmk2"); e com a última compra/positivação na empresa nos últimos 60 dias. A parametrização é aplicada somente a partir do dia 16. Ação: atender a cada 5 dias.

### Retenção / Ext. Lagos (286) e Norte (284) para Tmk 2 (292)

Para clientes vinculados ao time “tmk_2”, considerar clientes contido na segmentacao("ext_lagos_norte_para_tmk2"); e com a última compra/positivação na empresa nos últimos 90 dias. Ação: atender a cada 7 dias.

### Recuperação / Ext. Lagos (286) e Norte (284) para Tmk 2 (292)

Para clientes vinculados ao time “tmk_2”, considerar clientes contido na segmentacao("ext_lagos_norte_para_tmk2"). Ação: atender a cada 7 dias.

### Prospects / Ext. Baixada 1 (275) e Baixada 3 (277) para Tmk 3 (294)

Para clientes vinculados ao time “tmk_3”, considerar clientes contido na segmentacao("ext_baixada1_baixada3_para_tmk3"); e com ciclo de vida Prospect na empresa. Ação: atender a cada 7 dias.

### Ativos (A partir do dia 20 de cada mês) / Ext. Baixada 1 (275) e Baixada 3 (277) para Tmk 3 (294)

Para clientes vinculados ao time “tmk_3”, considerar clientes contido na segmentacao("ext_baixada1_baixada3_para_tmk3"); e com a última compra/positivação na empresa nos últimos 60 dias. A parametrização é aplicada somente a partir do dia 16. Ação: atender a cada 5 dias.

### Retenção / Ext. Baixada 1 (275) e Baixada 3 (277) para Tmk 3 (294)

Para clientes vinculados ao time “tmk_3”, considerar clientes contido na segmentacao("ext_baixada1_baixada3_para_tmk3"); e com a última compra/positivação na empresa nos últimos 90 dias. Ação: atender a cada 7 dias.

### Recuperação / Ext. Baixada 1 (275) e Baixada 3 (277) para Tmk 3 (294)

Para clientes vinculados ao time “tmk_3”, considerar clientes contido na segmentacao("ext_baixada1_baixada3_para_tmk3"). Ação: atender a cada 7 dias.

### Prospects / Ext. Rio 1 (278) e Rio 3 (280) para Tmk 5 (375)

Para clientes vinculados ao time “tmk_5”, considerar clientes contido na segmentacao("ext_rio1_rio3_para_tmk5"); e com ciclo de vida Prospect na empresa. Ação: atender a cada 7 dias.

### Ativos (A partir do dia 20 de cada mês) / Ext. Rio 1 (278) e Rio 3 (280) para Tmk 5 (375)

Para clientes vinculados ao time “tmk_5”, considerar clientes contido na segmentacao("ext_rio1_rio3_para_tmk5"); e com a última compra/positivação na empresa nos últimos 60 dias. A parametrização é aplicada somente a partir do dia 16. Ação: atender a cada 5 dias.

### Retenção / Ext. Rio 1 (278) e Rio 3 (280) para Tmk 5 (375)

Para clientes vinculados ao time “tmk_5”, considerar clientes contido na segmentacao("ext_rio1_rio3_para_tmk5"); e com a última compra/positivação na empresa nos últimos 90 dias. Ação: atender a cada 7 dias.

### Recuperação / Ext. Rio 1 (278) e Rio 3 (280) para Tmk 5 (375)

Para clientes vinculados ao time “tmk_5”, considerar clientes contido na segmentacao("ext_rio1_rio3_para_tmk5"). Ação: atender a cada 7 dias.

### Prospects / Ext. Sul Flu 1 (273) e Sul Flu 2 (274) para Tmk 6 (900)

Para clientes vinculados ao time “tmk_6”, considerar clientes contido na segmentacao("ext_sulflu1_sulflu2_para_tmk6"); e com ciclo de vida Prospect na empresa. Ação: atender a cada 7 dias.

### Ativos (A partir do dia 20 de cada mês) / Ext. Sul Flu 1 (273) e Sul Flu 2 (274) para Tmk 6 (900)

Para clientes vinculados ao time “tmk_6”, considerar clientes contido na segmentacao("ext_sulflu1_sulflu2_para_tmk6"); e com a última compra/positivação na empresa nos últimos 60 dias. A parametrização é aplicada somente a partir do dia 16. Ação: atender a cada 5 dias.

### Retenção / Ext. Sul Flu 1 (273) e Sul Flu 2 (274) para Tmk 6 (900)

Para clientes vinculados ao time “tmk_6”, considerar clientes contido na segmentacao("ext_sulflu1_sulflu2_para_tmk6"); e com a última compra/positivação na empresa nos últimos 90 dias. Ação: atender a cada 7 dias.

### Recuperação / Ext. Sul Flu 1 (273) e Sul Flu 2 (274) para Tmk 6 (900)

Para clientes vinculados ao time “tmk_6”, considerar clientes contido na segmentacao("ext_sulflu1_sulflu2_para_tmk6"). Ação: atender a cada 7 dias.

### Prospects / Ext. Serrana (282) e Baixada 2 (276) para Tmk 7 (901)

Para clientes vinculados ao time “tmk_7”, considerar clientes contido na segmentacao("ext_serrana_baixada2_para_tmk7"); e com ciclo de vida Prospect na empresa. Ação: atender a cada 7 dias.

### Ativos (A partir do dia 20 de cada mês) / Ext. Serrana (282) e Baixada 2 (276) para Tmk 7 (901)

Para clientes vinculados ao time “tmk_7”, considerar clientes contido na segmentacao("ext_serrana_baixada2_para_tmk7"); e com a última compra/positivação na empresa nos últimos 60 dias. A parametrização é aplicada somente a partir do dia 16. Ação: atender a cada 5 dias.

### Retenção / Ext. Serrana (282) e Baixada 2 (276) para Tmk 7 (901)

Para clientes vinculados ao time “tmk_7”, considerar clientes contido na segmentacao("ext_serrana_baixada2_para_tmk7"); e com a última compra/positivação na empresa nos últimos 90 dias. Ação: atender a cada 7 dias.

### Recuperação / Ext. Serrana (282) e Baixada 2 (276) para Tmk 7 (901)

Para clientes vinculados ao time “tmk_7”, considerar clientes contido na segmentacao("ext_serrana_baixada2_para_tmk7"). Ação: atender a cada 7 dias.

### Prospects / Exclusivo do televendas

Para clientes vinculados ao time “tmk_1”, “tmk_2”, “tmk_3”, “tmk_5”, “tmk_6”, “tmk_7”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 7 dias.

### Ativos / Exclusivo do televendas

Para clientes vinculados ao time “tmk_1”, “tmk_2”, “tmk_3”, “tmk_5”, “tmk_6”, “tmk_7”, considerar clientes com a última compra/positivação na empresa nos últimos 60 dias. Ação: atender a cada 7 dias.

### Retenção / Exclusivo do televendas

Para clientes vinculados ao time “tmk_1”, “tmk_2”, “tmk_3”, “tmk_5”, “tmk_6”, “tmk_7”, considerar clientes com a última compra/positivação na empresa nos últimos 90 dias. Ação: atender a cada 7 dias.

### Recuperação / Exclusivo do televendas

Para clientes vinculados ao time “tmk_1”, “tmk_2”, “tmk_3”, “tmk_5”, “tmk_6”, “tmk_7”, considerar clientes nao contido na segmentacao( "ext_niteroi_rio2_para_tmk1","ext_lagos_norte_para_tmk2","ext_baixada1_baixada3_para_tmk3", "ext_rio1_rio3_para_tmk5","ext_sulflu1_sulflu2_para_tmk6","ext_serrana_baixada2_para_tmk7" ). Ação: atender a cada 7 dias.

### Clientes que hoje não se enquadraram nas regra solicitadas

Aplicar a regra a clientes vinculados ao time “tmk_1”, “tmk_2”, “tmk_3”, “tmk_5”, “tmk_6”, “tmk_7”. Ação: não agendar esses clientes.

## regra_129.gobr

### Boa Praça: Não agendar clientes inadimplentes

Para clientes vinculados ao time “todos”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Boa Praça: Não agendar clientes filial

Para clientes vinculados ao time “todos”, considerar clientes que são filiais. Ação: não agendar esses clientes.

### Boa Praça: Freq. de 7 dias para clientes ativos

Para clientes vinculados ao time “todos”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias.

### Boa Praça: Freq. de 14 dias para clientes inativos

Aplicar a regra a clientes vinculados ao time “todos”. Ação: atender a cada 14 dias.

## regra_130.gobr

### Regra Padrao da Macropac: Não agendar clientes CPF (Televendas)

Para clientes vinculados ao time “time interno”, considerar clientes pessoa física. Ação: não agendar esses clientes.

### Regra Padrao da Macropac: Frequencia de 7 dias para ativos (Televendas)

Para clientes vinculados ao time “time interno”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias.

### Regra Padrao da Macropac: Frequencia de 15 dias para inativos adimplentes (Televendas)

Para clientes vinculados ao time “time interno”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 15 dias.

### Regra Padrao da Macropac: Não agendar clientes inativos inadimplentes (Televendas)

Para clientes vinculados ao time “time interno”, considerar clientes inativos para o vendedor e inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Macropac: Não agendar clientes sem compra e CPF (Televendas)

Para clientes vinculados ao time “time interno”, considerar clientes sem vendas e pessoa fisica. Ação: não agendar esses clientes.

### Regra Padrao da Macropac: Frequencia de 20 dias para clientes sem compra e CNPJ (Televendas)

Para clientes vinculados ao time “time interno”, considerar clientes sem vendas e pessoa juridica. Ação: atender a cada 20 dias.

### Regra Padrao da Macropac: Frequencia de 7 dias para clientes ativos (campo)

Para clientes vinculados ao time “time externo”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias; marcar a parametrização como fixa.

### Regra Padrao da Macropac: Frequencia de 14 dias para clientes inativos (campo)

Aplicar a regra a clientes vinculados ao time “time externo”. Ação: atender a cada 15 dias; marcar a parametrização como fixa.

## regra_131.gobr

### Labtech: Não agendar inadimplentes

Para clientes vinculados ao time “time televendas”, “time campo”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Labtech: Não agendar 'Administração pública em geral' e 'Segurança e ordem pública'

Para clientes vinculados ao time “time televendas”, “time campo”, considerar clientes com CNAE ("8411600","8424800"). Ação: não agendar esses clientes.

### Labtech: Frequência de 7 dias para clientes sem crédito

Para clientes vinculados ao time “time televendas”, “time campo”, considerar clientes nao tem crédito. Ação: atender a cada 7 dias.

### Labtech: Frequência de 7 dias para clientes ativos - Modelo 1 - Televendas

Para clientes vinculados ao time “time televendas”, considerar clientes ativos para o vendedor e com CNAE ("8630501","8610101","8630502","7500100","8610102","8630503","8640201","8690901","8630501"). Ação: atender a cada 7 dias.

### Labtech: Frequência de 14 dias para clientes inativos - Modelo 1 - Televendas

Para clientes vinculados ao time “time televendas”, considerar clientes com CNAE ("8630501","8610101","8630502","7500100","8610102","8630503","8640201","8690901","8630501"). Ação: atender a cada 14 dias.

### Labtech: Frequência de 21 dias para clientes ativos - Modelo 2 - Televendas

Para clientes vinculados ao time “time televendas”, considerar clientes ativos para o vendedor e com CNAE ("8533300","8532500","4645101","3250705","4773300"). Ação: atender a cada 21 dias.

### Labtech: Frequência de 30 dias para clientes inativos - Modelo 2 - Televendas

Para clientes vinculados ao time “time televendas”, considerar clientes com CNAE ("8533300","8532500","4645101","3250705","4773300"). Ação: atender a cada 30 dias.

### Labtech: Frequência de 30 dias - Modelo 3 - Televendas

Aplicar a regra a clientes vinculados ao time “time televendas”. Ação: atender a cada 30 dias.

### Labtech: Frequência de 7 dias para clientes ativos - Modelo 1 - Externos

Para clientes vinculados ao time “time campo”, considerar clientes ativos para o vendedor e com CNAE ("8630501","8610101","8630502","7500100","8610102","8630503","8640201","8690901","8630501"). Ação: atender a cada 7 dias; definir preferência de atendimento na segunda e na quarta e na sexta.

### Labtech: Frequência de 14 dias para clientes inativos - Modelo 1 - Externos

Para clientes vinculados ao time “time campo”, considerar clientes com CNAE ("8630501","8610101","8630502","7500100","8610102","8630503","8640201","8690901","8630501"). Ação: atender a cada 14 dias; definir preferência de atendimento na segunda e na quarta e na sexta.

### Labtech: Frequência de 21 dias para clientes ativos - Modelo 2 - Externos

Para clientes vinculados ao time “time campo”, considerar clientes ativos para o vendedor e com CNAE ("8533300","8532500","4645101","3250705","4773300"). Ação: atender a cada 21 dias; definir preferência de atendimento na segunda e na quarta e na sexta.

### Labtech: Frequência de 30 dias para clientes inativos - Modelo 2 - Externos

Para clientes vinculados ao time “time campo”, considerar clientes com CNAE ("8533300","8532500","4645101","3250705","4773300"). Ação: atender a cada 30 dias; definir preferência de atendimento na segunda e na quarta e na sexta.

### Labtech: Frequência de 30 dias - Modelo 3 - Externos

Aplicar a regra a clientes vinculados ao time “time campo”. Ação: atender a cada 30 dias; definir preferência de atendimento na segunda e na quarta e na sexta.

## regra_132.gobr

### Não agendar 'Inadimplentes'

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Freq. de 7d para 'Prospect - Cliente potencial'

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect para o vendedor. Ação: atender a cada 7 dias.

### Freq. de 7d para 'Ativado - Fez um pedido e não comprou mais'

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com o vendedor. Ação: atender a cada 7 dias.

### Freq. de 14d para 'Ativo - Compra regularmente'

Para clientes vinculados ao time “televendas”, considerar clientes frequência histórica menor que 11 dias. Ação: atender a cada 14 dias.

### Freq. de 10d para 'Ativo - Estimular a regularidade de compra'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor entre 11 e 59 dias atrás. Ação: atender a cada 10 dias.

### Freq. de 7d para 'Em ruptura - Risco de ficar inativo'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor entre 60 e 89 dias atrás. Ação: atender a cada 7 dias.

### Freq. de 10d para 'Inativo - Reativar cliente sem compra'

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 10 dias.

## regra_133.gobr

### Regra Padrao da Casa Cardao: nao agendar inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Casa Cardao: 7 dias para clintes ativos

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias.

### Regra Padrao da Casa Cardao: 14 dias clintes inativos

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 14 dias.

### Regra Padrao da Casa Cardao - Frequencia 7 dias para clientes ativos (campo)

Para clientes da carteira “carteira campo”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias; marcar a parametrização como fixa.

### Regra Padrao da Casa Cardao - Frequencia de 15 dias para clientes inativos (campo)

Aplicar a regra a clientes da carteira “carteira campo”. Ação: atender a cada 15 dias; marcar a parametrização como fixa.

## regra_134.gobr

### Regra padrão da Linavet: Frequencia de 15 dias para todos os clientes

Aplicar a regra a clientes vinculados ao time “toda empresa”. Ação: atender a cada 15 dias.

## regra_135.gobr

### Prospects Segunda

Para clientes da carteira “segunda_feira_televendas_2”, considerar clientes com ciclo de vida Prospect para o vendedor. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na sexta.

### Alta Frequencia Segunda

Para clientes da carteira “segunda_feira_televendas_2”, considerar clientes com a última compra/positivação com o vendedor nos últimos 30 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na sexta.

### Regularidade Segunda

Para clientes da carteira “segunda_feira_televendas_2”, considerar clientes com a última compra/positivação com o vendedor nos últimos 45 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na sexta.

### Risco Inatividade Segunda

Para clientes da carteira “segunda_feira_televendas_2”, considerar clientes sem compra/positivação na empresa nos últimos 120 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na sexta.

### Inativos Segunda

Para clientes da carteira “segunda_feira_televendas_2”, considerar clientes sem compra/positivação nos últimos 180 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na sexta.

### Sem Regra Segunda

Aplicar a regra a clientes da carteira “segunda_feira_televendas_2”. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na sexta.

### Prospects Terca

Para clientes da carteira “terca_feira_televendas_2”, considerar clientes com ciclo de vida Prospect para o vendedor. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na segunda.

### Alta Frequencia Terca

Para clientes da carteira “terca_feira_televendas_2”, considerar clientes com a última compra/positivação com o vendedor nos últimos 30 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na segunda.

### Regularidade Terca

Para clientes da carteira “terca_feira_televendas_2”, considerar clientes com a última compra/positivação com o vendedor nos últimos 45 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na segunda.

### Risco Inatividade Terca

Para clientes da carteira “terca_feira_televendas_2”, considerar clientes sem compra/positivação na empresa nos últimos 120 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na segunda.

### Inativos Terca

Para clientes da carteira “terca_feira_televendas_2”, considerar clientes sem compra/positivação nos últimos 180 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na segunda.

### Sem Regra Terca

Aplicar a regra a clientes da carteira “terca_feira_televendas_2”. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na segunda.

### Prospects Quarta

Para clientes da carteira “quarta_feira_televendas_2”, considerar clientes com ciclo de vida Prospect para o vendedor. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na terça.

### Alta Frequencia Quarta

Para clientes da carteira “quarta_feira_televendas_2”, considerar clientes com a última compra/positivação com o vendedor nos últimos 30 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na terça.

### Regularidade Quarta

Para clientes da carteira “quarta_feira_televendas_2”, considerar clientes com a última compra/positivação com o vendedor nos últimos 45 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na terça.

### Risco Inatividade Quarta

Para clientes da carteira “quarta_feira_televendas_2”, considerar clientes sem compra/positivação na empresa nos últimos 120 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na terça.

### Inativos Quarta

Para clientes da carteira “quarta_feira_televendas_2”, considerar clientes sem compra/positivação nos últimos 180 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na terça.

### Sem Regra Quarta

Aplicar a regra a clientes da carteira “quarta_feira_televendas_2”. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na terça.

### Prospects Quinta

Para clientes da carteira “quinta_feira_televendas_2”, considerar clientes com ciclo de vida Prospect para o vendedor. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na quarta.

### Alta Frequencia Quinta

Para clientes da carteira “quinta_feira_televendas_2”, considerar clientes com a última compra/positivação com o vendedor nos últimos 30 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na quarta.

### Regularidade Quinta

Para clientes da carteira “quinta_feira_televendas_2”, considerar clientes com a última compra/positivação com o vendedor nos últimos 45 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na quarta.

### Risco Inatividade Quinta

Para clientes da carteira “quinta_feira_televendas_2”, considerar clientes sem compra/positivação na empresa nos últimos 120 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na quarta.

### Inativos Quinta

Para clientes da carteira “quinta_feira_televendas_2”, considerar clientes sem compra/positivação nos últimos 180 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na quarta.

### Sem Regra Quinta

Aplicar a regra a clientes da carteira “quinta_feira_televendas_2”. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na quarta.

### Prospects Sexta

Para clientes da carteira “sexta_feira_televendas_2”, considerar clientes com ciclo de vida Prospect para o vendedor. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na quinta.

### Alta Frequencia Sexta

Para clientes da carteira “sexta_feira_televendas_2”, considerar clientes com a última compra/positivação com o vendedor nos últimos 30 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na quinta.

### Regularidade Sexta

Para clientes da carteira “sexta_feira_televendas_2”, considerar clientes com a última compra/positivação com o vendedor nos últimos 45 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na quinta.

### Risco Inatividade Sexta

Para clientes da carteira “sexta_feira_televendas_2”, considerar clientes sem compra/positivação na empresa nos últimos 120 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na quinta.

### Inativos Sexta

Para clientes da carteira “sexta_feira_televendas_2”, considerar clientes sem compra/positivação nos últimos 180 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na quinta.

### Sem Regra Sexta

Aplicar a regra a clientes da carteira “sexta_feira_televendas_2”. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na quinta.

### Irrestrito: Clientes prospects

Para clientes da carteira “irrestrito_televendas_2”, considerar clientes com ciclo de vida Prospect para o vendedor. Ação: atender semanalmente (a cada 7 dias).

### Irrestrito: Clientes com Alta Freq. de compra

Para clientes da carteira “irrestrito_televendas_2”, considerar clientes com a última compra/positivação nos últimos 7 dias. Ação: atender a cada 7 dias.

### Irrestrito: Clientes que compram com regularidade

Para clientes da carteira “irrestrito_televendas_2”, considerar clientes com a última compra/positivação nos últimos 45 dias. Ação: atender a cada 14 dias.

### Irrestrito: Risco de ficar inativo curva A

Para clientes da carteira “irrestrito_televendas_2”, considerar clientes sem compra/positivação na empresa nos últimos 120 dias; e classificados na curva A com a empresa. Ação: atender a cada 14 dias.

### Irrestrito: Risco de ficar inativo curva B

Para clientes da carteira “irrestrito_televendas_2”, considerar clientes sem compra/positivação na empresa nos últimos 120 dias; e classificados na curva B com a empresa. Ação: atender a cada 30 dias.

### Irrestrito: Risco de ficar inativo curva C

Para clientes da carteira “irrestrito_televendas_2”, considerar clientes sem compra/positivação na empresa nos últimos 120 dias; e classificados na curva C com a empresa. Ação: atender a cada 30 dias.

### Irrestrito: Clientes inativos

Para clientes da carteira “irrestrito_televendas_2”, considerar clientes sem compra/positivação nos últimos 180 dias. Ação: atender a cada 21 dias.

### cidade SÃO JOSE DO RIO PRETO - 30 dias

Para clientes vinculados ao time “televendas_2”, considerar clientes localizados nas cidades ("SAO JOSE DO RIO PRETO"). Ação: atender a cada 30 dias.

### Irrestrito: sem regra mapeada

Aplicar a regra a clientes vinculados ao time “televendas_2”. Ação: atender a cada 30 dias.

### Freq. de 14d para Prospects

Para clientes vinculados ao time “televendas_1”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 14 dias.

### Ativos - recência 1 a 7 dias

Para clientes vinculados ao time “televendas_1”, considerar clientes com a última compra/positivação nos últimos 7 dias. Ação: atender a cada 21 dias.

### Ativos - recência 8 a 30 dias

Para clientes vinculados ao time “televendas_1”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: atender a cada 30 dias.

### Ativos - recência 31 a 60 dias

Para clientes vinculados ao time “televendas_1”, considerar clientes com a última compra/positivação nos últimos 60 dias. Ação: atender a cada 45 dias.

### Ativos - recência 61 a 90 dias

Para clientes vinculados ao time “televendas_1”, considerar clientes com a última compra/positivação nos últimos 90 dias. Ação: atender a cada 70 dias.

### Ativos - recência 91 a 180 dias

Para clientes vinculados ao time “televendas_1”, considerar clientes com a última compra/positivação nos últimos 180 dias. Ação: atender a cada 15 dias.

### Inativos - sem compra acima de 180 dias

Aplicar a regra a clientes vinculados ao time “televendas_1”. Ação: atender a cada 21 dias.

## regra_136.gobr

### Não agendar ramo de atividade 19 (Funcionários)

Para clientes vinculados ao time “empresa toda”, considerar clientes dos ramos de atividade ("19"). Ação: não agendar esses clientes.

### Regra Padrao da Multisul: 7 dias para ativos (Capital)

Para clientes da carteira “carteira capital”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias.

### Regra Padrao da Multisul: nao agendar clientes inativos (Capital)

Aplicar a regra a clientes da carteira “carteira capital”. Ação: não agendar esses clientes.

### Regra Padrao da Multisul: 14 dias para ativos (Interior)

Para clientes da carteira “carteira interior”, considerar clientes ativos para o vendedor. Ação: atender a cada 14 dias.

### Regra Padrao da Multisul: nao agendar clientes inativos (Interior)

Aplicar a regra a clientes da carteira “carteira interior”. Ação: não agendar esses clientes.

## regra_137.gobr

### Fênix distribuidora: 14d para prospects

Para clientes vinculados ao time “empresa toda”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 14 dias.

### Fênix distribuidora: 21d para ativos/adimplentes

Para clientes vinculados ao time “empresa toda”, considerar clientes ativos para o vendedor. Ação: atender a cada 21 dias.

### Fênix distribuidora: 14d para inativos/adimplentes

Aplicar a regra a clientes vinculados ao time “empresa toda”. Ação: atender a cada 14 dias.

## regra_138.gobr

### American Farma: Não agendar clientes inadimplentes (televendas)

Para clientes vinculados ao time “todos vendedores”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### American Farma: Freq. 7d para clientes ativos/inativos/prospects adimplentes (televendas)

Aplicar a regra a clientes vinculados ao time “todos vendedores”. Ação: atender a cada 7 dias.

## regra_139.gobr

### Não agendar Prospects

Para clientes vinculados ao time “farm_venda na base”, considerar clientes com ciclo de vida Prospect na empresa. Ação: não agendar esses clientes.

### Não agendar inadimplentes

Para clientes vinculados ao time “hunter_ativacao de novos”, “farm_venda na base”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Não agendar bloqueados

Para clientes vinculados ao time “hunter_ativacao de novos”, “farm_venda na base”, considerar clientes bloqueados. Ação: não agendar esses clientes.

### Freq. do histórico para 'Padrão de compra em até 30d'

Para clientes vinculados ao time “hunter_ativacao de novos”, considerar clientes frequência histórica menor que 31 dias. Ação: aplicar frequência do histórico ou no máximo de 30 dias.

### Freq. de 21d para 'Padrão de compra entre 30d e 90d'

Para clientes vinculados ao time “hunter_ativacao de novos”, considerar clientes frequência histórica entre 31 dias e 90 dias. Ação: atender a cada 21 dias.

### Freq. de 30d para 'Padrão de compra maior que 90d'

Aplicar a regra a clientes vinculados ao time “hunter_ativacao de novos”. Ação: atender a cada 30 dias.

### Freq. de 30d para 'Estimular regularidade de compra'

Para clientes vinculados ao time “farm_venda na base”, considerar clientes com a última compra/positivação com o vendedor entre 45 e 90 dias atrás. Ação: atender a cada 30 dias.

### Freq. de 25d para 'Risco de inatividade'

Para clientes vinculados ao time “farm_venda na base”, considerar clientes com a última compra/positivação com o vendedor entre 91 e 180 dias atrás. Ação: atender a cada 25 dias.

### Freq. de 21d para 'Resgate de cliente sem compra - Inativos'

Para clientes vinculados ao time “farm_venda na base”, considerar clientes inativos para o vendedor. Ação: atender a cada 21 dias.

### Freq. do histórico para 'Alta frequência de compra'

Para clientes vinculados ao time “farm_venda na base”, considerar clientes frequência histórica menor que 45 dias. Ação: aplicar frequência do histórico ou no mínimo de 40 dias e no máximo de 45 dias.

## regra_140.gobr

### Não agendar CPF

Para clientes vinculados ao time “televendas”, considerar clientes pessoa física. Ação: não agendar esses clientes.

### Não agendar Filiais

Para clientes vinculados ao time “televendas”, considerar clientes que são filiais. Ação: não agendar esses clientes.

### Não agendar Inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Não agendar com visita recente

Para clientes da carteira “rotas_dias_variaveis”, “rotas 3 e 4”, “rota 5”, “rota 6”, “rota 7”, considerar clientes recência de visita em 3 dias. Ação: não agendar esses clientes.

### Rotas 008, 009, 010 e 011 - Primeira compra

Para clientes da carteira “rotas_dias_variaveis”, considerar clientes sem venda do vendedor. Ação: atender semanalmente (a cada 7 dias).

### Rotas 008, 009, 010 e 011 - Compra regularmente

Para clientes da carteira “rotas_dias_variaveis”, considerar clientes com a última compra/positivação com o vendedor nos últimos 21 dias. Ação: atender semanalmente (a cada 7 dias).

### Rotas 008, 009, 010 e 011 - Estimular a regularidade de compra

Para clientes da carteira “rotas_dias_variaveis”, considerar clientes com a última compra/positivação entre 21 e 41 dias atrás. Ação: atender semanalmente (a cada 7 dias).

### Rotas 008, 009, 010 e 011 - Risco de inatividade

Para clientes da carteira “rotas_dias_variaveis”, considerar clientes com a última compra/positivação entre 41 e 90 dias atrás. Ação: atender semanalmente (a cada 7 dias).

### Rotas 008, 009, 010 e 011 - Cliente sem compra há mais de 90d

Para clientes da carteira “rotas_dias_variaveis”, considerar clientes sem compra/positivação nos últimos 90 dias. Ação: atender semanalmente (a cada 7 dias).

### Rotas 003 e 004 - Primeira compra

Para clientes da carteira “rotas 3 e 4”, considerar clientes sem venda do vendedor. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na segunda; marcar a parametrização como fixa.

### Rotas 003 e 004 - Compra regularmente

Para clientes da carteira “rotas 3 e 4”, considerar clientes com a última compra/positivação com o vendedor nos últimos 21 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na segunda; marcar a parametrização como fixa.

### Rotas 003 e 004 - Estimular a regularidade de compra

Para clientes da carteira “rotas 3 e 4”, considerar clientes com a última compra/positivação entre 21 e 41 dias atrás. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na segunda; marcar a parametrização como fixa.

### Rotas 003 e 004 - Risco de inatividade

Para clientes da carteira “rotas 3 e 4”, considerar clientes com a última compra/positivação entre 41 e 90 dias atrás. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na segunda; marcar a parametrização como fixa.

### Rotas 003 e 004 - Cliente sem compra há mais de 90d

Para clientes da carteira “rotas 3 e 4”, considerar clientes sem compra/positivação nos últimos 90 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na segunda; marcar a parametrização como fixa.

### Rota 005 - Primeira compra

Para clientes da carteira “rota 5”, considerar clientes sem venda do vendedor. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na terça; marcar a parametrização como fixa.

### Rota 005 - Compra regularmente

Para clientes da carteira “rota 5”, considerar clientes recência de compra/positivação do vendedor em 21 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na terça; marcar a parametrização como fixa.

### Rota 005 - Estimular a regularidade de compra

Para clientes da carteira “rota 5”, considerar clientes com a última compra/positivação entre 21 e 41 dias atrás. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na terça; marcar a parametrização como fixa.

### Rota 005 - Risco de inatividade

Para clientes da carteira “rota 5”, considerar clientes com a última compra/positivação entre 41 e 90 dias atrás. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na terça; marcar a parametrização como fixa.

### Rota 005 - Cliente sem compra há mais de 90d

Para clientes da carteira “rota 5”, considerar clientes sem compra/positivação nos últimos 90 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na terça; marcar a parametrização como fixa.

### Rota 006 - Primeira compra

Para clientes da carteira “rota 6”, considerar clientes sem venda do vendedor. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na quarta; marcar a parametrização como fixa.

### Rota 006 - Compra regularmente

Para clientes da carteira “rota 6”, considerar clientes com a última compra/positivação com o vendedor nos últimos 21 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na quarta; marcar a parametrização como fixa.

### Rota 006 - Estimular a regularidade de compra

Para clientes da carteira “rota 6”, considerar clientes com a última compra/positivação entre 21 e 41 dias atrás. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na quarta; marcar a parametrização como fixa.

### Rota 006 - Risco de inatividade

Para clientes da carteira “rota 6”, considerar clientes com a última compra/positivação entre 41 e 90 dias atrás. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na quarta; marcar a parametrização como fixa.

### Rota 006 - Cliente sem compra há mais de 90d

Para clientes da carteira “rota 6”, considerar clientes sem compra/positivação nos últimos 90 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na quarta; marcar a parametrização como fixa.

### Rota 007 - Primeira compra

Para clientes da carteira “rota 7”, considerar clientes sem venda do vendedor. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na sexta; marcar a parametrização como fixa.

### Rota 007 - Compra regularmente

Para clientes da carteira “rota 7”, considerar clientes com a última compra/positivação com o vendedor nos últimos 21 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na sexta; marcar a parametrização como fixa.

### Rota 007 - Estimular a regularidade de compra

Para clientes da carteira “rota 7”, considerar clientes com a última compra/positivação entre 21 e 41 dias atrás. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na sexta; marcar a parametrização como fixa.

### Rota 007 - Risco de inatividade

Para clientes da carteira “rota 7”, considerar clientes com a última compra/positivação entre 41 e 90 dias atrás. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na sexta; marcar a parametrização como fixa.

### Rota 007 - Cliente sem compra há mais de 90d

Para clientes da carteira “rota 7”, considerar clientes sem compra/positivação nos últimos 90 dias. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na sexta; marcar a parametrização como fixa.

### CLIENTES SEM ROTAS ASSOCIADAS

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender semanalmente (a cada 7 dias).

## regra_141.gobr

### Ever Limp: Frequência de 15 dias para clientes ativos curva A

Para clientes vinculados ao time “todos”, considerar clientes classificados na curva A com a empresa e ativos para o vendedor. Ação: atender a cada 15 dias.

### Ever Limp: Frequência de 7 dias para clientes inativos curva A

Para clientes vinculados ao time “todos”, considerar clientes classificados na curva A com a empresa. Ação: atender a cada 7 dias.

### Ever Limp: Frequência de 21 dias para clientes ativos curva B

Para clientes vinculados ao time “todos”, considerar clientes classificados na curva B com a empresa e ativos para o vendedor. Ação: atender a cada 21 dias.

### Ever Limp: Frequência de 14 dias para clientes inativos curva B

Para clientes vinculados ao time “todos”, considerar clientes classificados na curva B com a empresa. Ação: atender a cada 14 dias.

### Ever Limp: Frequência de 30 dias para clientes ativos curva C

Para clientes vinculados ao time “todos”, considerar clientes classificados na curva C com a empresa e ativos para o vendedor. Ação: atender a cada 30 dias.

### Ever Limp: Frequência de 21 dias para clientes inativos curva C

Para clientes vinculados ao time “todos”, considerar clientes classificados na curva C com a empresa. Ação: atender a cada 21 dias.

### Ever Limp: Frequência de 21 dias para prospects

Aplicar a regra a clientes vinculados ao time “todos”. Ação: atender a cada 21 dias.

## regra_142.gobr

### Dispomed: Frequência de 3 dias para clientes curva A (Yara)

Para clientes vinculados ao time “Yara”, considerar clientes classificados na curva A com a empresa. Ação: atender a cada 3 dias.

### Dispomed: Frequência de 7 dias para clientes curva B (Yara)

Para clientes vinculados ao time “Yara”, considerar clientes classificados na curva B com a empresa. Ação: atender a cada 7 dias.

### Dispomed: Frequência de 14 dias para clientes curva C (Yara)

Para clientes vinculados ao time “Yara”, considerar clientes classificados na curva C com a empresa. Ação: atender a cada 14 dias.

### Dispomed: Frequência de 14 dias para clientes sem classificação de curva (Yara)

Aplicar a regra a clientes vinculados ao time “Yara”. Ação: atender a cada 14 dias.

### Dispomed: Frequência de 2 dias para clientes curva A (Lúcia)

Para clientes vinculados ao time “Lúcia”, considerar clientes classificados na curva A com a empresa. Ação: atender a cada 2 dias.

### Dispomed: Frequência de 7 dias para clientes curva B (Lúcia)

Para clientes vinculados ao time “Lúcia”, considerar clientes classificados na curva B com a empresa. Ação: atender a cada 7 dias.

### Dispomed: Frequência de 14 dias para clientes curva C (Lúcia)

Para clientes vinculados ao time “Lúcia”, considerar clientes classificados na curva C com a empresa. Ação: atender a cada 14 dias.

### Dispomed: Frequência de 7 dias para clientes sem classificação de curva (Lúcia)

Aplicar a regra a clientes vinculados ao time “Lúcia”. Ação: atender a cada 7 dias.

### Dispomed: Frequência de 4 dias para clientes curva A (Wanderson)

Para clientes vinculados ao time “Wanderson”, considerar clientes classificados na curva A com a empresa. Ação: atender a cada 4 dias.

### Dispomed: Frequência de 7 dias para clientes curva B (Wanderson)

Para clientes vinculados ao time “Wanderson”, considerar clientes classificados na curva B com a empresa. Ação: atender a cada 7 dias.

### Dispomed: Frequência de 9 dias para clientes curva C (Wanderson)

Para clientes vinculados ao time “Wanderson”, considerar clientes classificados na curva C com a empresa. Ação: atender a cada 9 dias.

### Dispomed: Frequência de 14 dias para clientes sem classificação de curva (Wanderson)

Aplicar a regra a clientes vinculados ao time “Wanderson”. Ação: atender a cada 14 dias.

### Regra Padrão da Dispomed: Não liguar para inadimplente

Para clientes vinculados ao time “todos”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Regra Padrão da Dispomed: Frequência de 14 dias para Hospitais e Clínicas

Para clientes vinculados ao time “todos”, considerar clientes dos ramos de atividade ("001","002"). Ação: atender a cada 14 dias.

### Regra Padrão da Dispomed: Frequência de 7 dias para Distribuidora

Para clientes vinculados ao time “todos”, considerar clientes dos ramos de atividade ("003"). Ação: atender a cada 7 dias.

### Regra Padrão da Dispomed: Frequência de 21 dias para Farmácias

Para clientes vinculados ao time “todos”, considerar clientes dos ramos de atividade ("004"). Ação: atender a cada 21 dias.

### Regra Padrão da Dispomed: Não liguar para Fornecedor de uso e consumo, Orgão público e Representantes

Para clientes vinculados ao time “todos”, considerar clientes dos ramos de atividade ("005","006","100"). Ação: não agendar esses clientes.

### Regra Padrão da Dispomed: Frequência semanal para clientes ativos

Para clientes vinculados ao time “todos”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias.

### Regra Padrao do goVendas: Frequência quinzenal para clientes inativos

Aplicar a regra a clientes vinculados ao time “todos”. Ação: atender a cada 15 dias.

## regra_143.gobr

### Não agendar filiais

Para clientes vinculados ao time “televendas”, considerar clientes que são filiais. Ação: não agendar esses clientes.

### Não agendar clientes com compra em 30d

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa nos últimos 30 dias. Ação: não agendar esses clientes.

### Freq. de 28d para 'Prospects'

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 28 dias.

### Freq. de 7d para 'Ativos sem compra com a empresa há mais de 30d (Curva A)'

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Ativo na empresa; e cuja última compra/positivação na empresa está fora do intervalo de 30 a 45 dias atrás; e classificados na curva A com a empresa. Ação: atender a cada 7 dias.

### Freq. de 14d para 'Ativos sem compra com a empresa há mais de 30d (Curva B)'

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Ativo na empresa; e cuja última compra/positivação na empresa está fora do intervalo de 30 a 45 dias atrás; e classificados na curva B com a empresa. Ação: atender a cada 14 dias.

### Freq. de 21d para 'Ativos sem compra com a empresa há mais de 30d (Curva C)'

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Ativo na empresa; e cuja última compra/positivação na empresa está fora do intervalo de 30 a 45 dias atrás. Ação: atender a cada 21 dias.

### Freq. de 14d para 'Ativos sem compra com a empresa há mais de 45d'

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Ativo na empresa; e cuja última compra/positivação na empresa está fora do intervalo de 45 a 60 dias atrás. Ação: atender a cada 14 dias.

### Freq. de 7d para 'Ativos sem compra com a empresa há mais de 60d'

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Ativo na empresa. Ação: atender a cada 7 dias.

### Freq. de 7d para 'Inativos'

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 7 dias.

## regra_144.gobr

### Freq. de 14d para 'PROSPECT: FAZER O PRIMEIRO PEDIDO' (Todos)

Para clientes vinculados ao time “todos”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 14 dias.

### Freq. de 21d para 'INADIMPLENTES' (Todos)

Para clientes vinculados ao time “todos”, considerar clientes inadimplentes. Ação: atender a cada 21 dias.

### Freq. de 28d para 'BOAS VINDAS A CLIENTE COM O PRIMEIRO PEDIDO' (Todos)

Para clientes vinculados ao time “todos”, considerar clientes unica compra com a empresa; e cadastrados há 30 dias. Ação: atender a cada 28 dias.

### Freq. de 30d para 'COM COMPRA ENTRE 31 E 60 DIAS' (Todos)

Para clientes vinculados ao time “todos”, considerar clientes com a última compra/positivação entre 31 e 60 dias atrás. Ação: atender a cada 30 dias.

### Freq. de 10d para 'EM RUPTURA: RISCO DE INATIVIDADE' (Todos)

Para clientes vinculados ao time “todos”, considerar clientes com a última compra/positivação entre 61 e 90 dias atrás. Ação: atender a cada 10 dias.

### Freq. de 21d 'INATIVOS: RESGATE DE CLIENTES SEM COMPRA' (Todos)

Para clientes vinculados ao time “todos”, considerar clientes com ciclo de vida Inativo na empresa. Ação: atender a cada 21 dias.

### Freq. de 21d para 'ATIVO: COMPRA REGULARMENTE' (Fabricantes e Segmentos de Revendas/Manutenção)

Para clientes vinculados ao time “fabricantes”, “segmentos de revendas/manutencao”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: atender a cada 21 dias.

### Freq. de 28d para 'ATIVO: COMPRA REGULARMENTE' (Consumidor final recorrente, Compra exporádica e Consumidor final - Grande porte)

Para clientes vinculados ao time “consumidor final recorrente”, “compra exporadica”, “consumidor final - grande porte”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: atender a cada 28 dias.

## regra_145.gobr

### Não agendar Filiais

Para clientes vinculados ao time “empresa toda”, considerar clientes que são filiais. Ação: não agendar esses clientes.

### Freq. de 10d para 'Ativação de Prospects'

Para clientes vinculados ao time “empresa toda”, considerar clientes pessoa jurídica; e com ciclo de vida Prospect para o vendedor. Ação: atender a cada 10 dias.

### Freq. de 14d para 'Primeira compra' (Indústria)

Para clientes vinculados ao time “empresa toda”, considerar clientes pessoa jurídica; e sem venda do vendedor; e dos ramos de atividade ("2"). Ação: atender a cada 14 dias.

### Freq. de 7d para 'Primeira compra' (Revenda)

Para clientes vinculados ao time “empresa toda”, considerar clientes pessoa jurídica; e sem venda do vendedor; e dos ramos de atividade ("1"). Ação: atender a cada 7 dias.

### Freq. de 14d para 'Estimular a regularidade de compra'

Para clientes vinculados ao time “empresa toda”, considerar clientes pessoa jurídica; e adimplentes; e com a última compra/positivação com o vendedor entre 31 e 60 dias atrás. Ação: atender a cada 14 dias.

### Freq. de 21d para 'Compra regularmente'

Para clientes vinculados ao time “empresa toda”, considerar clientes pessoa jurídica; e adimplentes; e atividade do vendedor de 30 dias. Ação: atender a cada 21 dias.

### Freq. de 7d para 'Risco de inatividade'

Para clientes vinculados ao time “empresa toda”, considerar clientes pessoa jurídica; e adimplentes; e com a última compra/positivação com o vendedor entre 61 e 90 dias atrás. Ação: atender a cada 7 dias.

### Freq. de 21d para 'Resgate de clientes sem compra'

Para clientes vinculados ao time “empresa toda”, considerar clientes pessoa jurídica. Ação: atender a cada 21 dias.

## regra_146.gobr

### Não Agendar Inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Segmento: Saude

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("37","43","15"). Ação: atender a cada 7 dias.

### Segmento: FOOD

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("41","4","25"); e frequência histórica de 7 dias. Ação: atender a cada 7 dias.

### Cliente potencial

Para clientes vinculados ao time “televendas”, considerar clientes sem venda do vendedor. Ação: atender a cada 30 dias.

### Ativado: Fez um pedido e ainda não comprou mais

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com o vendedor; e com a última compra/positivação nos últimos 30 dias. Ação: atender a cada 30 dias.

### Ativo: compra regularmente

Para clientes vinculados ao time “televendas”, considerar clientes frequência histórica menor que 21 dias. Ação: atender a cada 21 dias.

### Em ruptura: risco de ficar inativo

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor entre 30 e 45 dias atrás. Ação: atender a cada 21 dias.

### Inativo: reativar cliente sem compra

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação com o vendedor nos últimos 46 dias. Ação: atender a cada 45 dias.

## regra_147.gobr

### HospDrogas: Frequência de 1 dia para clientes novos e sem atendimento (Time Carteira, PetVet e Portal)

Para clientes vinculados ao time “time carteira”, “time petvet”, “time portal”, considerar clientes cadastrado a partir do dia '2023-07-18'; e fora da recência de visita em 60 dias. Ação: atender a cada 1 dia.

### HospDrogas: Frequência de 7 dias para clientes novos (Time Carteira, PetVet e Portal)

Para clientes vinculados ao time “time carteira”, “time petvet”, “time portal”, considerar clientes cadastrado a partir do dia '2023-07-18'. Ação: atender a cada 7 dias.

### HospDrogas: Frequência de 5 dias para clientes ativos (Time Carteira, PetVet e Portal)

Para clientes vinculados ao time “time carteira”, “time petvet”, “time portal”, considerar clientes ativos para o vendedor. Ação: atender a cada 5 dias.

### HospDrogas: Frequência de 10 dias para clientes inativos (Time Carteira, PetVet e Portal)

Para clientes vinculados ao time “time carteira”, “time petvet”, “time portal”, considerar clientes inativos para o vendedor. Ação: atender a cada 10 dias.

### HospDrogas: Frequência de 20 dias para clientes sem venda (Time Carteira, PetVet e Portal)

Para clientes vinculados ao time “time carteira”, “time petvet”, “time portal”, considerar clientes sem venda. Ação: atender a cada 20 dias.

### HospDrogas: Frequência de 2 dias para clientes curva A (Time Distribuidor)

Para clientes vinculados ao time “time distribuidor”, considerar clientes curva A com o vendedor. Ação: atender a cada 2 dias.

### HospDrogas: Frequência de 4 dias para clientes curva B (Time Distribuidor)

Para clientes vinculados ao time “time distribuidor”, considerar clientes curva B com o vendedor. Ação: atender a cada 4 dias.

### HospDrogas: Frequência de 7 dias para clientes curva C (Time Distribuidor)

Para clientes vinculados ao time “time distribuidor”, considerar clientes curva C com o vendedor. Ação: atender a cada 7 dias.

### HospDrogas: Frequência de 15 dias para clientes sem classificação de curva ABC (Time Distribuidor)

Aplicar a regra a clientes vinculados ao time “time distribuidor”. Ação: atender a cada 15 dias.

### HospDrogas: Freq. de 7d para todos os clientes (Time Pré-venda)

Aplicar a regra a clientes vinculados ao time “pre-venda”. Ação: atender a cada 7 dias.

## regra_148.gobr

### Regra Padrao da Jumori: Não agendar inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Regra Padrao da Jumori: Frequencia semanal para clientes ativos

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor. Ação: atender semanalmente (a cada 7 dias).

### Regra Padrao da Jumori: Frequencia quinzenal para clientes inativos

Para clientes vinculados ao time “televendas”, considerar clientes inativos para o vendedor. Ação: atender quinzenalmente (a cada 15 dias).

### Regra Padrao da Jumori: Frequencia de 14 dias para clientes sem vendas

Para clientes vinculados ao time “televendas”, considerar clientes sem venda. Ação: atender quinzenalmente (a cada 15 dias).

## regra_149.gobr

### Ativos com compra em 7 dias

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 7 dias. Ação: não agendar esses clientes.

### Clientes Prospects

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Ativos com compra entre 7d e 30d

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Ativos com compra entre 30d e 60d

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 60 dias. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Ativos com compra entre 60d e 90d

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 90 dias. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Clientes inativos

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis e ao sábado.

## regra_150.gobr

### Não agendar clientes com compra da empresa nos últimos 45d

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa nos últimos 45 dias. Ação: não agendar esses clientes.

### Ative este cliente na sua carteira

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 28 dias.

### Cliente está caminhando para inatividade

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa entre 46 e 89 dias atrás. Ação: atender a cada 14 dias.

### Cliente inativo - Resgate este cliente

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 21 dias.

## regra_151.gobr

### Não agendar Ativos de campo com vendas em 60 dias

Para clientes da carteira “televendas fixa com ruptura de campo”, considerar clientes contido na segmentacao("cliente de ruptura"). A parametrização é aplicada somente na ultima semana. Ação: não agendar esses clientes.

## regra_152.gobr

### Nunca fez pedido com o vendedor (prospect)

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect para o vendedor. Ação: atender a cada 7 dias.

### Tirou o primeiro pedido com o vendedor

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com o vendedor. Ação: atender a cada 7 dias.

### Teve pedido entre 0 e 7 dias

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 7 dias. Ação: atender a cada 14 dias.

### Teve pedido entre 7 e 30 dias

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 7 e 30 dias atrás. Ação: atender a cada 14 dias.

### Teve pedido entre 30 e 60 dias

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 30 e 60 dias atrás. Ação: atender a cada 14 dias.

### Teve pedido entre 60 e 90 dias

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 60 e 90 dias atrás. Ação: atender a cada 7 dias.

### Teve pedido há 90 dias ou mais

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 7 dias.

## regra_153.gobr

### Não agendar clientes DH com crédito igual ou menor que R$0,00 (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes sem crédito disponível e tipo de cobranca igual("DH"). Ação: não agendar esses clientes.

### Não agendar clientes BK com crédito menor que R$200,00 (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes com menos de R$ 80 de credito disponivel e tipo de cobranca igual("BK"). Ação: não agendar esses clientes.

### Não agendar clientes inadimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Frequência de 7d para clientes ativos/adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias.

### Frequência de 14d para clientes inativos/adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor. Ação: atender a cada 14 dias.

### Frequência de 14d para clientes sem venda (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes sem venda. Ação: atender a cada 14 dias.

## regra_154.gobr

### Rota fixa de segunda-feira

Para clientes vinculados ao time “todos”, considerar clientes localizados nas cidades ("BALNEARIO BARRA DO S","BELA VISTA","CAMPO ALEGRE","CANOINHAS","CORUPA","ITAIOPOLIS","MAFRA","MAJOR VIEIRA","MONTE CASTELO", "PAPANDUVA","PORTO UNIAO","RIO NEGRINHO","SAO BENTO DO SUL","TRES BARRAS"). Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na segunda; marcar a parametrização como fixa.

### Rota fixa de terça-feira

Para clientes vinculados ao time “todos”, considerar clientes localizados nas cidades ("APIUNA","ASCURRA","BENEDITO NOVO","BLUMENAU","DOUTOR PEDRINHO","GASPAR","IBIRAMA","INDAIAL","POMERODE","PRESIDENTE GETULIO","RIO DOS CEDROS","TIMBO"). Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na terça; marcar a parametrização como fixa.

### Rota fixa de quarta-feira

Para clientes vinculados ao time “todos”, considerar clientes localizados nas cidades ("ARARANGUA","BIGUACU","BRACO DO NORTE","CAPIVARI DE BAIXO","COCAL DO SUL","CRICIUMA","FLORIANOPOLIS","FORQUILHINHA","GRAVATAL","ICARA", "IMBITUBA","JAGUARUMA","LAGUNA","LUIZ ALVES","MORRO DA FUMACA","ORLEANS","PALHOCA","PAULO LOPES","PEDRAS GRANDES","PESCARIA BRAVA", "PRAIA GRANDE","SANGAO","SANTA ROSA DO SUL","SAO JOAO DO SUL","SAO JOSE","SAO LUDGERO","SOMBRIO","TUBARAO","URUSSANGA"). Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na quarta; marcar a parametrização como fixa.

### Rota fixa de quinta-feira

Para clientes vinculados ao time “todos”, considerar clientes localizados nas cidades ("ARAQUARI","MASSARANDUBA","PIRABEIRABA","SAO JOAO DO ITAPERIU"). Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na quinta; marcar a parametrização como fixa.

### Rota dinâmica de segunda, terça ou sexta

Para clientes vinculados ao time “todos”, considerar clientes localizados nas cidades ("BRUSQUE"). Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na segunda e na terça e na sexta.

### Rota dinâmica para terça ou sexta

Para clientes vinculados ao time “todos”, considerar clientes localizados nas cidades ("NOVA TRENTO"). Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na terça e na sexta.

### Rota dinâmica de segunda ou quinta

Para clientes vinculados ao time “todos”, considerar clientes localizados nas cidades ("GUARAMIRIM","JARAGUA DO SUL","JOINVILLE","SCHROEDER"). Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na segunda e na quinta.

### Rota dinâmica de terça ou quinta

Para clientes vinculados ao time “todos”, considerar clientes localizados nas cidades ("BARRA VELHA","NAVEGANTES","PENHA","BALNEARIO PICARRAS"). Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na terça e na quinta.

### Rota dinâmica para dias variados

Para clientes vinculados ao time “todos”, considerar clientes localizados nas cidades ("BALNEARIO CAMBORIU","CAMBORIU","CANELINHA","ITAJAI","ITAPEMA","PORTO BELO","SAO JOAO BATISTA","TIJUCAS"). Ação: atender semanalmente (a cada 7 dias).

### Freq. de 30d para 'Prospects'

Para clientes vinculados ao time “todos”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 30 dias.

### Freq. de 14d para 'Ativos - Curva A'

Para clientes vinculados ao time “todos”, considerar clientes ativos para o vendedor; e classificados na curva A com a empresa. Ação: atender a cada 14 dias.

### Freq. de 21d para 'Ativos - Curva B'

Para clientes vinculados ao time “todos”, considerar clientes ativos para o vendedor; e classificados na curva B com a empresa. Ação: atender a cada 21 dias.

### Freq. de 28d para 'Ativos - Curva C'

Para clientes vinculados ao time “todos”, considerar clientes ativos para o vendedor. Ação: atender a cada 28 dias.

### Freq. de 30d para 'Inativos'

Aplicar a regra a clientes vinculados ao time “todos”. Ação: atender a cada 30 dias.

## regra_155.gobr

### Não agendar PF

Para clientes vinculados ao time “televendas”, considerar clientes pessoa física. Ação: não agendar esses clientes.

### Não agendar filiais

Para clientes vinculados ao time “televendas”, considerar clientes que são filiais. Ação: não agendar esses clientes.

### Não agendar baixadas na receita federal

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Não agendar Inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Não agendar clientes com compra em 30d

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: não agendar esses clientes.

### Ativação de um novo cliente em potencial - Conceito: Quando o cliente ainda não comprou com o vendedor

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa; e cadastrados há 30 dias. Ação: atender a cada 7 dias.

### Requalificar lead - Conceito: Requalificar o lead cadastrado na empresa que nunca tirou ou não tira orçamento há mais de 1 ano

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 21 dias.

### Boas vindas a um novo cliente ativado - Conceito: Quando o cliente tirou o primeiro orçamento com o vendedor

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com o vendedor. Ação: atender a cada 7 dias.

### Cliente com bom histórico de compra - Conceito: Quando o cliente tem alta recência de compra com a empresa (CURVA A)

Para clientes vinculados ao time “televendas”, considerar clientes cuja última compra/positivação na empresa está fora do intervalo de 30 a 45 dias atrás; e classificados na curva A com a empresa. Ação: atender a cada 14 dias.

### Cliente com bom histórico de compra - Conceito: Quando o cliente tem alta recência de compra com a empresa (CURVA B)

Para clientes vinculados ao time “televendas”, considerar clientes cuja última compra/positivação na empresa está fora do intervalo de 30 a 45 dias atrás; e classificados na curva B com a empresa. Ação: atender a cada 28 dias.

### Cliente com bom histórico de compra - Conceito: Quando o cliente tem alta recência de compra com a empresa (CURVA C)

Para clientes vinculados ao time “televendas”, considerar clientes cuja última compra/positivação na empresa está fora do intervalo de 30 a 45 dias atrás. Ação: atender a cada 45 dias.

### Estimular regularidade de compra - Conceito: Quando o cliente está há mais de 45 dias sem orçamento

Para clientes vinculados ao time “televendas”, considerar clientes cuja última compra/positivação na empresa está fora do intervalo de 46 a 60 dias atrás. Ação: atender a cada 28 dias.

### Atenção!!! Cliente com RISCO de ficar inativo - Conceito: Quando o cliente está há mais de 60 dias sem orçamento

Para clientes vinculados ao time “televendas”, considerar clientes cuja última compra/positivação na empresa está fora do intervalo de 61 a 90 dias atrás. Ação: atender a cada 21 dias.

### Atenção!!! Seu cliente corre RISCO de ativação por outro RCA - Conceito: Quando o cliente está há mais de 90 dias sem orçamento

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 14 dias.

## regra_156.gobr

### Tropical Color: Não agendar clientes inadimplentes

Para clientes vinculados ao time “todos”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Tropical Color: 14 dias para prospects

Para clientes vinculados ao time “todos”, considerar clientes com ciclo de vida Prospect para o vendedor. Ação: atender a cada 14 dias.

### Tropical Color: 10 dias para clientes com apenas 1 compra

Para clientes vinculados ao time “todos”, considerar clientes unica compra com o vendedor. Ação: atender a cada 10 dias.

### Tropical Color: 7 dias para adimplentes/ativos

Para clientes vinculados ao time “todos”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias.

### Tropical Color: 14 dias para adimplentes/inativos

Aplicar a regra a clientes vinculados ao time “todos”. Ação: atender a cada 14 dias.

## regra_157.gobr

### Regra Padrao da Lubrilages: Frequência de 14 dias para clientes com mais de 120 dias sem vendas

Para clientes vinculados ao time “toda empresa”, considerar clientes sem compra/positivação nos últimos 120 dias. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Lubrilages: Frequência de 7 dias para clientes com mais de 30 dias sem vendas

Para clientes vinculados ao time “toda empresa”, considerar clientes sem compra/positivação nos últimos 30 dias. Ação: atender a cada 7 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

### Regra Padrao da Lubrilages: mínimo de 5 dias e máximo de 30 dias

Aplicar a regra a clientes vinculados ao time “toda empresa”. Ação: aplicar frequência do histórico ou no mínimo de 5 dias e no máximo de 30 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

## regra_158.gobr

### Não agendar inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Não agendar Baixados na Receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Freq. de 30d para 'Prospect: Cliente potencial'

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 30 dias.

### Freq. de 21d para 'Ativado: fez um pedido e ainda não comprou mais'

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com a empresa; e com a última compra/positivação na empresa nos últimos 45 dias; e cadastrados há 120 dias. Ação: atender a cada 21 dias.

### Freq. de 14d para 'Ativo: Alta frequência de compra'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa nos últimos 45 dias; e frequência histórica menor que 30 dias. Ação: atender a cada 14 dias.

### Freq. de 30d para 'Ativo: compra regularmente'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa nos últimos 120 dias; e frequência histórica menor que 120 dias. Ação: atender a cada 30 dias.

### Freq. de 30d para 'Ativo: estimular a regularidade de compra'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa entre 45 e 70 dias atrás. Ação: atender a cada 30 dias.

### Freq. de 21d para 'Em ruptura: risco de ficar inativo'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa entre 71 e 120 dias atrás. Ação: atender a cada 21 dias.

### Freq. de 30d para 'Inativo: reativar cliente sem compra'

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação na empresa nos últimos 120 dias. Ação: atender a cada 30 dias.

## regra_159.gobr

### Brasgroup: 45d para clientes Curva C (Segmento Baby)

Para clientes vinculados ao time “baby”, considerar clientes total faturado no ano com a empresa menor que R$ 10000 ou indefinido. Ação: atender a cada 45 dias.

### Brasgroup: 15d para clientes Curva A (Segmento Baby)

Para clientes vinculados ao time “baby”, considerar clientes total faturado no ano com a empresa maior que R$ 30000. Ação: atender a cada 15 dias.

### Brasgroup: 30d para clientes Curva B (Segmento Baby)

Aplicar a regra a clientes vinculados ao time “baby”. Ação: atender a cada 30 dias.

### Brasgroup: 45d para clientes Curva C (Segmento Pet)

Para clientes vinculados ao time “pet”, considerar clientes total faturado no ano com a empresa menor que R$ 5000 ou indefinido. Ação: atender a cada 45 dias.

### Brasgroup: 15d para clientes Curva A (Segmento Pet)

Para clientes vinculados ao time “pet”, considerar clientes total faturado no ano com a empresa maior que R$ 20000. Ação: atender a cada 15 dias.

### Brasgroup: 30d para clientes Curva B (Segmento Pet)

Aplicar a regra a clientes vinculados ao time “pet”. Ação: atender a cada 30 dias.

### Regra Padrao do goVendas: Frequencia semanal para clientes ativos

Para clientes vinculados ao time “todos os vendedores”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias.

### Regra Padrao do goVendas: Frequencia quinzenal para clientes inativos

Aplicar a regra a clientes vinculados ao time “todos os vendedores”. Ação: atender a cada 15 dias.

## regra_160.gobr

### Fechamento de Rota e Sem Atendimento há 3 dias - Primeira Compra

Para clientes vinculados ao time “vendedores_ativos”, “vendedores_prospects”, considerar clientes pessoa jurídica; e data da rota nos proximos 1 dia; e sem venda do vendedor; e recência de visita entre 4 dias e 3000 dias. Ação: atender a cada 1 dia.

### Fechamento de Rota e Sem Atendimento há 3 dias - Estimular Regularidade de Compra

Para clientes vinculados ao time “vendedores_ativos”, “vendedores_prospects”, considerar clientes pessoa jurídica; e data da rota nos proximos 1 dia; e recência de visita entre 4 dias e 3000 dias; e com a última compra/positivação com o vendedor entre 31 e 60 dias atrás. Ação: atender a cada 1 dia.

### Fechamento de Rota e Sem Atendimento há 3 dias - Risco de inatividade

Para clientes vinculados ao time “vendedores_ativos”, “vendedores_prospects”, considerar clientes pessoa jurídica; e data da rota nos proximos 1 dia; e recência de visita entre 4 dias e 3000 dias; e com a última compra/positivação com o vendedor entre 61 e 90 dias atrás. Ação: atender a cada 1 dia.

### Fechamento de Rota e Sem Atendimento há 3 dias - Compra regularmente

Para clientes vinculados ao time “vendedores_ativos”, “vendedores_prospects”, considerar clientes pessoa jurídica; e data da rota nos proximos 1 dia; e recência de visita entre 4 dias e 3000 dias; e atividade do vendedor de 30 dias. Ação: atender a cada 1 dia.

### Fechamento de Rota e Sem Atendimento há 3 dias - Resgate de cliente sem compra

Para clientes vinculados ao time “vendedores_ativos”, “vendedores_prospects”, considerar clientes pessoa jurídica; e data da rota nos proximos 1 dia; e recência de visita entre 4 dias e 3000 dias; e inativos para o vendedor. Ação: atender a cada 1 dia.

### Fechamento de Rota e Sem Atendimento há 3 dias

Para clientes vinculados ao time “vendedores_ativos”, “vendedores_prospects”, considerar clientes pessoa jurídica; e data da rota nos proximos 1 dia; e recência de visita entre 4 dias e 3000 dias. Ação: atender a cada 1 dia.

### Primeira Compra (Vendedores Prospects)

Para clientes vinculados ao time “vendedores_prospects”, considerar clientes pessoa jurídica; e sem venda do vendedor. Ação: atender a cada 7 dias.

### Primeira Compra (Vendedores Ativos)

Para clientes vinculados ao time “vendedores_ativos”, considerar clientes pessoa jurídica; e sem venda do vendedor. Ação: atender a cada 14 dias.

### Risco de inatividade

Para clientes vinculados ao time “vendedores_ativos”, “vendedores_prospects”, considerar clientes pessoa jurídica; e com a última compra/positivação com o vendedor entre 61 e 90 dias atrás. Ação: atender a cada 7 dias.

### Estimular a regularidade de compra

Para clientes vinculados ao time “vendedores_ativos”, “vendedores_prospects”, considerar clientes pessoa jurídica; e com a última compra/positivação com o vendedor entre 31 e 60 dias atrás. Ação: atender a cada 14 dias.

### Compra regularmente

Para clientes vinculados ao time “vendedores_ativos”, “vendedores_prospects”, considerar clientes pessoa jurídica; e atividade do vendedor de 30 dias. Ação: atender a cada 14 dias.

### Resgate de cliente sem compra

Para clientes vinculados ao time “vendedores_ativos”, “vendedores_prospects”, considerar clientes pessoa jurídica; e inativos para o vendedor. Ação: atender a cada 21 dias.

### Pessoa Física

Para clientes vinculados ao time “vendedores_ativos”, “vendedores_prospects”, considerar clientes pessoa física. Ação: atender a cada 14 dias.

### Pessoa Física/Jurídica (indefinido)

Aplicar a regra a clientes vinculados ao time “vendedores_ativos”, “vendedores_prospects”. Ação: atender a cada 14 dias.

## regra_161.gobr

### Freq. de 15d para 'Ativos Curva A'

Para clientes vinculados ao time “todos”, considerar clientes ativos para o vendedor; e classificados na curva A com a empresa. Ação: atender a cada 15 dias.

### Freq. de 7d para 'Ativos Curva B'

Para clientes vinculados ao time “todos”, considerar clientes ativos para o vendedor; e classificados na curva B com a empresa. Ação: atender a cada 7 dias.

### Freq. de 15d para 'Ativos Curva C'

Para clientes vinculados ao time “todos”, considerar clientes ativos para o vendedor; e classificados na curva C com a empresa. Ação: atender a cada 15 dias.

### Freq. de 7d para 'Inativos'

Aplicar a regra a clientes vinculados ao time “todos”. Ação: atender a cada 7 dias.

## regra_162.gobr

### Não agendar 'CPF'

Para clientes vinculados ao time “televendas”, considerar clientes pessoa física. Ação: não agendar esses clientes.

### Não agendar 'Inadimplentes'

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Freq. de 14d para 'Sem histórico de compra'

Para clientes vinculados ao time “televendas”, considerar clientes prospect. Ação: atender a cada 14 dias.

### Freq. de 14d para 'Inativos'

Para clientes vinculados ao time “televendas”, considerar clientes inativos para o vendedor. Ação: atender a cada 14 dias.

### Freq. de 30d para 'Mais de 45d sem compra'

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação nos últimos 45 dias. Ação: atender a cada 30 dias.

### Freq. do histórico ou no mínimo de 14 dias e no máximo de 45 dias

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: aplicar frequência do histórico ou no mínimo de 14 dias e no máximo de 45 dias.

## regra_163.gobr

### Não agendar clientes com venda em 30d (Construtoras)

Para clientes da carteira “construtora”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: não agendar esses clientes.

### Ative um novo cliente em sua carteira (Construtoras)

Para clientes da carteira “construtora”, considerar clientes sem venda do vendedor. Ação: atender a cada 30 dias.

### Estabeleça relacionamento com seu novo cliente (Construtoras)

Para clientes da carteira “construtora”, considerar clientes unica compra com o vendedor; e sem compra/positivação nos últimos 60 dias. Ação: atender a cada 21 dias.

### Estimule a regularidade de compra do seu cliente (Construtoras)

Para clientes da carteira “construtora”, considerar clientes cuja última compra/positivação com o vendedor está fora do intervalo de 31 a 60 dias atrás. Ação: atender a cada 28 dias.

### Cliente entrando em ruptura (Construtoras)

Para clientes da carteira “construtora”, considerar clientes cuja última compra/positivação com o vendedor está fora do intervalo de 61 a 90 dias atrás. Ação: atender a cada 14 dias.

### Garanta que este cliente se mantenha ativo, pois ele está perdendo relacionamento com você! (Construtoras)

Aplicar a regra a clientes da carteira “construtora”. Ação: atender a cada 21 dias.

### Ative um novo cliente em sua carteira (Matcom)

Para clientes da carteira “matcom”, considerar clientes sem venda do vendedor. Ação: atender a cada 7 dias.

### Estabeleça relacionamento com seu novo cliente (Matcom)

Para clientes da carteira “matcom”, considerar clientes unica compra com o vendedor; e sem compra/positivação nos últimos 30 dias. Ação: atender a cada 14 dias.

### Cliente que compra com regularidade (Matcom)

Para clientes da carteira “matcom”, considerar clientes com a última compra/positivação entre 7 e 30 dias atrás. Ação: aplicar frequência do histórico ou no mínimo de 7 dias e no máximo de 30 dias.

### Estimule a regularidade de compra do seu cliente (Matcom)

Para clientes da carteira “matcom”, considerar clientes cuja última compra/positivação com o vendedor está fora do intervalo de 31 a 60 dias atrás. Ação: atender a cada 14 dias.

### Cliente entrando em ruptura (Matcom)

Para clientes da carteira “matcom”, considerar clientes cuja última compra/positivação com o vendedor está fora do intervalo de 61 a 90 dias atrás. Ação: atender a cada 7 dias.

### Garanta que este cliente se mantenha ativo, pois ele está perdendo relacionamento com você! (Matcom)

Aplicar a regra a clientes da carteira “matcom”. Ação: atender a cada 7 dias.

## regra_164.gobr

### Freq. 14 dias para novos cadastros 'Condomínio' vendedora Bruna

Para clientes vinculados ao time “time bruna”, considerar clientes cujo rótulo contém ("condominio"); e cadastrado a partir do dia '2024-10-03'. Ação: atender a cada 14 dias.

### Freq. de 7 dias para compra detectada com a empresa entre 0 e 30 dias 'Condomínio' vendedora Bruna

Para clientes vinculados ao time “time bruna”, considerar clientes cujo rótulo contém ("condominio"); e com a última compra/positivação na empresa nos últimos 30 dias. Ação: atender a cada 7 dias.

### Freq. de 30 dias para não tem compra com a empresa nos últimos 90 dias 'Condomínio' vendedora Bruna

Para clientes vinculados ao time “time bruna”, considerar clientes cujo rótulo contém ("condominio"); e sem compra/positivação na empresa nos últimos 90 dias. Ação: atender a cada 30 dias.

### Freq. de 7d para: 'Ativar prospects'

Para clientes vinculados ao time “time todos”, considerar clientes sem venda; e cadastrado a partir do dia '2024-08-01'. Ação: atender a cada 7 dias.

### Boas vindas: Frequência de 14d para construtora

Para clientes vinculados ao time “time todos”, considerar clientes cujo rótulo contém ("construtora"); e unica compra com a empresa; e sem compra/positivação nos últimos 60 dias. Ação: atender a cada 14 dias.

### Compra com regularidade no RJ - Curva A: Frequência de 7d para construtora

Para clientes vinculados ao time “time todos”, considerar clientes cujo rótulo contém ("construtora"); e frequência histórica menor que 30 dias; e sem compra/positivação nos últimos 14 dias; e localizados nos estados/UF ("RJ"); e classificados na curva A com a empresa. Ação: atender a cada 7 dias.

### Compra com regularidade no RJ - Curva B: Frequência de 10d para construtora

Para clientes vinculados ao time “time todos”, considerar clientes cujo rótulo contém ("construtora"); e frequência histórica menor que 30 dias; e sem compra/positivação nos últimos 14 dias; e localizados nos estados/UF ("RJ"); e classificados na curva B com a empresa. Ação: atender a cada 10 dias.

### Compra com regularidade no RJ - Curva C: Frequência de 14d para construtora

Para clientes vinculados ao time “time todos”, considerar clientes cujo rótulo contém ("construtora"); e frequência histórica menor que 30 dias; e sem compra/positivação nos últimos 14 dias; e localizados nos estados/UF ("RJ"); e classificados na curva C com a empresa. Ação: atender a cada 14 dias.

### Compra com regularidade: Frequência de 14d para construtora

Para clientes vinculados ao time “time todos”, considerar clientes cujo rótulo contém ("construtora"); e frequência histórica menor que 30 dias; e sem compra/positivação nos últimos 14 dias. Ação: atender a cada 14 dias.

### Estimular regularidade: Frequência de 10d para construtora

Para clientes vinculados ao time “time todos”, considerar clientes cujo rótulo contém ("construtora"); e com ciclo de vida Ativo na empresa; e sem compra/positivação na empresa nos últimos 45 dias. Ação: atender a cada 10 dias.

### Risco de ficar inativo: Frequência de 14d para construtora

Para clientes vinculados ao time “time todos”, considerar clientes cujo rótulo contém ("construtora"); e sem compra/positivação nos últimos 60 dias. Ação: atender a cada 14 dias.

### Ativar novos clientes: Frequência de 7d para construtora

Para clientes vinculados ao time “time todos”, considerar clientes cujo rótulo contém ("construtora"); e cadastrado a partir do dia '2024-10-03'. Ação: atender a cada 7 dias.

### Resgate de inativos: Frequência de 45d para construtora

Para clientes vinculados ao time “time todos”, considerar clientes cujo rótulo contém ("construtora"). Ação: atender a cada 45 dias.

### Freq. de 14 dias para Novos cadastros shopping, supermercado, industria, estaleiro, clube, escolas, universidade, igreja, hotel, hospital, clínica, restaurantes, condominio

Para clientes vinculados ao time “time todos”, considerar clientes cujo rótulo contém ("shopping", "supermercado", "industria", "estaleiro", "clube","escolas", "universidade", "igreja", "hotel", "hospital", "clinica", "restaurantes", "condominio"); e cadastrado a partir do dia '2024-10-03'. Ação: atender a cada 14 dias.

### Freq. de 7 dias para Novos cadastros shopping, supermercado, industria, estaleiro, clube, escolas, universidade, igreja, hotel, hospital, clínica, restaurantes, condominio

Para clientes vinculados ao time “time todos”, considerar clientes cujo rótulo contém ("shopping", "supermercado", "industria", "estaleiro", "clube","escolas", "universidade", "igreja", "hotel", "hospital", "clinica", "restaurantes", "condominio"); e com a última compra/positivação na empresa nos últimos 30 dias. Ação: atender a cada 7 dias.

### Freq. de 30 dias para Novos cadastros shopping, supermercado, industria, estaleiro, clube, escolas, universidade, igreja, hotel, hospital, clínica, restaurantes, condominio

Para clientes vinculados ao time “time todos”, considerar clientes cujo rótulo contém ("shopping", "supermercado", "industria", "estaleiro", "clube","escolas", "universidade", "igreja", "hotel", "hospital", "clinica", "restaurantes", "condominio"); e com a última compra/positivação na empresa nos últimos 30 dias. Ação: atender a cada 30 dias.

### Isocom: Não agendar - cliente não coberto por regra comercial

Aplicar a regra a clientes vinculados ao time “time todos”. Ação: não agendar esses clientes.

## regra_165.gobr

### Não agendar clientes inativos inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Inativo na empresa; e inadimplentes. Ação: não agendar esses clientes.

### Clientes há mais de 90 dias sem compra

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação nos últimos 90 dias. Ação: atender a cada 7 dias.

### Clientes com frequência histórica de pedidos entre 1 e 7 dias, e sem compra entre 8 e 15 dias.

Para clientes vinculados ao time “televendas”, considerar clientes contido na segmentacao("freq_hist_1a7"); e cuja última compra/positivação está fora do intervalo de 8 a 15 dias atrás. Ação: atender a cada 14 dias.

### Clientes com frequência histórica de pedidos entre 16 e 30 dias, e sem compra entre 31 e 45 dias.

Para clientes vinculados ao time “televendas”, considerar clientes contido na segmentacao("freq_hist_16a30"); e cuja última compra/positivação está fora do intervalo de 31 a 45 dias atrás. Ação: atender a cada 28 dias.

### Clientes com frequência histórica de pedidos entre 31 e 45 dias, e sem compra entre 46 e 60 dias.

Para clientes vinculados ao time “televendas”, considerar clientes contido na segmentacao("freq_hist_31a45"); e cuja última compra/positivação está fora do intervalo de 46 a 60 dias atrás. Ação: atender a cada 21 dias.

### Clientes com frequência histórica de pedidos entre 61 e 90 dias, e sem compra há 90 dias.

Para clientes vinculados ao time “televendas”, considerar clientes contido na segmentacao("freq_hist_61a90"); e sem compra/positivação nos últimos 90 dias. Ação: atender a cada 15 dias.

### Não agendar clientes que não se enquadrem em nenhuma regra padrão

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: não agendar esses clientes.

## regra_166.gobr

### Nordil PB: Não agendar clientes DH com crédito igual ou menor que R$0,00 (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes sem crédito disponível e tipo de cobranca igual("DH"). Ação: não agendar esses clientes.

### Nordil PB: Não agendar clientes BK com crédito menor que R$200,00 (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes com menos de R$ 199 de credito disponivel e tipo de cobranca igual("BK"). Ação: não agendar esses clientes.

### Nordil PB: Não agendar clientes inadimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Nordil PB: Frequência de 7d para clientes ativos/adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias.

### Nordil PB: Frequência de 14d para clientes inativos/adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor. Ação: atender a cada 14 dias.

### Nordil PB: Frequência de 14d para clientes sem venda (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes sem venda. Ação: atender a cada 14 dias.

## regra_167.gobr

### Não agendar baixados na receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Primeira compra

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 7 dias.

### Tirou o primeiro pedido

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com a empresa. Ação: atender a cada 15 dias.

### Ativo: cliente que tem compra com a empresa em 30 dias

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: aplicar frequência do histórico ou no mínimo de 7 dias e no máximo de 21 dias.

### Aumentar a regularidade de compra

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 31 e 90 dias atrás. Ação: atender a cada 28 dias.

### Cliente caminhando para inatividade

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 91 e 120 dias atrás. Ação: atender a cada 45 dias.

### Resgate de inativos

Para clientes vinculados ao time “televendas”, considerar clientes nao tem venda da empresa em 120 dias. Ação: atender a cada 60 dias.

## regra_168.gobr

### Não agendar baixados na Receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Não agendar bloqueados

Para clientes vinculados ao time “televendas”, considerar clientes bloqueados. Ação: não agendar esses clientes.

### Rota todo dia -> Agendamento todo dia

Aplicar a regra a clientes da carteira “rota_todo_dia”. Ação: atender diariamente (a cada 1 dia); definir preferência de atendimento maior na segunda e maior na terça e maior na quarta e maior na quinta e maior na sexta; marcar os clientes como roteirizáveis; marcar a parametrização como fixa.

### Rota de terça -> Agendamento segunda

Aplicar a regra a clientes da carteira “rota_terca”. A parametrização é aplicada somente na segunda. Ação: atender diariamente (a cada 1 dia); definir preferência de atendimento maior na segunda; marcar os clientes como roteirizáveis; marcar a parametrização como fixa.

### Rota de quarta -> Agendamento terça

Aplicar a regra a clientes da carteira “rota_quarta”. A parametrização é aplicada somente na terça. Ação: atender diariamente (a cada 1 dia); definir preferência de atendimento maior na terça; marcar os clientes como roteirizáveis; marcar a parametrização como fixa.

### Rota de quinta -> Agendamento quarta

Aplicar a regra a clientes da carteira “rota_quinta”. A parametrização é aplicada somente na quarta. Ação: atender diariamente (a cada 1 dia); definir preferência de atendimento maior na quarta; marcar os clientes como roteirizáveis; marcar a parametrização como fixa.

### Rota de sexta -> Agendamento quinta

Aplicar a regra a clientes da carteira “rota_sexta”. A parametrização é aplicada somente na quinta. Ação: atender diariamente (a cada 1 dia); definir preferência de atendimento maior na quinta; marcar os clientes como roteirizáveis; marcar a parametrização como fixa.

### Não agendar clientes que não se enquadraram nas regras hoje

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: não agendar esses clientes.

## regra_169.gobr

### Clientes Prospects

Para clientes da segmentação “televendas ruptura de fornecedor”, considerar clientes da carteira("televendas consumidor"); e com ciclo de vida Prospect na empresa. Ação: atender a cada 14 dias.

### Ativos com compra entre 7d e 30d

Para clientes da segmentação “televendas ruptura de fornecedor”, considerar clientes da carteira("televendas consumidor"); e com a última compra/positivação na empresa nos últimos 30 dias. Ação: atender a cada 14 dias.

### Ativos com compra entre 30d e 60d

Para clientes da segmentação “televendas ruptura de fornecedor”, considerar clientes da carteira("televendas consumidor"); e com a última compra/positivação na empresa nos últimos 60 dias. Ação: atender a cada 14 dias.

### Ativos com compra entre 60d e 90d

Para clientes da segmentação “televendas ruptura de fornecedor”, considerar clientes da carteira("televendas consumidor"); e com a última compra/positivação na empresa nos últimos 90 dias. Ação: atender a cada 14 dias.

### Clientes inativos

Para clientes da segmentação “televendas ruptura de fornecedor”, considerar clientes da carteira("televendas consumidor"); e com a última compra/positivação na empresa entre 90 e 180 dias atrás. Ação: atender a cada 14 dias.

### Ativos com compra em 7 dias

Para clientes vinculados ao time “televendas”, “televendas_2”, considerar clientes com a última compra/positivação na empresa nos últimos 7 dias. Ação: não agendar esses clientes.

### Não agendar Inadimplentes

Para clientes vinculados ao time “televendas”, “televendas_2”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Não agendar - choque de agendas

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: não agendar esses clientes.

### Freq. de 14 dias para clientes sem venda em 8 dias

Aplicar a regra a clientes vinculados ao time “televendas_2”. Ação: atender a cada 14 dias.

## regra_170.gobr

### Ramo distribuidor sem vendas em 60 dias

Para clientes vinculados ao time “todos os vendedores”, considerar clientes ativos para o vendedor; e dos ramos de atividade ("DISTRIBUIDOR"); e sem compra/positivação nos últimos 60 dias. Ação: atender quinzenalmente (a cada 15 dias).

### Compra com regularidade

Para clientes vinculados ao time “todos os vendedores”, considerar clientes sem compra/positivação na empresa nos últimos 10 dias; e frequência histórica menor que 7 dias. Ação: atender a cada 21 dias.

### Não agendar ramo distribuidor com vendas em 60 dias

Para clientes vinculados ao time “todos os vendedores”, considerar clientes ativos para o vendedor; e dos ramos de atividade ("DISTRIBUIDOR"). Ação: não agendar esses clientes.

### Ativos e sem vendas em 30 dias

Para clientes vinculados ao time “todos os vendedores”, considerar clientes ativos para o vendedor; e sem compra/positivação nos últimos 30 dias. Ação: atender quinzenalmente (a cada 15 dias).

### Não agendar ativos com vendas em 30 dias

Para clientes vinculados ao time “todos os vendedores”, considerar clientes ativos para o vendedor. Ação: não agendar esses clientes.

### Clientes inativos e prospects

Aplicar a regra a clientes vinculados ao time “todos os vendedores”. Ação: atender mensalmente (a cada 30 dias).

## regra_171.gobr

### Não agendar inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Não agendar bloqueados

Para clientes vinculados ao time “televendas”, considerar clientes bloqueados. Ação: não agendar esses clientes.

### Não agendar filiais

Para clientes vinculados ao time “televendas”, considerar clientes que são filiais. Ação: não agendar esses clientes.

### Não agendar Baixados na Receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Freq. de 14d para 'Prospect: Cliente potencial'

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 14 dias.

### Freq. de 10d para 'Ativado: fez um pedido e ainda não comprou mais'

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com a empresa e cadastrado há 30 dias. Ação: atender a cada 10 dias.

### Freq. de 14d para 'Ativo: Alta frequência de compra'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa nos últimos 30 dias; e frequência histórica menor que 14 dias. Ação: atender a cada 14 dias.

### Freq. de 21d para 'Ativo: compra regularmente'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa nos últimos 30 dias; e frequência histórica menor que 30 dias. Ação: aplicar frequência do histórico ou no mínimo de 14 dias e no máximo de 28 dias.

### Freq. de 14d para 'Ativo: estimular a regularidade de compra'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa entre 21 e 60 dias atrás. Ação: atender a cada 14 dias.

### Freq. de 7d para 'Em ruptura: risco de ficar inativo'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa entre 61 e 90 dias atrás. Ação: atender a cada 7 dias.

### Freq. de 21d para 'Inativo: reativar cliente sem compra'

Para clientes vinculados ao time “televendas”, considerar clientes cuja última compra/positivação na empresa está fora do intervalo de 90 a 180 dias atrás. Ação: atender a cada 21 dias.

## regra_172.gobr

### Não agendar inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Não agendar filiais

Para clientes vinculados ao time “televendas”, considerar clientes que são filiais. Ação: não agendar esses clientes.

### Ativo:'Freq. de 7 dias'

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias.

### Inativo:'Freq. de 14 dias'

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 14 dias.

## regra_173.gobr

### Não agendar clientes baixados na receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Não agendar inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Não agendar clientes com data da rota na semana

Para clientes vinculados ao time “televendas”, considerar clientes data da rota na semana. Ação: não agendar esses clientes.

### Clientes prospects

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 14 dias.

### Clientes ativos

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 60 dias. Ação: atender a cada 14 dias.

### Risco de inatividade

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 90 dias. Ação: atender a cada 7 dias.

### Inativos (90 dias)

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 120 dias. Ação: atender a cada 14 dias.

### Inativos (120 dias)

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 150 dias. Ação: atender a cada 21 dias.

### Inativos (150 dias)

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 180 dias. Ação: atender a cada 28 dias.

### Clientes que não se enquadraram nas regras padrão

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: não agendar esses clientes.

## regra_174.gobr

### Não agendar inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Não agendar Baixados na Receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Freq. de 14d para 'Prospect: Cliente potencial'

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect para o vendedor. Ação: atender a cada 14 dias.

### Freq. de 21d para 'Ativado: fez um pedido e ainda não comprou mais'

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com o vendedor; e cadastrados há 60 dias. Ação: atender a cada 21 dias.

### Freq. do histórico para 'Ativo: Alta frequência de compra'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor nos últimos 30 dias; e frequência histórica menor que 14 dias. Ação: aplicar frequência do histórico ou no mínimo de 10 dias e no máximo de 14 dias.

### Freq. do histórico para 'Ativo: compra regularmente'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor nos últimos 60 dias; e frequência histórica menor que 30 dias; e dos ramos de atividade ("9", "18"). Ação: aplicar frequência do histórico ou no mínimo de 14 dias e no máximo de 21 dias.

### Freq. de 28d para 'Ativo: compra regularmente'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor nos últimos 60 dias; e frequência histórica menor que 30 dias; e fora dos ramos de atividade ("9", "18"). Ação: atender a cada 28 dias.

### Freq. de 14d para 'Ativo: estimular a regularidade de compra'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor entre 21 e 60 dias atrás; e dos ramos de atividade ("9", "18"). Ação: atender a cada 14 dias.

### Freq. de 21d para 'Ativo: estimular a regularidade de compra'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor entre 21 e 60 dias atrás; e fora dos ramos de atividade ("9", "18"). Ação: atender a cada 21 dias.

### Freq. de 14d para 'Em ruptura: risco de ficar inativo para os ramos 9 e 18'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor entre 61 e 90 dias atrás; e dos ramos de atividade ("9", "18"). Ação: atender a cada 14 dias.

### Freq. de 14d para 'Em ruptura: risco de ficar inativo'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor entre 61 e 90 dias atrás; e fora dos ramos de atividade ("9", "18"). Ação: atender a cada 14 dias.

### Freq. de 21d para 'Inativo: reativar cliente sem compra'

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação com o vendedor nos últimos 90 dias. Ação: atender a cada 21 dias.

## regra_175.gobr

### Não agendar clientes filiais

Para clientes da carteira “activity_in”, considerar clientes que são filiais. Ação: não agendar esses clientes.

### Não agendar clientes inadimplentes

Para clientes da carteira “activity_in”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Não agendar clientes com compra em 30d

Para clientes da carteira “activity_in”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: não agendar esses clientes.

### Clientes ativos na empresa

Para clientes da carteira “activity_in”, considerar clientes ativos para a empresa. Ação: atender a cada 14 dias.

### Clientes inativos na empresa

Para clientes da carteira “activity_in”, considerar clientes inativos para a empresa. Ação: atender a cada 21 dias.

### Clientes que compraram em 2024 e estão sem vendas em 2025

Para clientes da carteira “activity_in”, considerar clientes tem venda da empresa no ano anterior; e nao tem venda da empresa no ano. Ação: atender a cada 21 dias.

### Clientes que compraram em 2023 e não compraram mais

Para clientes da carteira “activity_in”, considerar clientes recência de compra/positivação entre '2023-12-31' e '2023-01-01'. Ação: atender a cada 30 dias.

### Não agendar clientes fora das regras solicitadas

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: não agendar esses clientes.

## regra_176.gobr

### Nordil AL: Não agendar clientes DH com crédito igual ou menor que R$0,00 (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes sem crédito disponível e tipo de cobranca igual("DH"). Ação: não agendar esses clientes.

### Nordil AL: Não agendar clientes BK com crédito menor que R$200,00 (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes com menos de R$ 199 de credito disponivel e tipo de cobranca igual("BK"). Ação: não agendar esses clientes.

### Nordil AL: Não agendar clientes inadimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Nordil AL: Frequência de 7d para clientes ativos/adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias.

### Nordil AL: Frequência de 14d para clientes inativos/adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor. Ação: atender a cada 14 dias.

### Nordil AL: Frequência de 14d para clientes sem venda (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes sem venda. Ação: atender a cada 14 dias.

## regra_177.gobr

### Acioly: Não agendar clientes DH com crédito igual ou menor que R$0,00 (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes sem crédito disponível e tipo de cobranca igual("DH"). Ação: não agendar esses clientes.

### Acioly: Não agendar clientes BK com crédito menor que R$200,00 (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes com menos de R$ 199 de credito disponivel e tipo de cobranca igual("BK"). Ação: não agendar esses clientes.

### Acioly: Não agendar clientes inadimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Acioly: Frequência de 7d para clientes ativos/adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias.

### Acioly: Frequência de 14d para clientes inativos/adimplentes (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes inativos para o vendedor. Ação: atender a cada 14 dias.

### Acioly: Frequência de 14d para clientes sem venda (televendas)

Para clientes da carteira “carteira televendas”, considerar clientes sem venda. Ação: atender a cada 14 dias.

## regra_178.gobr

### Não agendar clientes baixados na receita

Para clientes vinculados ao time “televendas_1”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Clientes que nunca compraram com a empresa

Para clientes vinculados ao time “televendas_2”, considerar clientes cadastrados há 7 dias. Ação: não agendar esses clientes.

### Não agendar clientes com compra recente

Para clientes vinculados ao time “televendas_1”, considerar clientes com a última compra/positivação nos últimos 39 dias. Ação: não agendar esses clientes.

### Tentativa final

Para clientes vinculados ao time “televendas_2”, considerar clientes cadastrados há 60 dias. Ação: atender a cada 30 dias.

### Lead frio

Para clientes vinculados ao time “televendas_2”, considerar clientes cadastrados há 30 dias. Ação: atender a cada 20 dias.

### Lead morno

Para clientes vinculados ao time “televendas_2”, considerar clientes cadastrados há 15 dias. Ação: atender a cada 15 dias.

### Follow-up

Para clientes vinculados ao time “televendas_2”, considerar clientes cadastrados há 8 dias. Ação: atender a cada 15 dias.

### Estimular recompra

Para clientes vinculados ao time “televendas_1”, considerar clientes com a última compra/positivação entre 40 e 89 dias atrás. Ação: atender a cada 15 dias.

### Reativação moderada

Para clientes vinculados ao time “televendas_1”, considerar clientes com a última compra/positivação entre 90 e 119 dias atrás. Ação: atender a cada 7 dias.

### Reativação intensa

Para clientes vinculados ao time “televendas_1”, considerar clientes com a última compra/positivação entre 120 e 359 dias atrás. Ação: atender a cada 7 dias.

### Resgate crítico

Para clientes vinculados ao time “televendas_1”, considerar clientes sem compra/positivação nos últimos 359 dias. Ação: atender a cada 7 dias.

## regra_179.gobr

### Ative um novo cliente em sua carteira! (Todos os segmentos)

Para clientes da carteira “construtora”, “matcon”, “demais_segment”, considerar clientes com ciclo de vida Prospect para o vendedor. Ação: atender a cada 7 dias.

### Estabeleça relacionamento com seu novo cliente! (Construtoras)

Para clientes da carteira “construtora”, considerar clientes unica compra com o vendedor. Ação: atender a cada 14 dias.

### Estabeleça relacionamento com seu novo cliente! (Exceto Construtoras)

Para clientes da carteira “matcon”, “demais_segment”, considerar clientes unica compra com o vendedor. Ação: atender a cada 7 dias.

### Cliente que compra com regularidade! (Exceto Construtoras)

Para clientes da carteira “matcon”, “demais_segment”, considerar clientes com a última compra/positivação entre 7 e 30 dias atrás. Ação: aplicar frequência do histórico ou no mínimo de 7 dias e no máximo de 30 dias.

### Cliente que compra com regularidade! (Construtoras com venda em 30d)

Para clientes da carteira “construtora”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: atender a cada 7 dias.

### Cliente que compra com regularidade! (Construtoras sem venda em 30d)

Para clientes da carteira “construtora”, considerar clientes sem compra/positivação nos últimos 30 dias. Ação: atender a cada 14 dias.

### Estimule a regularidade de compra do seu cliente! (Matcon)

Para clientes da carteira “matcon”, considerar clientes com a última compra/positivação na empresa entre 30 e 60 dias atrás. Ação: atender a cada 7 dias.

### Estimule a regularidade de compra do seu cliente! (Exceto Matcon)

Para clientes da carteira “construtora”, “demais_segment”, considerar clientes com a última compra/positivação na empresa entre 30 e 60 dias atrás. Ação: atender a cada 14 dias.

### Atenção!!! Cliente caminhando para inatividade! (Matcon)

Para clientes da carteira “matcon”, considerar clientes com a última compra/positivação na empresa entre 60 e 89 dias atrás. Ação: atender a cada 7 dias.

### Atenção!!! Cliente caminhando para inatividade! (Construtoras)

Para clientes da carteira “construtora”, considerar clientes com a última compra/positivação na empresa entre 60 e 89 dias atrás. Ação: atender a cada 14 dias.

### Atenção!!! Cliente caminhando para inatividade! (Exceto Matcon e Construtoras)

Para clientes da carteira “demais_segment”, considerar clientes com a última compra/positivação na empresa entre 60 e 89 dias atrás. Ação: atender a cada 21 dias.

### Resgate este cliente inativo! (Matcon)

Para clientes da carteira “matcon”, considerar clientes com a última compra/positivação na empresa entre 90 e 179 dias atrás. Ação: atender a cada 7 dias.

### Resgate este cliente inativo! (Construtoras)

Para clientes da carteira “construtora”, considerar clientes com a última compra/positivação na empresa entre 90 e 179 dias atrás. Ação: atender a cada 21 dias.

### Resgate este cliente inativo! (Exceto Matcon e Construtoras)

Para clientes da carteira “demais_segment”, considerar clientes com a última compra/positivação na empresa entre 90 e 179 dias atrás. Ação: atender a cada 14 dias.

### Requalifique e resgate este cliente! (Exceto Construtoras)

Para clientes da carteira “matcon”, “demais_segment”, considerar clientes sem compra/positivação na empresa nos últimos 180 dias. Ação: atender a cada 14 dias.

### Requalifique e resgate este cliente! (Construtoras)

Para clientes da carteira “construtora”, considerar clientes sem compra/positivação na empresa nos últimos 180 dias. Ação: atender a cada 28 dias.

## regra_180.gobr

### Não agendar filiais

Para clientes vinculados ao time “televendas”, considerar clientes que são filiais. Ação: não agendar esses clientes.

### Não agendar Suspensos, Inapto ou Baixado na Receita Federal

Para clientes vinculados ao time “televendas”, considerar clientes status na receita federal definido como suspensa. Ação: não agendar esses clientes.

### Não agendar Suspenso, Inaptos ou Baixado na Receita Federal

Para clientes vinculados ao time “televendas”, considerar clientes status na receita federal definido como inapta. Ação: não agendar esses clientes.

### Não agendar Suspenso, Inapto ou Baixados na Receita Federal

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Freq. de 7d para ramos de atividade 84, 73, 69, 85 e 22

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("84","73","69","85","22"). Ação: atender a cada 7 dias.

### Freq. de 30d para todos os clientes fora dos ramos de atividade 84, 73, 69, 85 e 22

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 30 dias.

## regra_181.gobr

### Restrição de agendamento - não agendar filiais

Para clientes da carteira “empresa cescom”, considerar clientes que são filiais. Ação: não agendar esses clientes.

### Regra Padrao da Empresa Customizavel: semanal para ativos adimplentes

Para clientes da carteira “empresa cescom”, considerar clientes ativos para o vendedor e adimplentes. Ação: atender semanalmente (a cada 7 dias); usar a preferência de dias configurada pelo vendedor.

### Regra Padrao da Empresa Customizavel: 14 dias para ativos inadimplentes

Para clientes da carteira “empresa cescom”, considerar clientes ativos para o vendedor e inadimplentes. Ação: atender a cada 14 dias; usar a preferência de dias configurada pelo vendedor.

### Regra Padrao da Empresa Customizavel: 14 dias para inativos adimplentes

Para clientes da carteira “empresa cescom”, considerar clientes inativos para o vendedor e adimplentes. Ação: atender a cada 14 dias; usar a preferência de dias configurada pelo vendedor.

### Regra Padrao da Empresa Customizavel: 30 dias para inativos inadimplentes

Para clientes da carteira “empresa cescom”, considerar clientes inativos para o vendedor e inadimplentes. Ação: atender a cada 30 dias; usar a preferência de dias configurada pelo vendedor.

### Regra Padrao da Empresa Customizavel: 14 dias para clientes sem vendas

Para clientes da carteira “empresa cescom”, considerar clientes sem vendas. Ação: atender a cada 14 dias.

## regra_182.gobr

### Não agendar CPF

Para clientes vinculados ao time “televendas”, considerar clientes pessoa física. Ação: não agendar esses clientes.

### Não agendar inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Não agendar baixados na Receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Não agendar cliente com pedido nos últimos 7 dias

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 7 dias. Ação: não agendar esses clientes.

### Prospects dos ramos de atividade 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("089","090","091","092","093","094","095","096","097","098","099","100","101","102","103"); e com ciclo de vida Prospect na empresa. Ação: atender a cada 7 dias.

### Ramo de atividade MANGUEIRAS com pedido em 45d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("089"); e com a última compra/positivação nos últimos 45 dias. Ação: atender a cada 14 dias.

### Ramo de atividade MANGUEIRAS com pedido acima de 45d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("089"). Ação: atender a cada 7 dias.

### Ramo de atividade MATERIAIS DE LIMPEZA com pedido em 60d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("090"); e com a última compra/positivação nos últimos 60 dias. Ação: atender a cada 21 dias.

### Ramo de atividade MATERIAIS DE LIMPEZA com pedido acima de 60d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("090"). Ação: atender a cada 10 dias.

### Ramo de atividade REVENDA EPI com pedido em 45d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("091"); e com a última compra/positivação nos últimos 45 dias. Ação: atender a cada 14 dias.

### Ramo de atividade REVENDA EPI com pedido acima de 45d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("091"). Ação: atender a cada 7 dias.

### Ramo de atividade MATERIAIS DE CONSTRUÇÃO com pedido em 90d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("092"); e com a última compra/positivação nos últimos 90 dias. Ação: atender a cada 28 dias.

### Ramo de atividade MATERIAIS DE CONSTRUÇÃO com pedido acima de 90d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("092"). Ação: atender a cada 14 dias.

### Ramo de atividade FERRAGEM E FERRAMENTAS com pedido em 45d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("093"); e com a última compra/positivação nos últimos 45 dias. Ação: atender a cada 14 dias.

### Ramo de atividade FERRAGEM E FERRAMENTAS com pedido acima de 45d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("093"). Ação: atender a cada 7 dias.

### Ramo de atividade AGROPECUARIA com pedido em 90d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("094"); e com a última compra/positivação nos últimos 90 dias. Ação: atender a cada 28 dias.

### Ramo de atividade AGROPECUARIA com pedido acima 90d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("094"). Ação: atender a cada 14 dias.

### Ramo de atividade PRESTADOR DE SERVIÇO com pedido em 75d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("095"); e com a última compra/positivação nos últimos 75 dias. Ação: atender a cada 21 dias.

### Ramo de atividade PRESTADOR DE SERVIÇO com pedido acima de 75d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("095"). Ação: atender a cada 14 dias.

### Ramo de atividade INDÚSTRIA com pedido em 75d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("096"); e com a última compra/positivação nos últimos 75 dias. Ação: atender a cada 28 dias.

### Ramo de atividade INDÚSTRIA com pedido acima de 75d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("096"). Ação: atender a cada 14 dias.

### Ramo de atividade COOPERATIVA com pedido em 60d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("097"); e com a última compra/positivação nos últimos 60 dias. Ação: atender a cada 21 dias.

### Ramo de atividade COOPERATIVA com pedido acima de 60d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("097"). Ação: atender a cada 10 dias.

### Ramo de atividade HOME CENTER com pedido em 60d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("098"); e com a última compra/positivação nos últimos 60 dias. Ação: atender a cada 21 dias.

### Ramo de atividade HOME CENTER com pedido acima de 60d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("098"). Ação: atender a cada 10 dias.

### Ramo de atividade ATACADO com pedido em 45d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("099"); e com a última compra/positivação nos últimos 45 dias. Ação: atender a cada 14 dias.

### Ramo de atividade ATACADO com pedido acima de 45d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("099"). Ação: atender a cada 7 dias.

### Ramo de atividade CONSTRUTORA com pedido em 75d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("100"); e com a última compra/positivação nos últimos 75 dias. Ação: atender a cada 28 dias.

### Ramo de atividade CONSTRUTORA com pedido acima de 75d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("100"). Ação: atender a cada 7 dias.

### Ramo de atividade ÓRGÃO PÚBLICO com pedido em 90d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("101"); e com a última compra/positivação nos últimos 90 dias. Ação: atender a cada 28 dias.

### Ramo de atividade ÓRGÃO PÚBLICO com pedido acima de 90d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("101"). Ação: atender a cada 14 dias.

### Ramo de atividade E-COMMERCE com pedido em 45d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("102"); e com a última compra/positivação nos últimos 45 dias. Ação: atender a cada 14 dias.

### Ramo de atividade E-COMMERCE com pedido acima de 45d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("102"). Ação: atender a cada 7 dias.

### Ramo de atividade PRODUTOR RURAL com pedido em 90d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("103"); e com a última compra/positivação nos últimos 90 dias. Ação: atender a cada 28 dias.

### Ramo de atividade PRODUTOR RURAL com pedido acima de 90d

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("103"). Ação: atender a cada 14 dias.

## regra_183.gobr

### Não agendar inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Freq. de 21d para prospects

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 21 dias.

### Freq. do histórico para 'Alta frequência de compra'

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor; e frequência histórica menor que 30 dias. Ação: aplicar frequência do histórico ou no mínimo de 5 dias e no máximo de 30 dias.

### Freq. de 14d para 'Compra regularmente' (Sem pedido em 30d)

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor; e frequência histórica maior que 30 dias. Ação: atender a cada 14 dias.

### Freq. de 14d para 'Compra regularmente' (Com pedido em 30d)

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor; e frequência histórica maior que 30 dias; e atividade do vendedor de 30 dias. Ação: atender a cada 14 dias.

### Freq. de 21 para inativos

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Inativo na empresa. Ação: atender a cada 21 dias.

## regra_184.gobr

### Garantir recorrência de compra

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com a empresa; e recência de compra/positivação no mes. Ação: atender a cada 5 dias.

### Alta frequência de compra

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 1 e 7 dias atrás. Ação: aplicar frequência do histórico ou no mínimo de 1 dias e no máximo de 5 dias; definir preferência de atendimento na segunda e na terça.

### Manter regularidade de compra

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 7 e 14 dias atrás. Ação: aplicar frequência do histórico ou no mínimo de 7 dias e no máximo de 12 dias.

### Estimular compra dentro do mês

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 14 e 30 dias atrás. Ação: aplicar frequência do histórico ou no mínimo de 14 dias e no máximo de 28 dias.

### Gerar relacionamento e estimular compra

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 31 e 90 dias atrás. Ação: atender a cada 14 dias.

### Resgate de clientes inativos

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 91 e 180 dias atrás. Ação: atender a cada 14 dias.

### Requalificar perfil e ativar cliente

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação nos últimos 360 dias. Ação: atender a cada 21 dias.

### Clientes com freq. semanal (Time São Paulo)

Para clientes vinculados ao time “sao_paulo”, considerar clientes frequência histórica de 7 dias. Ação: atender a cada 7 dias; definir preferência de atendimento maior na segunda; marcar a parametrização como fixa.

### Clientes com freq. quinzenal (Time São Paulo)

Para clientes vinculados ao time “sao_paulo”, considerar clientes frequência histórica de 14 dias. Ação: atender a cada 14 dias; definir preferência de atendimento maior na segunda; marcar a parametrização como fixa.

### Clientes com freq. mensal (Time São Paulo)

Para clientes vinculados ao time “sao_paulo”, considerar clientes frequência histórica de 28 dias. Ação: atender a cada 28 dias; definir preferência de atendimento maior na segunda; marcar a parametrização como fixa.

### Clientes com freq. bimestral (Time São Paulo)

Para clientes vinculados ao time “sao_paulo”, considerar clientes frequência histórica de 56 dias. Ação: atender a cada 56 dias; definir preferência de atendimento maior na segunda; marcar a parametrização como fixa.

### Clientes com freq. trimestral (Time São Paulo)

Para clientes vinculados ao time “sao_paulo”, considerar clientes frequência histórica de 84 dias. Ação: atender a cada 84 dias; definir preferência de atendimento maior na segunda; marcar a parametrização como fixa.

### Clientes que não se enquadraram nas demais regras

Aplicar a regra a clientes vinculados ao time “televendas”, “sao_paulo”. Ação: atender a cada 30 dias.

## regra_185.gobr

### Não agendar Pessoa Física

Para clientes vinculados ao time “televendas”, considerar clientes pessoa física. Ação: não agendar esses clientes.

### Não agendar baixados na Receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Freq. de 14d para Prospects

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 14 dias.

### Freq. de 7d para Ativos

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Ativo na empresa. Ação: atender a cada 7 dias.

### Freq. de 14 dias para Inativos

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 14 dias.

## regra_186.gobr

### Não agendar clientes que compraram com o televendas em 7d.

Para clientes vinculados ao time “televendas”, considerar clientes tem venda do vendedor em 7 dias. Ação: não agendar esses clientes.

### Não agendar clientes que tem rota em 7 dias à frente.

Para clientes vinculados ao time “televendas”, considerar clientes data da rota futura nos proximos 7 dias. Ação: não agendar esses clientes.

### Ative este cliente! (Nunca tirou pedido)

Para clientes vinculados ao time “televendas”, considerar clientes sem venda da empresa. Ação: atender a cada 14 dias.

### Ative este cliente!

Para clientes vinculados ao time “televendas”, considerar clientes tem venda no ano passado; e com a última compra/positivação entre 180 e 360 dias atrás. Ação: atender a cada 14 dias.

### Restabeleça relacionamento com este cliente que foi ativado!

Para clientes vinculados ao time “televendas”, considerar clientes tem venda da empresa em 14 dias; e tem venda da empresa entre 181 dias e 360 dias; e nao tem venda da empresa entre 15 dias e 180 dias. Ação: atender a cada 14 dias.

### Mantenha a regularidade de compra do cliente que teve pedido detectado nos últimos 30d e foi visitado na semana anterior!

Para clientes vinculados ao time “televendas”, considerar clientes data da rota ha 7 dias atras; e tem visita da empresa na semana anterior; e tem venda da empresa entre 7 dias e 30 dias. Ação: atender a cada 7 dias.

### Garanta regularidade de compra e relacionamento com este cliente! Seu último pedido foi entre 30d e 60d atrás.

Para clientes vinculados ao time “televendas”, considerar clientes data da rota ha 7 dias atras; e tem visita da empresa na semana anterior; e tem venda da empresa entre 31 dias e 60 dias. Ação: atender a cada 7 dias.

### Cliente caminhando para INATIVIDADE! Seu último pedido foi entre 60d e 90d atrás.

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa entre 61 e 90 dias atrás. Ação: atender a cada 7 dias.

### Resgaste este cliente! Seu último pedido foi entre 90d e 180d atrás.

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa entre 91 e 180 dias atrás. Ação: atender a cada 7 dias.

### Atendimento ao cliente que não se enquadrou nas demais regras.

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 28 dias.

## regra_187.gobr

### Não agendar clientes baixados na receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Não agendar filiais

Para clientes vinculados ao time “televendas”, considerar clientes que são filiais. Ação: não agendar esses clientes.

### Não agendar 'Inadimplentes'

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Não agendar clientes recém-cadastrados em 60d

Para clientes vinculados ao time “televendas”, considerar clientes cadastrados há 60 dias. Ação: não agendar esses clientes.

### Não agendar clientes com compras em 60d

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa nos últimos 60 dias. Ação: não agendar esses clientes.

### Clientes Prospects

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 14 dias.

### Inativos Recentes

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 90 dias. Ação: atender a cada 7 dias.

### Inativos Médio

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 120 dias. Ação: atender a cada 7 dias.

### Inativos Antigos

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 180 dias. Ação: atender a cada 14 dias.

### Requalificação de Inativos

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 360 dias. Ação: atender a cada 21 dias.

### Requalificar o cliente do zero

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 28 dias.

## regra_188.gobr

### Não agendar inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Não agendar clientes filiais

Para clientes vinculados ao time “televendas”, considerar clientes que são filiais. Ação: não agendar esses clientes.

### Não agendar Baixados na Receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Este cliente foi pré-qualificado. Aproveite a oportunidade e ative este novo cliente!

Para clientes vinculados ao time “televendas”, considerar clientes sem venda do vendedor. Ação: atender a cada 21 dias.

### Cliente com compra regular e com bom histórico de compra!

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: aplicar frequência do histórico ou no mínimo de 7 dias e no máximo de 30 dias.

### Estimule a regularidade de compra deste cliente, pois ele está entre 30 e 45 dias sem comprar!

Para clientes vinculados ao time “televendas”, considerar clientes cuja última compra/positivação está fora do intervalo de 31 a 45 dias atrás. Ação: atender a cada 14 dias.

### Atenção!!! Cliente deixando de comprar com você! Ele está entre 45 e 60 dias sem comprar!

Para clientes vinculados ao time “televendas”, considerar clientes cuja última compra/positivação está fora do intervalo de 46 a 60 dias atrás. Ação: atender a cada 7 dias.

### Atenção!!! Resgate este cliente caso ele seja perfil!

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 14 dias.

## regra_189.gobr

### Base de valor alto

Para clientes vinculados ao time “televendas”, considerar clientes nao tem venda da empresa no ano; e com ticket medio maior que R$ 4999. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na segunda e na sexta; marcar a parametrização como fixa.

### Base de valor médio

Para clientes vinculados ao time “televendas”, considerar clientes nao tem venda da empresa no ano; e com ticket medio menor que R$ 4999. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na terça e na sexta; marcar a parametrização como fixa.

### Última compra em 2024

Para clientes vinculados ao time “televendas”, considerar clientes não tem venda da empresa no ano; e tem venda da empresa no ano passado. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na quarta e na quinta.

### Ativação de um novo cliente em potencial

Para clientes vinculados ao time “televendas”, considerar clientes sem venda do vendedor. Ação: atender a cada 7 dias.

### Boas vindas a um novo cliente ativado

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com o vendedor. Ação: atender a cada 7 dias.

### Clientes com bom histórico de compra

Para clientes vinculados ao time “televendas”, considerar clientes frequência histórica entre 0 dias e 14 dias. Ação: aplicar frequência do histórico ou no mínimo de 4 dias e no máximo de 6 dias.

### Atenção!!! Cliente com RISCO de ficar inativo

Para clientes vinculados ao time “televendas”, considerar clientes cuja última compra/positivação com o vendedor está fora do intervalo de 25 a 30 dias atrás. Ação: atender a cada 7 dias.

## regra_190.gobr

### Ases: Freq. de 21d para 'PROSPECT: FAZER O PRIMEIRO PEDIDO'

Para clientes vinculados ao time “Televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 21 dias.

### Ases: Freq. de 10d para 'ATIVADO: BOAS VINDAS AO CLIENTE COM O PRIMEIRO PEDIDO'

Para clientes vinculados ao time “Televendas”, considerar clientes unica compra com a empresa; e cadastrados há 30 dias. Ação: atender a cada 10 dias.

### Ases: Freq. de 7d para 'EM RUPTURA: RISCO DE INATIVIDADE'

Para clientes vinculados ao time “Televendas”, considerar clientes adimplentes; e com a última compra/positivação entre 61 e 90 dias atrás. Ação: atender a cada 7 dias.

### Ases: Freq. de 14d 'INATIVOS: RESGATE DE CLIENTES SEM COMPRA'

Para clientes vinculados ao time “Televendas”, considerar clientes adimplentes; e com ciclo de vida Inativo na empresa. Ação: atender a cada 14 dias.

### Ases: Freq. do histórico para 'ATIVO: COMPRA REGULARMENTE Curva A (com compra no mês)'

Para clientes vinculados ao time “Televendas”, considerar clientes classificados na curva A com a empresa; e tem venda no mês. Ação: aplicar frequência do histórico ou no máximo de 30 dias.

### Ases: Freq. de 7d para 'ATIVO: COMPRA REGULARMENTE Curva A (sem compra no mês)'

Para clientes vinculados ao time “Televendas”, considerar clientes classificados na curva A com a empresa. Ação: atender a cada 7 dias.

### Ases: Freq. do histórico para 'ATIVO: COMPRA REGULARMENTE Curva B (com compra no mês)'

Para clientes vinculados ao time “Televendas”, considerar clientes classificados na curva B com a empresa; e tem venda no mês. Ação: aplicar frequência do histórico ou no máximo de 30 dias.

### Ases: Freq. de 14d para 'ATIVO: COMPRA REGULARMENTE Curva B (sem compra no mês)'

Para clientes vinculados ao time “Televendas”, considerar clientes classificados na curva B com a empresa. Ação: atender a cada 14 dias.

### Ases: Freq. do histórico para 'ATIVO: COMPRA REGULARMENTE Curva C (com compra no mês)'

Para clientes vinculados ao time “Televendas”, considerar clientes tem venda no mês. Ação: aplicar frequência do histórico ou no máximo de 30 dias.

### Ases: Freq. de 21d para 'ATIVO: COMPRA REGULARMENTE Curva C (sem compra no mês)'

Aplicar a regra a clientes vinculados ao time “Televendas”. Ação: atender a cada 21 dias.

## regra_191.gobr

### Não agendar clientes baixados na receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Não agendar inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Clientes Prospects

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 21 dias.

### Pós-venda

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 7 dias. Ação: atender a cada 21 dias.

### Alta regularidade

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: aplicar frequência do histórico mais 3 dias ou no mínimo de 14 dias e no máximo de 30 dias.

### Estimular regularidade

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 45 dias. Ação: atender a cada 7 dias.

### Risco de inatividade

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 60 dias. Ação: atender a cada 7 dias.

### Clientes Inativos

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 7 dias.

## regra_192.gobr

### Não agendar clientes baixados na receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Clientes Prospects

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 14 dias.

### Clientes Ativos

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 15 dias. Ação: atender a cada 7 dias.

### Risco de Inatividade

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: atender a cada 3 dias.

### Inativos 30d

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 5 dias.

## regra_193.gobr

### Não agendar clientes filiais

Para clientes vinculados ao time “televendas”, considerar clientes que são filiais. Ação: não agendar esses clientes.

### Não agendar clientes baixados na receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Não agendar clientes fora da semana de cobertura

Para clientes vinculados ao time “televendas”, considerar clientes data da rota futura do vendedor nos proximos 21 dias; e com a última compra/positivação na empresa nos últimos 60 dias. Ação: não agendar esses clientes.

### Freq. de 14d para ramos de atividade específicos, com venda em 60d.

Para clientes da carteira “ramos_freq_14”, considerar clientes com a última compra/positivação na empresa nos últimos 60 dias. Ação: atender a cada 14 dias.

### Freq. de 21d para ramos de atividade específicos, com venda em 60d

Para clientes da carteira “ramos_freq_21”, considerar clientes com a última compra/positivação na empresa nos últimos 60 dias. Ação: atender a cada 21 dias.

### Freq. de 7d para todos os ramos de atividade, sem venda em 60d

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 7 dias.

## regra_194.gobr

### Baixados na Receita Federal

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Prospects (Nunca tirou pedido)

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 7 dias.

### Ativo (Com último pedido em até 60d atrás)

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa nos últimos 60 dias. Ação: atender a cada 14 dias.

### Risco de Inatividade (Com pedido entre 60 e 90d atrás)

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 90 dias. Ação: atender a cada 7 dias.

### Inativo (Com último pedido há mais de 90d atrás)

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 28 dias.

## regra_195.gobr

### Não agendar PF

Para clientes vinculados ao time “televendas”, considerar clientes pessoa física. Ação: não agendar esses clientes.

### Não agendar Baixados na Receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Não agendar clientes com pedido em 7d

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 7 dias. Ação: não agendar esses clientes.

### Manter contato com cliente que comprou no mês

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 7 e 30 dias atrás. Ação: atender a cada 21 dias.

### Ativação de novos

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 14 dias.

### Fazer relacionamento com o cliente

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com a empresa. Ação: atender a cada 21 dias.

### Manter a regularidade de compra

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor entre 31 e 60 dias atrás. Ação: atender a cada 21 dias.

### Atuar para que o cliente não fique inativo

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor entre 61 e 90 dias atrás. Ação: atender a cada 7 dias.

### Resgatar o cliente inativo

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 14 dias.

## regra_196.gobr

### Não agendar Inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Não agendar cidade de Fortaleza e com compra em 60d

Para clientes vinculados ao time “televendas”, considerar clientes localizados nas cidades ("FORTALEZA"); e com a última compra/positivação nos últimos 60 dias. Ação: não agendar esses clientes.

### Freq. de 40d para Prospects

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 40 dias.

### Freq. de 15d para Ativos Adimplentes

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor. Ação: atender a cada 15 dias.

### Freq. de 20d para Inativos Adimplentes

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 20 dias.

## regra_197.gobr

### Não agendar clientes baixados na receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Não agendar inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Não agendar clientes com data da rota na semana

Para clientes vinculados ao time “televendas”, considerar clientes data da rota na semana. Ação: não agendar esses clientes.

### Clientes Prospects

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 14 dias.

### Clientes Ativos

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa nos últimos 60 dias. Ação: atender a cada 7 dias.

### Risco de Inatividade

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa nos últimos 90 dias. Ação: atender a cada 7 dias.

### Inativos + 90d

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 7 dias.

## regra_198.gobr

### Freq. de 25d para Prospects

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 25 dias.

### Freq. de 14d para 'Ativado: Boas vindas ao cliente com primeiro pedido'

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com a empresa; e fora da recencia de venda do vendedor em 30 dias. Ação: atender a cada 14 dias.

### Freq. do histórico para 'Alta frequência de compra'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor nos últimos 30 dias. Ação: aplicar frequência do histórico ou no mínimo de 7 dias e no máximo de 30 dias.

### Freq. de 14d para Ativos

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Ativo na empresa. Ação: atender a cada 14 dias.

### Freq. de 21d para Inativos

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 21 dias.

## regra_199.gobr

### Não agendar inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Não agendar bloqueados

Para clientes vinculados ao time “televendas”, considerar clientes bloqueados. Ação: não agendar esses clientes.

### Freq. de 30d para 'Prospect: Cliente potencial'

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 30 dias.

### Freq. de 30d para 'Ativado: fez um pedido e ainda não comprou mais'

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com a empresa e recência de compra/positivação em 40 dias. Ação: atender a cada 30 dias.

### Freq. de 90d para 'Ativo: compra regularmente'

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor; e frequência histórica menor que 21 dias. Ação: atender a cada 90 dias.

### Freq. de 30d para 'Ativo: estimular a regularidade de compra'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa entre 31 e 59 dias atrás. Ação: atender a cada 30 dias.

### Freq. de 21d para 'Em ruptura: risco de ficar inativo'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa entre 60 e 89 dias atrás. Ação: atender a cada 21 dias.

### Freq. de 45d para 'Inativo: reativar cliente sem compra'

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação na empresa nos últimos 90 dias. Ação: atender a cada 45 dias.

## regra_200.gobr

### Freq. de 21d para 'Prospect: Fazer o primeiro pedido'

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 21 dias.

### Freq. de 10d para 'Ativado: Boas vindas ao cliente com primeiro pedido'

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com a empresa. Ação: atender a cada 10 dias.

### Freq. do histórico para 'Alta frequência de compra'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: aplicar frequência do histórico mais 5 dias ou no máximo de 30 dias.

### Freq. de 14d para 'Compra regularmente'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor nos últimos 30 dias. Ação: atender a cada 14 dias.

### Freq. de 7d para 'Estimular regularidade de compra'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 31 e 60 dias atrás. Ação: atender a cada 7 dias.

### Freq. de 7d para 'Risco de inatividade'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 61 e 90 dias atrás. Ação: atender a cada 7 dias.

### Freq. de 21d para 'Resgate de cliente sem compra' (Inativos)

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 21 dias.

## regra_201.gobr

### Clientes Baixados na Receita Federal

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Clientes Inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Clientes Bloqueados

Para clientes vinculados ao time “televendas”, considerar clientes bloqueados. Ação: não agendar esses clientes.

### Não agendar Filiais

Para clientes vinculados ao time “televendas”, considerar clientes que são filiais. Ação: não agendar esses clientes.

### Prospect: Cliente potencial

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect para o vendedor. Ação: atender a cada 7 dias.

### Inativo: Reativar clientes sem compra

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação nos últimos 90 dias. Ação: atender a cada 28 dias.

### Ativado: Fez um pedido e ainda não comprou mais

Para clientes vinculados ao time “televendas”, considerar clientes cadastrados há 60 dias; e unica compra com o vendedor. Ação: atender a cada 30 dias.

### Ativo: Alta frequência de compra

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 30 dias; e frequência histórica menor que 30 dias. Ação: atender a cada 30 dias.

### Ativo: Compra regularmente

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 30 dias; e frequência histórica menor que 90 dias. Ação: atender a cada 30 dias.

### Ativo: Estimular a regularidade de compra

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 30 e 60 dias atrás. Ação: atender a cada 10 dias.

### Em ruptura: Risco de ficar inativo

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 61 e 90 dias atrás. Ação: atender a cada 14 dias.

### Clientes que hoje não se enquararam nas regras padrão

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: não agendar esses clientes.

## regra_202.gobr

### Freq. de 7d para clientes sem compra em 60d

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação nos últimos 60 dias. Ação: atender a cada 7 dias.

### Ative um novo cliente na sua carteira

Para clientes vinculados ao time “televendas”, considerar clientes sem venda do vendedor. Ação: atender a cada 7 dias.

### Estabeleça relacionamento com seu novo cliente

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com o vendedor; e sem compra/positivação nos últimos 7 dias. Ação: atender a cada 7 dias.

### Cliente que tem uma alta frequência de compra com você!

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: aplicar frequência do histórico ou no máximo de 30 dias.

### Estimule a regularidade de compra do seu cliente, pois ele está sem pedido há mais de 30 dias!

Para clientes vinculados ao time “televendas”, considerar clientes cuja última compra/positivação está fora do intervalo de 31 a 60 dias atrás. Ação: atender a cada 7 dias.

## regra_203.gobr

### Não agendar baixados na receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Não agendar filiais

Para clientes vinculados ao time “televendas”, considerar clientes que são filiais; e id do cliente principal é diferente("36979"). Ação: não agendar esses clientes.

### Não agendar inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Não agendar prospects

Para clientes vinculados ao time “televendas”, considerar clientes sem venda. Ação: não agendar esses clientes.

### Não agendar clientes sem compra em 95 dias

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação nos últimos 95 dias. Ação: não agendar esses clientes.

### Clientes que compraram apenas uma vez

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com a empresa. Ação: atender a cada 28 dias.

### Clientes freq. hist. média de pedidos entre 0 e 7 dias

Para clientes vinculados ao time “televendas”, considerar clientes frequência histórica entre 0 dias e 7 dias. Ação: atender a cada 6 dias.

### Clientes com freq. hist. média de pedidos entre 8 e 14 dias

Para clientes vinculados ao time “televendas”, considerar clientes frequência histórica entre 8 dias e 14 dias. Ação: atender a cada 9 dias.

### Clientes com freq. hist. média de pedidos entre 15 e 21 dias

Para clientes vinculados ao time “televendas”, considerar clientes frequência histórica entre 15 dias e 21 dias. Ação: atender a cada 16 dias.

### Clientes com freq. hist. média de pedidos entre 22 e 28 dias

Para clientes vinculados ao time “televendas”, considerar clientes frequência histórica entre 22 dias e 28 dias. Ação: atender a cada 23 dias.

### Clientes com freq. hist. média de pedidos entre 29 e 38 dias

Para clientes vinculados ao time “televendas”, considerar clientes frequência histórica entre 29 dias e 38 dias. Ação: atender a cada 29 dias.

### Clientes com freq. hist. média de pedidos entre 39 e 60 dias

Para clientes vinculados ao time “televendas”, considerar clientes frequência histórica entre 39 dias e 60 dias. Ação: atender a cada 35 dias.

### Clientes com freq. hist. média de pedidos entre 61 e 95 dias

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 55 dias.

## regra_204.gobr

### Não agendar clientes com compra em 7d

Para clientes vinculados ao time “televendas”, considerar clientes tem venda em 7 dias. Ação: não agendar esses clientes.

### Manter a Regularidade de Compra

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: atender a cada 14 dias.

### Garantir a Positivação da Carteira

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 31 e 60 dias atrás. Ação: atender a cada 14 dias.

### Cliente com Risco de Inatividade

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 61 e 90 dias atrás. Ação: atender a cada 7 dias.

### Clientes Inativos - Frequencia 21 dias

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 21 dias.

## regra_205.gobr

### Freq. de 28d para Prospects

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect para o vendedor. Ação: atender a cada 28 dias.

### Freq. de 14d para Inativos

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação nos últimos 90 dias. Ação: atender a cada 14 dias.

### Cliente ativo na rota de hoje (Quinta ou Segunda)

Aplicar a regra a clientes da carteira “rota_quinta_segunda”. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na quinta e na segunda.

### Cliente ativo na rota de hoje (Terça)

Aplicar a regra a clientes da carteira “rota_terca”. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na terça.

### Cliente ativo na rota de hoje (Quarta)

Aplicar a regra a clientes da carteira “rota_quarta”. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na quarta.

### Cliente ativo na rota de hoje (Sexta)

Aplicar a regra a clientes da carteira “rota_sexta”. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na sexta.

## regra_206.gobr

### Não agendar filiais

Para clientes vinculados ao time “ativo_inativo”, “prospeccao”, considerar clientes que são filiais. Ação: não agendar esses clientes.

### Não agendar inadimplentes

Para clientes vinculados ao time “ativo_inativo”, “prospeccao”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Não agendar Prospects

Para clientes vinculados ao time “ativo_inativo”, considerar clientes com ciclo de vida Prospect na empresa. Ação: não agendar esses clientes.

### Com pedido nos últimos 90d dos segmentos POSTO DE MOLAS, EMPRESA ÔNIBUS, AUTO PEÇAS e MINERAÇÃO.

Para clientes da carteira “0_90”, considerar clientes dos ramos de atividade ("1", "2", "4", "12"). Ação: atender a cada 7 dias.

### Com pedido nos últimos 90d do segmento TRANSPORTADORA.

Para clientes da carteira “0_90”, considerar clientes dos ramos de atividade ("3"). Ação: atender a cada 15 dias.

### Com pedido nos últimos 90d de segmentos não especificados

Aplicar a regra a clientes da carteira “0_90”. Ação: atender a cada 28 dias.

### Com pedido entre 90d e 180d (clientes em risco) dos segmentos POSTO DE MOLAS, EMPRESA ÔNIBUS, AUTO PEÇAS e MINERAÇÃO.

Para clientes da carteira “90_180”, considerar clientes dos ramos de atividade ("1", "2", "4", "12"). Ação: atender a cada 7 dias.

### Com pedido entre 90d e 180d (clientes em risco) do segmento TRANSPORTADORA.

Para clientes da carteira “90_180”, considerar clientes dos ramos de atividade ("3"). Ação: atender a cada 15 dias.

### Com pedido entre 90d e 180d (clientes em risco) de segmentos não especificados

Aplicar a regra a clientes da carteira “90_180”. Ação: atender a cada 28 dias.

### Leads e Prospects dos segmentos POSTO DE MOLAS, EMPRESA ÔNIBUS, AUTO PEÇAS e MINERAÇÃO.

Para clientes vinculados ao time “prospeccao”, considerar clientes dos ramos de atividade ("1", "2", "4", "12"). Ação: atender a cada 7 dias.

### Leads e Prospects do segmento TRANSPORTADORA.

Para clientes vinculados ao time “prospeccao”, considerar clientes dos ramos de atividade ("3"). Ação: atender a cada 15 dias.

### Leads e Prospects de segmentos não especificados.

Aplicar a regra a clientes vinculados ao time “prospeccao”. Ação: atender a cada 28 dias.

## regra_207.gobr

### Não agendar CPF

Para clientes vinculados ao time “televendas”, considerar clientes pessoa física. Ação: não agendar esses clientes.

### Clientes sem pedido com a empresa

Para clientes vinculados ao time “televendas”, considerar clientes sem venda. Ação: atender a cada 14 dias.

### Clientes ativos com alta regularidade

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 14 dias. Ação: aplicar frequência do histórico mais 7 dias ou no máximo de 14 dias.

### Manter a regularidade

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 14 e 30 dias atrás. Ação: atender a cada 14 dias.

### Sem pedido entre 30 a 45d

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 30 e 45 dias atrás. Ação: atender a cada 21 dias.

### Risco de ficar inativo

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 45 e 90 dias atrás. Ação: atender a cada 14 dias.

### Resgate de inativos

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação nos últimos 90 dias. Ação: atender a cada 28 dias.

## regra_208.gobr

### Não agendar Baixados na Receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Não agendar inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Não agendar bloqueados

Para clientes vinculados ao time “televendas”, considerar clientes bloqueados. Ação: não agendar esses clientes.

### Não agendar filiais

Para clientes vinculados ao time “televendas”, considerar clientes que são filiais. Ação: não agendar esses clientes.

### Ativação de novos

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect para o vendedor. Ação: atender a cada 7 dias.

### Fazer relacionamento com o cliente

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com o vendedor. Ação: atender a cada 14 dias.

### Manter contato com o cliente que comprou no mês

Para clientes vinculados ao time “televendas”, considerar clientes recência de compra/positivação no mes; e frequência histórica entre 90 dias e 120 dias. Ação: atender a cada 14 dias.

### Manter a regularidade de compra

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: atender a cada 14 dias.

### Atuar para o cliente não ficar inativo

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 89 dias. Ação: atender a cada 7 dias.

### Resgatar cliente inativo

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 120 dias. Ação: atender a cada 3 dias.

### Não mapeados nas regras

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: não agendar esses clientes.

## regra_209.gobr

### Não agendar Inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Não agendar filiais

Para clientes vinculados ao time “televendas”, considerar clientes que são filiais. Ação: não agendar esses clientes.

### não agendar clientes fora de recencia em 90 dias

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação com o vendedor nos últimos 90 dias. Ação: não agendar esses clientes.

### Ative este novo cliente e aumente sua carteira!!!

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect para o vendedor. Ação: atender a cada 7 dias.

### Cliente compra com regularidade!

Para clientes vinculados ao time “televendas”, considerar clientes frequência histórica entre 0 dias e 30 dias; e com a última compra/positivação com o vendedor nos últimos 30 dias. Ação: atender a cada 7 dias.

### Cliente precisa de acompanhamento!

Para clientes vinculados ao time “televendas”, considerar clientes cuja última compra/positivação com o vendedor está fora do intervalo de 31 a 90 dias atrás. Ação: atender a cada 17 dias.

## regra_210.gobr

### Não agendar Filiais

Para clientes vinculados ao time “televendas”, considerar clientes que são filiais. Ação: não agendar esses clientes.

### Não agendar Inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Não agendar Bloqueados

Para clientes vinculados ao time “televendas”, considerar clientes bloqueados. Ação: não agendar esses clientes.

### Freq. de 30d para 'Ativado: fez um pedido e ainda não comprou mais'

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com o vendedor. Ação: atender a cada 30 dias.

### Freq. de 30d para 'Esquecido'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 181 e 365 dias atrás. Ação: atender a cada 30 dias.

### Freq. de 30d 'Inativo: Reativar cliente sem compra'

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação nos últimos 365 dias. Ação: atender a cada 30 dias.

### Freq. de 30d para 'Ativo fidelizado'

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 30 dias.

## regra_211.gobr

### Cliente com pedido nos últimos 30 dias

Para clientes vinculados ao time “ativacao”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: atender a cada 21 dias.

### Cliente sem pedido nos últimos 30 dias

Aplicar a regra a clientes vinculados ao time “ativacao”. Ação: atender a cada 15 dias.

## regra_212.gobr

### Não agendar clientes que tem rota em 7 dias à frente.

Para clientes vinculados ao time “televendas”, considerar clientes data da rota futura nos proximos 7 dias. Ação: não agendar esses clientes.

### Não agendar clientes que compraram com o televendas em 14d.

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa nos últimos 14 dias. Ação: não agendar esses clientes.

### Mantenha a regularidade de compra do cliente que teve pedido detectado nos últimos 30d e foi visitado na semana anterior!

Para clientes vinculados ao time “televendas”, considerar clientes data da rota ha 7 dias atras; e tem visita da empresa na semana anterior; e com a última compra/positivação na empresa entre 14 e 30 dias atrás. Ação: atender a cada 7 dias.

### Garanta regularidade de compra e relacionamento com este cliente! Seu último pedido foi entre 30d e 60d atrás.

Para clientes vinculados ao time “televendas”, considerar clientes data da rota ha 7 dias atras; e tem visita da empresa na semana anterior; e com a última compra/positivação na empresa entre 31 e 60 dias atrás. Ação: atender a cada 20 dias.

### Ative este cliente! (Nunca tirou pedido)

Para clientes vinculados ao time “televendas”, considerar clientes sem venda. Ação: atender a cada 14 dias.

### Ative este cliente!

Para clientes vinculados ao time “televendas”, considerar clientes recência de compra/positivação global no ano passado; e com a última compra/positivação na empresa entre 180 e 360 dias atrás. Ação: atender a cada 14 dias.

### Cliente caminhando para INATIVIDADE! Seu último pedido foi entre 60d e 90d atrás.

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa entre 61 e 90 dias atrás. Ação: atender a cada 7 dias.

### Resgaste este cliente! Seu último pedido foi entre 90d e 180d atrás.

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa entre 91 e 180 dias atrás. Ação: atender a cada 7 dias.

### Atendimento ao cliente que não se enquadrou nas demais regras.

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 7 dias.

## regra_213.gobr

### Não agendar Clientes Filiais

Para clientes vinculados ao time “time televendas”, considerar clientes que são filiais. Ação: não agendar esses clientes.

### Clientes Ativos (segunda)

Para clientes da carteira “carteira_segunda”, considerar clientes ativos para o vendedor. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na segunda; marcar a parametrização como fixa.

### Clientes Inativos (segunda)

Aplicar a regra a clientes da carteira “carteira_segunda”. Ação: atender a cada 28 dias; definir preferência de atendimento na segunda; marcar a parametrização como fixa.

### Clientes Ativos (terça)

Para clientes da carteira “carteira_terca”, considerar clientes ativos para o vendedor. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na terça; marcar a parametrização como fixa.

### Clientes Inativos (terça)

Aplicar a regra a clientes da carteira “carteira_terca”. Ação: atender a cada 28 dias; definir preferência de atendimento na terça; marcar a parametrização como fixa.

### Clientes Ativos (quarta)

Para clientes da carteira “carteira_quarta”, considerar clientes ativos para o vendedor. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na quarta; marcar a parametrização como fixa.

### Clientes Inativos (quarta)

Aplicar a regra a clientes da carteira “carteira_quarta”. Ação: atender a cada 28 dias; definir preferência de atendimento na quarta; marcar a parametrização como fixa.

### Clientes Ativos (quinta)

Para clientes da carteira “carteira_quinta”, considerar clientes ativos para o vendedor. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na quinta; marcar a parametrização como fixa.

### Clientes Inativos (quinta)

Aplicar a regra a clientes da carteira “carteira_quinta”. Ação: atender a cada 28 dias; definir preferência de atendimento na quinta; marcar a parametrização como fixa.

### Clientes Ativos (sexta)

Para clientes da carteira “carteira_sexta”, considerar clientes ativos para o vendedor. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento na sexta; marcar a parametrização como fixa.

### Clientes Inativos (sexta)

Aplicar a regra a clientes da carteira “carteira_sexta”. Ação: atender a cada 28 dias; definir preferência de atendimento na sexta; marcar a parametrização como fixa.

### Clientes sem dia específico

Aplicar a regra a clientes da carteira “carteira_curitiba”. Ação: atender semanalmente (a cada 7 dias).

## regra_214.gobr

### Não agendar inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Freq. de 14d para 'Cliente sem pedido com o vendedor'

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com o vendedor. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Freq. de 21d para 'Ativado: fez um pedido e ainda não comprou mais'

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com o vendedor; e com a última compra/positivação nos últimos 30 dias; e dos ramos de atividade ("29"). Ação: atender a cada 21 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Freq. de 14d para 'Ativado: fez um pedido e ainda não comprou mais'

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com o vendedor; e com a última compra/positivação nos últimos 30 dias; e fora dos ramos de atividade ("29"). Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Freq. de 10d para 'Ativo: compra regularmente'

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor; e frequência histórica menor que 14 dias. Ação: atender a cada 10 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Freq. de 30d para 'Ativo: estimular a regularidade de compra'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor entre 21 e 59 dias atrás; e dos ramos de atividade ("29"). Ação: atender a cada 30 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Freq. de 14d para 'Ativo: estimular a regularidade de compra'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor entre 21 e 59 dias atrás; e fora dos ramos de atividade ("29"). Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Freq. de 14d para 'Em ruptura: risco de ficar inativo' (RA 29)

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor entre 60 e 89 dias atrás; e dos ramos de atividade ("29"). Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Freq. de 14d para 'Em ruptura: risco de ficar inativo'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor entre 60 e 89 dias atrás; e fora dos ramos de atividade ("29"). Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Freq. de 10d para 'Resgate de cliente sem compra'

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação com o vendedor nos últimos 90 dias. Ação: atender a cada 10 dias; dar preferência de atendimento aos dias úteis e ao sábado.

## regra_215.gobr

### Freq. de 7d para 'Primeira compra'

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect para o vendedor. Ação: atender a cada 7 dias.

### Freq. de 7d para 'Prospect ativado'

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com o vendedor; e sem compra/positivação nos últimos 20 dias. Ação: atender a cada 7 dias.

### Freq. de 7d para 'Compra regularmente'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor nos últimos 30 dias. Ação: atender a cada 7 dias.

### Freq. de 7d para 'Ativo: estimular a regularidade de compra'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor entre 31 e 60 dias atrás. Ação: atender a cada 7 dias.

### Freq. de 7d para 'Risco de inatividade'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor entre 60 e 90 dias atrás. Ação: atender a cada 7 dias.

### Freq. de 7d para 'Resgate de cliente sem compra'

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação com o vendedor nos últimos 90 dias. Ação: atender a cada 7 dias.

## regra_216.gobr

### Ative um novo cliente em sua carteira! (Todos os segmentos)

Para clientes da carteira “construtora”, “matcon”, “demais_segment”, considerar clientes com ciclo de vida Prospect para o vendedor. Ação: atender a cada 7 dias.

### Estabeleça relacionamento com seu novo cliente! (Construtoras)

Para clientes da carteira “construtora”, considerar clientes unica compra com o vendedor. Ação: atender a cada 14 dias.

### Estabeleça relacionamento com seu novo cliente! (Exceto Construtoras)

Para clientes da carteira “matcon”, “demais_segment”, considerar clientes unica compra com o vendedor. Ação: atender a cada 7 dias.

### Cliente que compra com regularidade! (Exceto Construtoras)

Para clientes da carteira “matcon”, “demais_segment”, considerar clientes com a última compra/positivação entre 7 e 30 dias atrás. Ação: aplicar frequência do histórico ou no mínimo de 7 dias e no máximo de 30 dias.

### Cliente que compra com regularidade! (Construtoras com venda em 30d)

Para clientes da carteira “construtora”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: atender a cada 7 dias.

### Cliente que compra com regularidade! (Construtoras sem venda em 30d)

Para clientes da carteira “construtora”, considerar clientes sem compra/positivação nos últimos 30 dias. Ação: atender a cada 14 dias.

### Estimule a regularidade de compra do seu cliente! (Matcon)

Para clientes da carteira “matcon”, considerar clientes com a última compra/positivação na empresa entre 30 e 60 dias atrás. Ação: atender a cada 7 dias.

### Estimule a regularidade de compra do seu cliente! (Exceto Matcon)

Para clientes da carteira “construtora”, “demais_segment”, considerar clientes com a última compra/positivação na empresa entre 30 e 60 dias atrás. Ação: atender a cada 14 dias.

### Atenção!!! Cliente caminhando para inatividade! (Matcon)

Para clientes da carteira “matcon”, considerar clientes com a última compra/positivação na empresa entre 60 e 89 dias atrás. Ação: atender a cada 7 dias.

### Atenção!!! Cliente caminhando para inatividade! (Construtoras)

Para clientes da carteira “construtora”, considerar clientes com a última compra/positivação na empresa entre 60 e 89 dias atrás. Ação: atender a cada 14 dias.

### Atenção!!! Cliente caminhando para inatividade! (Exceto Matcon e Construtoras)

Para clientes da carteira “demais_segment”, considerar clientes com a última compra/positivação na empresa entre 60 e 89 dias atrás. Ação: atender a cada 21 dias.

### Resgate este cliente inativo! (Matcon)

Para clientes da carteira “matcon”, considerar clientes com a última compra/positivação na empresa entre 90 e 179 dias atrás. Ação: atender a cada 7 dias.

### Resgate este cliente inativo! (Construtoras)

Para clientes da carteira “construtora”, considerar clientes com a última compra/positivação na empresa entre 90 e 179 dias atrás. Ação: atender a cada 21 dias.

### Resgate este cliente inativo! (Exceto Matcon e Construtoras)

Para clientes da carteira “demais_segment”, considerar clientes com a última compra/positivação na empresa entre 90 e 179 dias atrás. Ação: atender a cada 14 dias.

### Requalifique e resgate este cliente! (Exceto Construtoras)

Para clientes da carteira “matcon”, “demais_segment”, considerar clientes sem compra/positivação na empresa nos últimos 180 dias. Ação: atender a cada 14 dias.

### Requalifique e resgate este cliente! (Construtoras)

Para clientes da carteira “construtora”, considerar clientes sem compra/positivação na empresa nos últimos 180 dias. Ação: atender a cada 28 dias.

## regra_217.gobr

### Fazer relacionamento com o cliente

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com o vendedor. Ação: atender a cada 7 dias.

### Manter a regularidade de compra

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 7 e 30 dias atrás. Ação: aplicar frequência do histórico ou no mínimo de 14 dias e no máximo de 28 dias.

## regra_218.gobr

### Freq. de 5d para clientes sem compra em 7d

Para clientes vinculados ao time “televendas_1”, considerar clientes sem compra/positivação nos últimos 7 dias. Ação: atender a cada 5 dias.

### Freq. do histórico para clientes com recência de compra entre 0 e 14d

Para clientes vinculados ao time “televendas_1”, considerar clientes com a última compra/positivação nos últimos 14 dias. Ação: aplicar frequência do histórico ou no máximo de 14 dias.

### Freq. de 14d para clientes sem compra em 14d

Aplicar a regra a clientes vinculados ao time “televendas_1”. Ação: atender a cada 14 dias.

### Freq. de 14d para clientes sem pedido

Para clientes vinculados ao time “televendas_2”, considerar clientes com ciclo de vida Prospect para o vendedor. Ação: atender a cada 14 dias.

### Freq. de 14d para clientes com compra em 30d

Para clientes vinculados ao time “televendas_2”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: atender a cada 14 dias.

### Freq. de 7d para clientes sem compra em 30d

Aplicar a regra a clientes vinculados ao time “televendas_2”. Ação: atender a cada 7 dias.

## regra_219.gobr

### Não agendar baixados na Receita Federal

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Não agendar com compra em 25d

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa nos últimos 25 dias. Ação: não agendar esses clientes.

### Ative essa oportunidade - Cliente nunca tirou pedido com o vendedor

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect para o vendedor. Ação: atender a cada 21 dias.

### Cliente com pedido com a empresa entre 25 e 60 dias

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa entre 26 e 60 dias atrás. Ação: atender a cada 14 dias.

### Cliente com pedido com a empresa entre 60 e 90 dias

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa entre 61 e 90 dias atrás. Ação: atender a cada 7 dias.

### Atenda esse cliente inativo há mais de 90 dias

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 21 dias.

## regra_220.gobr

### Não agendar clientes com compra na empresa nos últimos 30 dias - Carteira Regional

Para clientes vinculados ao time “carteira regional”, considerar clientes com a última compra/positivação na empresa nos últimos 30 dias. Ação: não agendar esses clientes.

### Regra Padrao da Girobem: Frequênicia de 7 dias para clientes sem comprar entre 30 e 150 dias - Carteira Regional

Aplicar a regra a clientes vinculados ao time “carteira regional”. Ação: atender a cada 7 dias.

### Regra Padrao da Girobem: 14 dias para clientes com mais de 150 dias sem compra  - Carteira Reativação

Para clientes vinculados ao time “carteira reativacao”, considerar clientes inatividade global maior que 149 dias. Ação: atender a cada 14 dias.

### Regra Padrao da Girobem: 14 dias para clientes sem compra  - Carteira Reativação

Para clientes vinculados ao time “carteira reativacao”, considerar clientes sem venda. Ação: atender a cada 14 dias.

### Regra Padrao da Girobem: Não agendar clientes com menos de 150 dias sem compra  - Carteira Reativação

Aplicar a regra a clientes vinculados ao time “carteira reativacao”. Ação: não agendar esses clientes.

### Regra Padrao da Girobem: 7 dias para todos os clientes - Carteira Direta

Aplicar a regra a clientes vinculados ao time “carteira direta”. Ação: atender a cada 7 dias.

## regra_221.gobr

### Este cliente foi pré-qualificado! Aproveite a oportunidade e ative este novo cliente!!!

Para clientes vinculados ao time “televendas”, considerar clientes sem venda do vendedor. Ação: atender a cada 21 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Este cliente foi ativado! Mantenha ele ativo em sua carteira!!!

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com o vendedor; e sem compra/positivação nos últimos 30 dias. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Cliente com compra regular e com bom histórico de compra!!!

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 30 dias; e sem compra/positivação nos últimos 21 dias. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Estimule a regularidade de compra deste cliente, pois ele está entre 30 e 60 dias sem comprar!!!

Para clientes vinculados ao time “televendas”, considerar clientes cuja última compra/positivação está fora do intervalo de 31 a 60 dias atrás. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Atenção!!! Cliente deixando de comprar com você! Ele está entre 60 e 90 dias sem comprar!

Para clientes vinculados ao time “televendas”, considerar clientes cuja última compra/positivação está fora do intervalo de 61 a 90 dias atrás. Ação: atender a cada 7 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Atenção!!! Resgate este cliente caso ele seja perfil!

Para clientes vinculados ao time “televendas”, considerar clientes cuja última compra/positivação está fora do intervalo de 91 a 360 dias atrás. Ação: atender a cada 28 dias; definir preferência de atendimento nos dias úteis e no sábado".

## regra_222.gobr

### Freq. de 14d para 'Sem venda há mais de 30d'

Para clientes vinculados ao time “ruptura_global”, considerar clientes adimplentes; e nao tem venda em 30 dias; e dos ramos de atividade ("6","7","8","10","28","32","33","37","38","40","41","42"). Ação: atender a cada 14 dias.

### Freq. de 14d para 'Sem venda há mais de 45d'

Para clientes vinculados ao time “ruptura_global”, considerar clientes adimplentes; e sem compra/positivação nos últimos 45 dias; e dos ramos de atividade ("1","2","3","4","11","12","13","14","15","16","17","18","19","20","21","22", "23","24","25","26","27","29","30","31","34","35","36","39","50","99"). Ação: atender a cada 14 dias.

### Freq. de 14d para curva A e com compra em 90 dias

Para clientes vinculados ao time “carteira”, considerar clientes com a última compra/positivação nos últimos 90 dias; e classificados na curva A com a empresa. Ação: atender a cada 14 dias.

### Freq. de 21d para curva B e com compra em 90 dias

Para clientes vinculados ao time “carteira”, considerar clientes com a última compra/positivação nos últimos 90 dias; e classificados na curva B com a empresa. Ação: atender a cada 21 dias.

### Freq. de 28d para curva C e com compra em 90 dias

Para clientes vinculados ao time “carteira”, considerar clientes com a última compra/positivação nos últimos 90 dias; e classificados na curva C com a empresa. Ação: atender a cada 28 dias.

### Freq. de 21d para sem classificação de curva e com compra em 90 dias

Para clientes vinculados ao time “carteira”, considerar clientes com a última compra/positivação nos últimos 90 dias. Ação: atender a cada 21 dias.

### Freq. de 21d para sem compra há mais de 90 dias

Aplicar a regra a clientes vinculados ao time “carteira”. Ação: atender a cada 21 dias.

## regra_223.gobr

### Cliente com pedido nos últimos 30 dias

Para clientes vinculados ao time “ativacao”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: atender a cada 21 dias.

### Cliente sem pedido nos últimos 30 dias

Aplicar a regra a clientes vinculados ao time “ativacao”. Ação: atender a cada 15 dias.

### Cliente com compra na semana corrente (Entre seg. e sex)

Para clientes vinculados ao time “generalista”, considerar clientes recência de compra/positivação na semana. Ação: não agendar esses clientes.

### Cliente semanal - padrão

Aplicar a regra a clientes vinculados ao time “generalista”. Ação: atender a cada 7 dias.

### Todos os clientes

Aplicar a regra a clientes vinculados ao time “construtora”. Ação: atender a cada 14 dias.

## regra_224.gobr

### Não agendar clientes baixados na receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Não agendar clientes com data da rota na semana

Para clientes vinculados ao time “televendas”, considerar clientes data da rota na semana. Ação: não agendar esses clientes.

### Clientes Prospects

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 14 dias.

### Clientes Ativos

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa nos últimos 60 dias. Ação: atender a cada 7 dias.

### Risco de Inatividade

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa nos últimos 90 dias. Ação: atender a cada 7 dias.

### Inativos + 90d

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 7 dias.

## regra_225.gobr

### Freq. de 10d para Prospects

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 10 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Freq. de 21d para Ativos Adimplentes

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor; e adimplentes. Ação: atender a cada 21 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Freq. de 10d para Ativos Inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor. Ação: atender a cada 10 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Freq. de 14d para Inativos Adimplentes

Para clientes vinculados ao time “televendas”, considerar clientes adimplentes. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Freq. de 21d para Inativos Inadimplentes

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 21 dias; dar preferência de atendimento aos dias úteis e ao sábado.

## regra_226.gobr

### Ative essa oportunidade

Para clientes vinculados ao time “televendas”, considerar clientes sem venda da empresa. Ação: atender a cada 7 dias.

### Cliente ativado! Crie relacionamento com seu cliente!

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa nos últimos 30 dias; e unica compra com a empresa. Ação: atender a cada 14 dias.

### Clientes que compram mensalmente (clientes regulares)

Para clientes vinculados ao time “televendas”, considerar clientes frequência histórica de 30 dias; e com a última compra/positivação na empresa nos últimos 120 dias. Ação: atender a cada 28 dias.

### Recência de atendimento igual a recência de compra (clientes que compram mês sim, mês não)

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor entre 20 e 30 dias atrás. Ação: aplicar frequência do histórico ou no máximo de 60 dias.

### Mantenha seu cliente ativo! Ele está há 120 dias sem comprar com a empresa

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação na empresa nos últimos 120 dias. Ação: atender a cada 14 dias.

### Resgate seu cliente inativo! Ele está há mais de 180 dias sem comprar com a empresa

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação na empresa nos últimos 180 dias. Ação: atender a cada 28 dias.

## regra_227.gobr

### Cobertura de rota de visita exatamente 7 dias depois

Para clientes vinculados ao time “felipe”, considerar clientes data da rota ha 7 dias atras. Ação: atender a cada 1 dia; marcar a parametrização como fixa.

### Não agendar clientes com compra em 30 dias (Ativos)

Para clientes vinculados ao time “felipe”, considerar clientes com a última compra/positivação na empresa nos últimos 30 dias. Ação: não agendar esses clientes.

### Freq. de 60d para clientes que nunca compraram (Prospects)

Para clientes vinculados ao time “felipe”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 60 dias.

### Freq. de 15d para clientes com compra entre 30 e 90 dias (Ativos)

Para clientes vinculados ao time “felipe”, considerar clientes com a última compra/positivação na empresa entre 30 e 90 dias atrás. Ação: atender a cada 15 dias.

### Freq. de 10d para clientes sem compra em 90 dias (Inativos)

Aplicar a regra a clientes vinculados ao time “felipe”. Ação: atender a cada 10 dias.

### Nao agendar clientes nao cobertos pelas regras

Aplicar a regra a clientes vinculados ao time “felipe”. Ação: não agendar esses clientes.

## regra_228.gobr

### Ative este novo cliente!

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect para o vendedor. Ação: atender a cada 28 dias.

### Cliente ativado!

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com o vendedor. Ação: atender a cada 21 dias.

### Compra com regularidade! (Curva C)

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 90 dias; e classificados na curva C com a empresa. Ação: atender a cada 7 dias.

### Compra com regularidade! (Curva A e B)

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 90 dias. Ação: atender a cada 14 dias.

### Cliente caminhando para inatividade!

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 91 e 180 dias atrás. Ação: atender a cada 28 dias.

### Resgatar cliente inativo!

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 45 dias.

## regra_229.gobr

### Não agendar clientes com compra em 30 dias

Para clientes vinculados ao time “farm”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: não agendar esses clientes.

### Este cliente nunca comprou de você. Faz sentido ele ficar na sua carteira? Ele é perfil? Você tem interesse em ativá-lo? Se sim, execute o atendimento!

Para clientes vinculados ao time “farm”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 14 dias.

### Mantenha este cliente com cobertura mensal de positivação - Ele está entre 31 e 60 dias sem compra!

Para clientes vinculados ao time “farm”, considerar clientes cuja última compra/positivação está fora do intervalo de 31 a 60 dias atrás. Ação: atender a cada 14 dias.

### Este cliente está caminhando para inatividade - Ele está entre 61 e 90 dias sem compra!

Para clientes vinculados ao time “farm”, considerar clientes cuja última compra/positivação está fora do intervalo de 61 a 90 dias atrás. Ação: atender a cada 21 dias.

### Este cliente já não tem fidelidade com a sua empresa - Ele está há mais de 90 dias sem compra!

Aplicar a regra a clientes vinculados ao time “farm”. Ação: atender a cada 28 dias.

## regra_230.gobr

### Não agendar inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Freq. de 14d para 'Prospect: Cliente potencial'

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect para o vendedor. Ação: atender a cada 14 dias.

### Freq. de 7d para 'Ativado: fez um pedido e ainda não comprou mais'

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com o vendedor. Ação: atender a cada 7 dias.

### Freq. de 14d para 'Ativo: compra regularmente'

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor; e frequência histórica menor que 16 dias. Ação: atender a cada 14 dias.

### Freq. de 14d para 'Ativo: estimular a regularidade de compra'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor entre 16 e 45 dias atrás. Ação: atender a cada 14 dias.

### Freq. de 7d para 'Em ruptura: risco de ficar inativo'

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor entre 60 e 89 dias atrás. Ação: atender a cada 7 dias.

### Freq. de 21d para 'Inativo: reativar cliente sem compra'

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação com o vendedor nos últimos 60 dias. Ação: atender a cada 21 dias.

## regra_231.gobr

### Baixados na receita

Para clientes vinculados ao time “carteira_regional”, “carteira_reativacao”, “carteira_direta”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Clientes com compra nos últimos 30 dias

Para clientes vinculados ao time “carteira_regional”, considerar clientes com a última compra/positivação na empresa nos últimos 30 dias. Ação: não agendar esses clientes.

### Clientes com compra entre 30 e 150 dias

Para clientes vinculados ao time “carteira_regional”, considerar clientes com a última compra/positivação na empresa entre 30 e 150 dias atrás. Ação: atender a cada 7 dias.

### Clientes com compra em 150 dias

Para clientes vinculados ao time “carteira_reativacao”, considerar clientes com a última compra/positivação na empresa nos últimos 150 dias. Ação: não agendar esses clientes.

### Clientes sem compra

Para clientes vinculados ao time “carteira_reativacao”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 14 dias.

### Clientes sem compra em 150 dias

Para clientes vinculados ao time “carteira_reativacao”, considerar clientes inatividade global maior que 149 dias. Ação: atender a cada 14 dias.

### Freq. de 7d para todos os clientes

Aplicar a regra a clientes vinculados ao time “carteira_direta”. Ação: atender a cada 7 dias.

## regra_232.gobr

### Não agendar filiais

Para clientes vinculados ao time “televendas”, considerar clientes que são filiais. Ação: não agendar esses clientes.

### Não agendar clientes Inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Freq. de 21d para clientes Prospects

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 21 dias.

### Freq. do histórico para clientes com compra entre 1 e 29 dias

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 29 dias. Ação: aplicar frequência do histórico ou no mínimo de 14 dias e no máximo de 30 dias.

### Freq. de 21d para clientes com compra entre 30 e 59 dias

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 30 e 59 dias atrás. Ação: atender a cada 21 dias.

### Freq. de 21d para clientes com compra entre 60 e 89 dias

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 60 e 89 dias atrás. Ação: atender a cada 21 dias.

### Freq. de 21d para clientes sem compra em 90 dias

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 21 dias.

## regra_233.gobr

### Nordece: Não agendar clientes DH com crédito igual ou menor que R$0,00 (televendas)

Para clientes vinculados ao time “televendas”, considerar clientes sem crédito disponível e tipo de cobranca igual("DH"). Ação: não agendar esses clientes.

### Nordece: Não agendar clientes BK com crédito menor que R$200,00 (televendas)

Para clientes vinculados ao time “televendas”, considerar clientes com menos de R$ 199 de credito disponivel e tipo de cobranca igual("BK"). Ação: não agendar esses clientes.

### Nordece: Não agendar clientes inadimplentes (televendas)

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Nordece: Frequência de 7d para clientes ativos/adimplentes (televendas)

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor. Ação: atender a cada 7 dias.

### Nordece: Frequência de 14d para clientes inativos/adimplentes (televendas)

Para clientes vinculados ao time “televendas”, considerar clientes inativos para o vendedor. Ação: atender a cada 14 dias.

### Nordece: Frequência de 14d para clientes sem venda (televendas)

Para clientes vinculados ao time “televendas”, considerar clientes sem venda. Ação: atender a cada 14 dias.

## regra_234.gobr

### Regra Padrao do goVendas: 3 dias para clientes em queda de faturamento

Para clientes da carteira “empresa toda”, considerar clientes queda de faturamento maior que 5%. Ação: atender a cada 3 dias.

### Regra Padrao do goVendas - Customizavel: Nao agendar quem esta a mais de 1138 dias sem comprar

Para clientes da carteira “empresa toda”, considerar clientes com a última compra/positivação entre 1138 e 9999 dias atrás. Ação: não agendar esses clientes.

### Regra Padrao do goVendas Customizável - Teste cidade goiania

Para clientes da carteira “empresa toda”, considerar clientes localizados nas cidades ("GOIANIA"). Ação: usar a frequência média dos clientes inativos da empresa; definir preferência de atendimento nos dias úteis e no sábado e no domingo.

### Regra Padrao do goVendas Customizável - Clientes ativos

Para clientes da carteira “empresa toda”, considerar clientes ativos para o vendedor. Ação: usar a frequência média dos clientes ativos da empresa; definir preferência de atendimento nos dias úteis e no sábado e no domingo.

### Regra Padrao do goVendas Customizável - Clientes inativos

Para clientes da carteira “empresa toda”, considerar clientes inativos para o vendedor. Ação: usar a frequência média dos clientes inativos da empresa; definir preferência de atendimento nos dias úteis e no sábado e no domingo.

### Regra Padrao do goVendas Customizável - Clientes sem vendas

Para clientes da carteira “empresa toda”, considerar clientes sem vendas. Ação: usar a frequência média dos clientes inativos da empresa; definir preferência de atendimento nos dias úteis e no sábado e no domingo.

### Regra Padrao - default

Aplicar a regra a clientes da carteira “empresa toda”. Ação: atender a cada 7 dias; dar preferência de atendimento aos dias úteis (segunda a sexta-feira).

## regra_235.gobr

### Nao agendar - clientes baixados na receita

Para clientes vinculados ao time “felipe”, “paola_1”, “paola_2”, “temporario_2meses”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Nao agendar - clientes com rota futura em 7 dias

Para clientes vinculados ao time “paola_1”, “paola_2”, considerar clientes data da rota futura em 7 dias. Ação: não agendar esses clientes.

### Nao agendar - clientes com recencia de positivacao em 7 dias

Para clientes vinculados ao time “paola_1”, “paola_2”, considerar clientes com a última compra/positivação nos últimos 7 dias. Ação: não agendar esses clientes.

### Clientes com compra em 30 dias

Para clientes vinculados ao time “felipe”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: não agendar esses clientes.

### Cobertura de rota de visita exatamente 14 dias depois

Para clientes vinculados ao time “temporario_2meses”, considerar clientes data da rota ha 14 dias atras; e com 5% de credito. Ação: atender a cada 1 dia; dar preferência de atendimento aos dias úteis e ao sábado.

### Clientes com compra entre 30 e 90 dias

Para clientes vinculados ao time “felipe”, considerar clientes com a última compra/positivação entre 30 e 90 dias atrás. Ação: atender a cada 15 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Clientes sem compra em 90 dias

Aplicar a regra a clientes vinculados ao time “felipe”. Ação: atender a cada 10 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Clientes com rota ha 7 dias ou mais

Para clientes vinculados ao time “paola_1”, “paola_2”, considerar clientes data da rota em 7 dias; e com 5% de credito. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Clientes com compra entre 7 e 30 dias

Para clientes vinculados ao time “paola_1”, “paola_2”, considerar clientes com a última compra/positivação na empresa entre 7 e 30 dias atrás; e com 5% de credito. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Clientes com compra entre 31 e 60 dias

Para clientes vinculados ao time “paola_1”, “paola_2”, considerar clientes com a última compra/positivação na empresa entre 31 e 60 dias atrás; e com 5% de credito. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Clientes com compra entre 61 e 89 dias

Para clientes vinculados ao time “paola_1”, “paola_2”, considerar clientes com a última compra/positivação na empresa entre 61 e 89 dias atrás; e com 5% de credito. Ação: atender a cada 7 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Clientes com compra entre 90 e 179 dias

Para clientes vinculados ao time “paola_1”, “paola_2”, considerar clientes com a última compra/positivação na empresa entre 90 e 179 dias atrás; e com 5% de credito. Ação: atender a cada 14 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Clientes sem compra em 180 dias

Para clientes vinculados ao time “paola_1”, “paola_2”, considerar clientes com 5% de credito. Ação: atender a cada 21 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Clientes que hoje não se enquadraram nas regras padrão

Aplicar a regra a clientes vinculados ao time “felipe”, “paola_1”, “paola_2”, “temporario_2meses”. Ação: não agendar esses clientes.

## regra_236.gobr

### Não agendar baixados na Receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Rota todos os dias (com venda recente)

Para clientes da carteira “cidades_todo_dia”, “bairros_todo_dia”, considerar clientes com a última compra/positivação nos últimos 1 dias. Ação: atender semanalmente (a cada 7 dias).

### Rota todos os dias

Aplicar a regra a clientes da carteira “cidades_todo_dia”, “bairros_todo_dia”. Ação: atender a cada 2 dias.

### Rota segunda, quarta e sexta

Para clientes da carteira “cidades_seg_qua_sex”, “bairros_seg_qua_sex”, considerar clientes fora da recência de compra/positivação na semana. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento normal na segunda e normal na quarta e normal na sexta.

### Rota terça e quinta

Para clientes da carteira “cidades_rj_ter_qui”, “bairros_rj_ter_qui”, “cidades_sp_ter_qui”, considerar clientes fora da recência de compra/positivação na semana. Ação: atender semanalmente (a cada 7 dias); definir preferência de atendimento normal na terça e normal na quinta.

### Não agendar clientes fora das regras padrão

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: não agendar esses clientes.

## regra_237.gobr

### Clientes ativados

Para clientes vinculados ao time “televendas”, considerar clientes sem venda. Ação: atender a cada 14 dias.

### Compra com regularidade

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 30 dias; e frequência histórica menor que 30 dias. Ação: aplicar frequência do histórico ou no mínimo de 0 dias e no máximo de 30 dias.

### Estimular a regularidade

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 30 e 60 dias atrás. Ação: atender a cada 14 dias.

### Clientes resgatados

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação nos últimos 60 dias; e frequência histórica maior que 30 dias. Ação: atender a cada 14 dias.

### Resgatar inativos

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação nos últimos 60 dias. Ação: atender a cada 14 dias.

## regra_238.gobr

### Matenha relacionamento com seu cliente!

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa nos últimos 59 dias. Ação: atender a cada 14 dias.

### Se não mantiver a regularidade de compra, o cliente ficará inativo!

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação na empresa nos últimos 89 dias. Ação: atender a cada 14 dias.

### Resgate seu cliente inativo!

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 14 dias.

## regra_239.gobr

### Não agendar clientes baixados na receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Não agendar clientes com data da rota na semana

Para clientes vinculados ao time “televendas”, considerar clientes data da rota na semana. Ação: não agendar esses clientes.

### Clients ativos

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 60 dias. Ação: atender a cada 14 dias.

### Risco de inatividade

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 90 dias. Ação: atender a cada 7 dias.

### Inativos 90 dias

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 120 dias. Ação: atender a cada 14 dias.

### Inativos 120 dias

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 150 dias. Ação: atender a cada 21 dias.

### Inativos 150 dias

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 180 dias. Ação: atender a cada 28 dias.

### Clientes não mapeados nas regras

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: não agendar esses clientes.

## regra_240.gobr

### Clientes com compra em 7d

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 7 dias. Ação: não agendar esses clientes.

### Manter a regularidade de compra!

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 30 dias. Ação: atender a cada 14 dias.

### Garantir a positivação da carteira!

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 60 dias. Ação: atender a cada 14 dias.

### Cliente com risco de inatividade!

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 90 dias. Ação: atender a cada 7 dias.

### Clientes inativos

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: atender a cada 21 dias.

## regra_241.gobr

### Não agendar clientes baixados na receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Clientes revenda freq 7 dias

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("106","139","109","143","141","142"). Ação: atender a cada 7 dias.

### Clientes revenda freq 14 dias

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("140","146","148"). Ação: atender a cada 14 dias.

### Clientes revenda freq 28 dias

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("138"). Ação: atender a cada 28 dias.

### Clientes comsumo freq 7 dias

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("144","147","108"). Ação: atender a cada 7 dias.

### Clientes comsumo freq 14 dias

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("111","100","110","112","145","107","113"). Ação: atender a cada 14 dias.

### Clientes comsumo freq 28 dias

Para clientes vinculados ao time “televendas”, considerar clientes dos ramos de atividade ("114"). Ação: atender a cada 28 dias.

### Clientes fora dos ramos mapeados

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: não agendar esses clientes.

## regra_242.gobr

### Freq. hist. de 0 a 30d - sem compra em 20d

Para clientes vinculados ao time “televendas”, considerar clientes frequência histórica entre 0 dias e 30 dias; e com a última compra/positivação entre 20 e 30 dias atrás. Ação: atender a cada 21 dias.

### Freq. hist. de 31 a 60d - sem compra em 29d

Para clientes vinculados ao time “televendas”, considerar clientes frequência histórica entre 31 dias e 60 dias; e com a última compra/positivação entre 29 e 44 dias atrás. Ação: atender a cada 21 dias.

### Freq. hist. de 31 a 60d - sem compra em 44d

Para clientes vinculados ao time “televendas”, considerar clientes frequência histórica entre 31 dias e 60 dias; e com a última compra/positivação entre 44 e 60 dias atrás. Ação: atender a cada 21 dias.

### Freq. hist. de 61 a 90d - sem compra em 60d

Para clientes vinculados ao time “televendas”, considerar clientes frequência histórica entre 61 dias e 90 dias; e com a última compra/positivação entre 61 e 90 dias atrás. Ação: atender a cada 15 dias.

### Freq. hist. de 61 a 90d - sem compra em 90d

Para clientes vinculados ao time “televendas”, considerar clientes frequência histórica entre 61 dias e 90 dias; e com a última compra/positivação entre 90 e 180 dias atrás. Ação: atender a cada 21 dias.

### Freq. hist. de 91 a 180d - sem compra em 44d

Para clientes vinculados ao time “televendas”, considerar clientes frequência histórica entre 91 dias e 180 dias; e com a última compra/positivação entre 44 e 120 dias atrás. Ação: atender a cada 21 dias.

### Freq. hist. de 91 a 180d - sem compra em 120d

Para clientes vinculados ao time “televendas”, considerar clientes frequência histórica entre 91 dias e 180 dias; e com a última compra/positivação entre 120 e 180 dias atrás. Ação: atender a cada 15 dias.

## regra_243.gobr

### Ative este cliente!

Para clientes vinculados ao time “televendas”, considerar clientes sem venda; e pessoa jurídica. Ação: atender a cada 21 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Faça seu pós-vendas!

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 20 dias; e pessoa jurídica. Ação: atender a cada 3 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Mantenha o cliente engajado!

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação entre 20 e 33 dias atrás; e pessoa jurídica. Ação: aplicar frequência do histórico mais 2 dias ou no mínimo de 20 dias e no máximo de 33 dias; dar preferência de atendimento aos dias úteis e ao sábado.

### Não agendar clientes sem compra em 33 dias

Para clientes vinculados ao time “televendas”, considerar clientes pessoa jurídica. Ação: não agendar esses clientes.

### Não agendar se não for PJ

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: não agendar esses clientes.

## regra_244.gobr

### Não agendar filiais

Para clientes vinculados ao time “televendas”, considerar clientes que são filiais. Ação: não agendar esses clientes.

### Não agendar inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Prospect: Cliente potencial

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect para o vendedor. Ação: atender a cada 14 dias.

### Ativado: Fez um pedido e ainda não comprou mais

Para clientes vinculados ao time “televendas”, considerar clientes unica compra com o vendedor. Ação: atender a cada 7 dias.

### Freq. histórica para Ativo: compra regularmente

Para clientes vinculados ao time “televendas”, considerar clientes ativos para o vendedor; e frequência histórica menor que 8 dias. Ação: aplicar frequência do histórico ou no mínimo de 5 dias e no máximo de 7 dias.

### Estimular a regularidade de compra

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor entre 8 e 30 dias atrás. Ação: atender a cada 14 dias.

### Em ruptura: risco de ficar inativo

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação com o vendedor entre 31 e 60 dias atrás. Ação: atender a cada 7 dias.

### Inativo: reativar cliente sem compra

Para clientes vinculados ao time “televendas”, considerar clientes sem compra/positivação com o vendedor nos últimos 60 dias. Ação: atender a cada 14 dias.

## regra_245.gobr

### Não agendar Inadimplentes

Para clientes vinculados ao time “televendas”, considerar clientes inadimplentes. Ação: não agendar esses clientes.

### Não agendar baixados na Receita

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Não agendar sem crédito

Para clientes vinculados ao time “televendas”, considerar clientes sem crédito disponível. Ação: não agendar esses clientes.

### Não agendar clientes com compra em 60d

Para clientes vinculados ao time “televendas”, considerar clientes com a última compra/positivação nos últimos 60 dias. Ação: não agendar esses clientes.

### Com atendimento/venda na semana / Rota: Todos os dias - Agendar para semana seguinte (freq. do hist.)

Para clientes da carteira “rota_todo_dia”, considerar clientes recência de visita na semana. Ação: aplicar frequência do histórico ou no mínimo de 7 dias e no máximo de 14 dias.

### Sem atendimento/venda na semana / Rota: Todos os dias - Agendar para semana corrente (freq. do hist. +2)

Aplicar a regra a clientes da carteira “rota_todo_dia”. Ação: aplicar frequência do histórico mais 2 dias ou no mínimo de 3 dias e no máximo de 7 dias.

### Com atendimento/venda na semana / Rota: Ter / Pref. de agend.: Seg

Para clientes da carteira “rota_terca”, considerar clientes recência de visita na semana. Ação: atender a cada 7 dias; definir preferência de atendimento maior na segunda.

### Sem atendimento/venda na semana / Rota: Ter / Pref. de agend.: Seg

Aplicar a regra a clientes da carteira “rota_terca”. Ação: atender a cada 7 dias; definir preferência de atendimento maior na segunda.

### Com atendimento/venda na semana / Rota: Qua / Pref. de agend.: Ter

Para clientes da carteira “rota_quarta”, considerar clientes recência de visita na semana. Ação: atender a cada 7 dias; definir preferência de atendimento maior na terça.

### Sem atendimento/venda na semana / Rota: Qua / Pref. de agend.: Ter

Aplicar a regra a clientes da carteira “rota_quarta”. Ação: atender a cada 7 dias; definir preferência de atendimento maior na terça.

### Com atendimento/venda na semana / Rota: Qui / Pref. de agend.: Qua

Para clientes da carteira “rota_quinta”, considerar clientes recência de visita na semana. Ação: atender a cada 7 dias; definir preferência de atendimento maior na quarta.

### Sem atendimento/venda na semana / Rota: Qui / Pref. de agend.: Qua

Aplicar a regra a clientes da carteira “rota_quinta”. Ação: atender a cada 7 dias; definir preferência de atendimento maior na quarta.

### Com atendimento/venda na semana / Rota: Sex / Pref. de agend.: Qui

Para clientes da carteira “rota_sexta”, considerar clientes recência de visita na semana. Ação: atender a cada 7 dias; definir preferência de atendimento maior na quinta.

### Sem atendimento/venda na semana / Rota: Sex / Pref. de agend.: Qui

Aplicar a regra a clientes da carteira “rota_sexta”. Ação: atender a cada 7 dias; definir preferência de atendimento maior na quinta.

### Com atendimento/venda na semana / Rota: Seg / Pref. de agend.: Sex

Para clientes da carteira “rota_segunda”, considerar clientes recência de visita na semana. Ação: atender a cada 7 dias; definir preferência de atendimento maior na sexta.

### Sem atendimento/venda na semana / Rota: Seg / Pref. de agend.: Sex

Aplicar a regra a clientes da carteira “rota_segunda”. Ação: atender a cada 7 dias; definir preferência de atendimento maior na sexta.

### Com atendimento/venda na semana - Cidades não informadas nas rotas - Agendar para semana seguinte (freq. do hist.)

Para clientes vinculados ao time “televendas”, considerar clientes recência de visita na semana. Ação: aplicar frequência do histórico ou no mínimo de 7 dias e no máximo de 14 dias.

### Sem atendimento/venda na semana - Cidades não informadas nas rotas - Agendar para semana corrente (freq. do hist. -1)

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: aplicar frequência do histórico menos 1 dias ou no mínimo de 1 dias e no máximo de 7 dias.

## regra_246.gobr

### Baixados na Receita Federal

Para clientes vinculados ao time “televendas”, considerar clientes com status “baixada” na Receita Federal. Ação: não agendar esses clientes.

### Prospects

Para clientes vinculados ao time “televendas”, considerar clientes com ciclo de vida Prospect na empresa. Ação: atender a cada 7 dias.

### Ativos dos ramos de atividade POSTO DE COMBUSTIVEL, FARMACIA E DROGARIA, SUPERMERCADO, REDE DE FAST FOOD, REDE DE POSTO DE COMBUSTIVEL, REDE DE DROGARIA, REDE DE SUPERMERCADO, REDE DE HIPERMERCADO, EMPRESA DE ONIBUS, TRANSPORTADORA, LOGISTICA, POSTO DE SERVICO - VDO

Para clientes da carteira “ramos_1”, considerar clientes com a última compra/positivação na empresa nos últimos 45 dias. Ação: atender a cada 14 dias.

### Inativos dos ramos de atividade POSTO DE COMBUSTIVEL, FARMACIA E DROGARIA, SUPERMERCADO, REDE DE FAST FOOD, REDE DE POSTO DE COMBUSTIVEL, REDE DE DROGARIA, REDE DE SUPERMERCADO, REDE DE HIPERMERCADO, EMPRESA DE ONIBUS, TRANSPORTADORA, LOGISTICA, POSTO DE SERVICO - VDO

Aplicar a regra a clientes da carteira “ramos_1”. Ação: atender a cada 7 dias.

### Ativos dos ramos de atividade DISTRIB. AUTOPECAS, DISTRIB. PECAS MECANICAS, DISTRIB. PECAS ELETRICAS, DISTRIB. PECAS E ACESSORIOS, DISTRIB. ACESSORIOS, DISTRIB. FILTROS/LUBRIFICANTES, CONCESSIONARIAS, AUTOMACAO, SUPRIMENTO DE INFORMATICA, GRAFICA, EMBALAGEM E DESCARTAVEL, MATERIAL DE LIMPEZA, MATERIAL DE ESCRITORIO, MATERIAL HOSPITALAR, PAPELARIA, COOPERATIVA, MAGAZINES, E-COMERCE, REDE DE MAGAZINE, REDE LOJA VAREJISTA, HOSPITAL, LABORATORIO, IND. ALIMENTICIA, IND. DE BEBIDAS, IND. FARMACEUTICA, IND. FRIGORIFICA

Para clientes da carteira “ramos_2”, considerar clientes com a última compra/positivação na empresa nos últimos 60 dias. Ação: atender a cada 21 dias.

### Inativos dos ramos de atividade DISTRIB. AUTOPECAS, DISTRIB. PECAS MECANICAS, DISTRIB. PECAS ELETRICAS, DISTRIB. PECAS E ACESSORIOS, DISTRIB. ACESSORIOS, DISTRIB. FILTROS/LUBRIFICANTES, CONCESSIONARIAS, AUTOMACAO, SUPRIMENTO DE INFORMATICA, GRAFICA, EMBALAGEM E DESCARTAVEL, MATERIAL DE LIMPEZA, MATERIAL DE ESCRITORIO, MATERIAL HOSPITALAR, PAPELARIA, COOPERATIVA, MAGAZINES, E-COMERCE, REDE DE MAGAZINE, REDE LOJA VAREJISTA, HOSPITAL, LABORATORIO, IND. ALIMENTICIA, IND. DE BEBIDAS, IND. FARMACEUTICA, IND. FRIGORIFICA

Aplicar a regra a clientes da carteira “ramos_2”. Ação: atender a cada 10 dias.

### Ativos dos ramos de atividade IMPLEMENTOS RODOVIARIOS, LOJA DE CONVENIENCIA, FARMACIA DE MANIPULACAO, ACOUGUE, PEIXARIA, HORTIFRUTI, PADARIA E CONFEITARIA, LANCHONETE, PIZZARIA, RESTAURANTE, MATERIAL DE CONSTRUCAO, JOALHERIA, LIVRARIA, FLORICULTURA, ARMARINHOS E MIUDEZAS, COSMETICOS, PERFUMARIA, HIGIENE PESSOAL, CIA DE GAS, ADMINISTRADORA DE CARTOES, ESTACIONAMENTO, HOTEL, INST. DE ENSINO, INST. FINANCEIRA, OFICINA, SHOPPING, ENTRETERIMENTO, IND. AUTOMOBILISTICA, IND. DE CALCADOS, IND. DE COSMETICOS, IND. PAPEL, IND. QUIMICA, IND. TEXTIL, IND. BRINQUEDOS, IND. MANUFATURAS, IND. ELETRONICOS

Para clientes da carteira “ramos_3”, considerar clientes com a última compra/positivação na empresa nos últimos 75 dias. Ação: atender a cada 28 dias.

### Inativos dos ramos de atividade IMPLEMENTOS RODOVIARIOS, LOJA DE CONVENIENCIA, FARMACIA DE MANIPULACAO, ACOUGUE, PEIXARIA, HORTIFRUTI, PADARIA E CONFEITARIA, LANCHONETE, PIZZARIA, RESTAURANTE, MATERIAL DE CONSTRUCAO, JOALHERIA, LIVRARIA, FLORICULTURA, ARMARINHOS E MIUDEZAS, COSMETICOS, PERFUMARIA, HIGIENE PESSOAL, CIA DE GAS, ADMINISTRADORA DE CARTOES, ESTACIONAMENTO, HOTEL, INST. DE ENSINO, INST. FINANCEIRA, OFICINA, SHOPPING, ENTRETERIMENTO, IND. AUTOMOBILISTICA, IND. DE CALCADOS, IND. DE COSMETICOS, IND. PAPEL, IND. QUIMICA, IND. TEXTIL, IND. BRINQUEDOS, IND. MANUFATURAS, IND. ELETRONICOS

Aplicar a regra a clientes da carteira “ramos_3”. Ação: atender a cada 14 dias.

### Ativos dos ramos de atividade RECARGA CELULAR, VIDRACARIA, EXPORTACAO DIRETA, EXPORTACAO TRADE, EVENTOS E SHOWS, REPRESENTANTE, PROMOTOR DE VENDA, OUTROS

Para clientes da carteira “ramos_4”, considerar clientes com a última compra/positivação na empresa nos últimos 90 dias. Ação: atender a cada 28 dias.

### Inativos dos ramos de atividade RECARGA CELULAR, VIDRACARIA, EXPORTACAO DIRETA, EXPORTACAO TRADE, EVENTOS E SHOWS, REPRESENTANTE, PROMOTOR DE VENDA, OUTROS

Aplicar a regra a clientes da carteira “ramos_4”. Ação: atender a cada 14 dias.

### Clientes que hoje não se enquadraram nas regras padrão

Aplicar a regra a clientes vinculados ao time “televendas”. Ação: não agendar esses clientes.

