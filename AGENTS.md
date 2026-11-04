# Instruções do projeto (NovaDrive Dashboard)

## Sobre o projeto

Painel **somente leitura** sobre o PostgreSQL da rede **NovaDrive Motors** (concessionárias). Desenvolvimento guiado por **Spec-Driven Development**: implemente apenas o que está em `specs/`; `requirements.md`, `design.md` e `tasks.md` são a fonte da verdade.

Stakeholders do case: **Ricardo Matos** (CEO), **Fernanda Alves** (Gerente Comercial), **Bruno Tavares** (CIO).

## Regras não negociáveis (CIO)

- Acesso ao banco é **somente leitura**. Nunca gerar ou executar INSERT, UPDATE, DELETE ou DDL.
- Banco: **PostgreSQL**. Driver: `psycopg2` via **SQLAlchemy**.
- Interface: **Python + Streamlit**. Gráficos: **Plotly** ou **Altair**.
- Credenciais **nunca** no código-fonte. Usar `.env` ou `st.secrets`.
- Consultas em `vendas`: **filtro de período na SQL**, nunca carregar a tabela inteira para filtrar depois.
- Cache (`st.cache_data`): **~1 min** para agregações simples; **15–20 min** para consultas com muitos joins.
- **Sem autenticação/login** nesta versão (uso interno).
- Erros de conexão: mensagem amigável, **sem expor credenciais**.

## Como trabalhar neste repositório

1. Antes de codar, leia a spec em `specs/<pasta>/`, o diagrama `docs/diagrama-banco-dados.png` e a exploração **`docs/notas-banco.md`** (joins, escopo das 7 tabelas, sanidade dos dados).
2. Não implemente fora da spec. Ambiguidade ou coluna inexistente → pare e pergunte.
3. Ordem: `01-acesso-dados` → `02-dashboard-executivo` → `03-analise-comercial`.
4. Código em `src/`, testes em `tests/`, páginas Streamlit em `pages/`. Mantenha `requirements.txt` atualizado.

Prompts sugeridos: `prompts.md`.
