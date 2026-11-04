# Requirements — Acesso a Dados (camada base, somente leitura)

**Stakeholder:** Bruno Tavares — CIO

## Objetivo

Garantir camada de acesso ao PostgreSQL de produção **somente leitura**, alinhada às regras técnicas do CIO, como fundação de `02-dashboard-executivo` e `03-analise-comercial`.

## Contexto do Pedido

Antes de qualquer acesso ao banco, Bruno definiu regras não negociáveis: leitura apenas, interface Streamlit, credenciais fora do código, filtro de período sempre no SQL e cache proporcional ao peso da consulta.

## Perguntas de esclarecimento e Respostas

| Pergunta | Resposta |
|----------|----------|
| Qual intervalo de cache é aceitável? | Agregação simples: **~1 min**. Consulta pesada com muitos joins: **15–20 min**. |
| Precisa de autenticação/login no dashboard? | **Não** nesta versão — uso interno. |
| Pode usar outra biblioteca além de Streamlit? | **Sim** para gráficos (Plotly, Altair); a **UI** continua Streamlit. |
| Qual o cuidado com volume de dados / limite de linhas? | Banco cresce rápido: **nunca** trazer tabela inteira; **sempre filtrar por período na query**. |

## User stories

- Conectar ao PostgreSQL com credenciais lidas de variável de ambiente ou `st.secrets` na inicialização.
- Impedir execução de qualquer instrução de escrita em consultas.
- Aplicar filtro de período na cláusula SQL quando a consulta envolver `vendas`.
- Cachear resultados com `st.cache_data` e TTL conforme peso da consulta (1 min vs 15–20 min).
- Exibir erro amigável em falha de conexão, sem expor credenciais.

## Fora do Escopo / decisões negociadas

- Autenticação/login: fora do escopo (uso interno).
- Escrita ou alteração de dados: **nunca** — regra fixa, não negociável.

## Critérios de Aceite

- [ ] Nenhuma credencial no código-fonte nem em mensagens de erro.
- [ ] Toda consulta em `vendas` inclui filtro de período no SQL.
- [ ] Cache nas consultas dos dashboards com TTL adequado.
- [ ] Conexão via `.env` ou `st.secrets`, nunca hardcoded.
