# Design — Análise Comercial

## Visão geral da solução

Página Streamlit com ranking de vendedores, ticket médio, modelos mais vendidos e desconto médio, filtros por concessionária e período. Nota explícita de que funil e pátio estão fora de escopo.

## Referência de dados

- **`docs/notas-banco.md`** — join comercial, fórmula de desconto, distribuição de modelos, snapshot de `valor_pago` vs `veiculos.valor`.

## Dados utilizados

`vendas` + `vendedores` + `veiculos` + `concessionarias` (joins em `notas-banco.md`).

| Métrica | Cálculo |
|---------|---------|
| Desconto unitário | `veiculos.valor - vendas.valor_pago` |
| Desconto médio | `AVG(veiculos.valor - vendas.valor_pago)` no SQL |
| Desconto % | `(valor - valor_pago) / NULLIF(valor, 0)` |
| Modelo | `veiculos.nome` (8 modelos no catálogo atual) |

Não usar views analíticas nem inferir funil a partir de `clientes` ou views de staging.

## Fluxo

Filtros (concessionária opcional + período com default alinhado a `notas-banco.md`) → queries agregadas → cache (15–20 min) → tabelas/gráficos Plotly.

## Decisões Técnicas

- Ranking: `st.dataframe` ordenável ou barras horizontais por faturamento/quantidade.
- Desconto: exibir média em R$ e %; **não ocultar** linhas com desconto negativo (venda acima da tabela) — spec Fernanda; snapshot atual só tem vendas abaixo da tabela, mas o código deve tratar ambos.
- Modelos mais vendidos: `GROUP BY veiculos.nome` + gráfico de participação (barras ou pizza).
- Comparação Rio vs POA (e demais): usar `cidades.cidade` / `estados.sigla` via join em `concessionarias` quando comparar unidades entre regiões.
- Nota fixa na página: funil e pátio indisponíveis (sem colunas/tabelas — ver diagrama e `notas-banco.md`).

## Riscos / pontos em aberto

- `veiculos.valor` sem histórico: desconto de vendas antigas usa tabela atual (diagrama + `notas-banco.md`).
- Poucos modelos (8) concentram vendas — gráficos podem parecer desbalanceados; isso é dado real, não bug.
