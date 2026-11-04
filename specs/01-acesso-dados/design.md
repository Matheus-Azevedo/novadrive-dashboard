# Design — Acesso a Dados

## Visão geral da solução

Módulo de conexão e execução de queries somente leitura, reutilizado pelos dashboards (`02` e `03`).

## Referência de dados

- Modelo ER: `docs/diagrama-banco-dados.png`
- Exploração validada (joins, escopo, sanidade): **`docs/notas-banco.md`** — decisões abaixo assumem esse documento.

## Dados utilizados

Somente as **7 tabelas** listadas em `notas-banco.md`. **Não** consultar views extras (`stg_vendas`, `vendedores_concessionarias`, etc.).

Toda função que toca `vendas` recebe `data_inicio` e `data_fim` e aplica:

`WHERE v.data_venda >= :data_inicio AND v.data_venda < :data_fim` (ou `BETWEEN`, equivalente).

Colunas e joins canônicos: ver seção “Relacionamentos” em `notas-banco.md`.

## Fluxo

`.env` / `st.secrets` → `database.py` (engine SQLAlchemy + psycopg2) → `queries.py` (funções parametrizadas por período) → `st.cache_data` → páginas Streamlit.

## Decisões Técnicas

- Driver `psycopg2-binary` via SQLAlchemy; usuário somente leitura.
- `st.cache_data`: TTL ~60 s (agregações só em `vendas`); 900–1200 s (joins conforme `notas-banco.md`).
- Evitar `SELECT *`; listar colunas da seção “Colunas críticas” em `notas-banco.md`.
- Guard que rejeita SQL de escrita antes da execução.
- Funções de query nomeadas por domínio (ex.: agregados executivos vs comerciais), sempre com parâmetros de período.

## Riscos / pontos em aberto

- Faixa real de datas estreita (ver snapshot em `notas-banco.md`): testes e demos devem usar intervalo que retorna linhas.
- Crescimento futuro de `vendas` pode exigir paginação ou pré-agregação diária (fora do MVP).
