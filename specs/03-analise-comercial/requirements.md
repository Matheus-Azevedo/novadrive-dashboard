# Requirements — Análise Comercial

**Stakeholder:** Fernanda Alves — Gerente Comercial

## Objetivo

Ferramenta operacional para o time comercial acompanhar vendedores, concessionárias, modelos vendidos e desconto praticado.

## Contexto do Pedido

Fernanda quer ranking de vendedores, comparação entre concessionárias, ticket médio, modelos mais vendidos, taxa de conversão de funil, desconto médio e visibilidade de veículos parados no pátio — nem tudo é possível com o banco atual.

## Perguntas de esclarecimento e Respostas

| Pergunta | Resposta |
|----------|----------|
| O que é taxa de conversão de funil? | Clientes que **entram na loja** vs. **quantos compraram**. |
| Banco só tem vendas concluídas, sem lead/visita — o que fazer? | Problema reconhecido: **focar no possível**, **registrar** e cobrar **na próxima fase**. |
| O que é desconto médio? | Diferença entre **preço de tabela** do carro e **valor realmente pago**. |
| Frequência de atualização dos dados? | Consulta **toda manhã**; não precisa tempo real — **de hora em hora já ajuda** (alinha ao cache do CIO). |
| Comparar concessionárias? | **Sim** — ex.: Rio vs. Porto Alegre, e **entender por quê**. |

## User stories

- Ranking de vendedores por **faturamento** e **quantidade**, filtrável por concessionária.
- **Ticket médio** geral e por vendedor/concessionária no período.
- **Modelos de veículos** mais vendidos no período.
- **Desconto médio** (`veiculos.valor - vendas.valor_pago`) por vendedor e concessionária, incluindo vendas acima da tabela.
- Comparar desempenho comercial entre concessionárias quando houver vendas no período.

## Fora do Escopo / decisões negociadas

- **Taxa de conversão de funil:** fora — sem tabela de leads/visitas.
- **Veículos parados no pátio:** fora — sem inventário/estoque.
- **Desconto médio:** **dentro do escopo** — colunas `veiculos.valor` e `vendas.valor_pago` permitem o cálculo descrito por Fernanda.

## Critérios de Aceite

- [ ] Ranking e ticket médio respeitam o período selecionado.
- [ ] Nenhum dado de funil inventado ou estimado por proxy.
- [ ] Desconto médio correto; vendas acima da tabela **visíveis**, não ocultas.
- [ ] Comparação entre concessionárias coerente e comparável.
