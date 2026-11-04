# Requirements — Dashboard Executivo

**Stakeholder:** Ricardo Matos — CEO

## Objetivo

Dar ao CEO visão rápida e executiva do desempenho de vendas entre concessionárias, para decisão ágil e apoio à apresentação trimestral ao conselho (sem gerar slides automaticamente).

## Contexto do Pedido

Ricardo hoje só acompanha o negócio pelo **fechamento mensal do financeiro** — tarde para agir. Quer abrir uma tela e ver se vende mais ou menos que antes, quais unidades vão bem ou mal e, se possível, **projeção do mês**.

## Perguntas de esclarecimento e Respostas

| Pergunta | Resposta |
|----------|----------|
| O que significa “performando bem”? Qual métrica? | **Faturamento** e **quantidade de veículos vendidos** — ambos importam. |
| Pode detalhar o método de projeção? | **Não precisa ser sofisticado**; pode ficar para depois se for muito complicado agora. |
| Comparar concessionárias e regiões? | **Sim** — ponto principal: saber qual unidade **carrega** a empresa e qual **pesa**. |
| Qual o prazo / urgência? | **O quanto antes**, mas prefere **certo** a **rápido e errado**. |

## User stories

- Exibir **faturamento total** e **quantidade de veículos vendidos** no período selecionado.
- Exibir **evolução de vendas** ao longo do tempo (faturamento e/ou quantidade).
- **Comparar todas as concessionárias** por faturamento e quantidade (inclusive sem vendas no período).
- Permitir comparação por **estado/cidade** quando os dados existirem.
- Exibir **projeção simples** do fechamento do mês (run-rate) quando o período for o **mês corrente**.

## Fora do Escopo / decisões negociadas

- **Projeção:** MVP com run-rate simples (regra de três no ritmo do mês) ou registrar como fase 2 se atrasar escopo.
- **Geração automática de apresentação** para o conselho: fora — painel visual limpo, não export de slides.
- **Metas e orçamento:** fora — não existem no banco.

## Critérios de Aceite

- [ ] Números respeitam o período selecionado.
- [ ] Todas as concessionárias na comparação, mesmo com zero vendas.
- [ ] Projeção deixa claro que é **estimativa simples (run-rate)**, não previsão estatística.
- [ ] Painel utilizável sem tabela extensa — visual, não planilha.
