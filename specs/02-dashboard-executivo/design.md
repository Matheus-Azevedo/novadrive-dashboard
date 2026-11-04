# Design — Dashboard Executivo

## Visão geral da solução

Página Streamlit com filtro de período (sidebar), cards (faturamento, quantidade, ticket médio), gráfico de evolução temporal, comparação entre concessionárias e por estado/cidade. Card de projeção com aviso de estimativa simples.

## Referência de dados

- **`docs/notas-banco.md`** — joins geográficos, default de período, regra `LEFT JOIN` para concessionárias com zero vendas no filtro.

## Dados utilizados

Fato: `vendas` (`valor_pago`, `data_venda`).

Dimensões:

- Unidade: `concessionarias.concessionaria`
- Geografia: `cidades.cidade`, `estados.estado`, `estados.sigla` (caminho em `notas-banco.md`)

Não usar `clientes` nesta página salvo necessidade futura.

## Fluxo

Filtro de datas (default sugerido: intervalo entre `MIN` e `MAX` de `data_venda` documentados em `notas-banco.md`, ou últimos 7 dias até a data máxima disponível) → `queries.py` → cache → formatação leve (pandas) → gráficos Plotly.

## Decisões Técnicas

- **Lista de concessionárias:** partir de `concessionarias` com `LEFT JOIN` em vendas agregadas no período, para incluir unidades com **zero** vendas (critério Ricardo + notas de sanidade).
- **Projeção (run-rate):** só quando o filtro for o mês corrente; fórmula simples em `notas-banco.md` / requirements; aviso na UI sobre sazonalidade.
- Gráficos Plotly: linha (evolução por dia), barras (por concessionária e por estado).
- Cache 15–20 min nas queries com join em `cidades`/`estados`.
- Evolução temporal: agrupar por `DATE(data_venda)` no SQL.

## Riscos / pontos em aberto

- Janela histórica curta no banco dificulta gráficos de longo prazo até novas cargas ETL.
- Run-rate ingênuo — tooltip/texto fixo na tela.
