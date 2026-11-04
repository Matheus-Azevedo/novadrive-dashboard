# Notas de exploração do banco (NovaDrive)

Documento de apoio às specs. **Fonte da verdade de negócio:** `specs/*/requirements.md`. **Modelo lógico:** `docs/diagrama-banco-dados.png`. Este arquivo registra o que foi validado no PostgreSQL de produção (usuário somente leitura) em nov/2026.

## Escopo de tabelas (MVP)

Usar **apenas** as 7 tabelas do diagrama:

| Tabela | Papel |
|--------|--------|
| `estados` | UF / região |
| `cidades` | Cidade → estado |
| `concessionarias` | Unidade de venda → cidade |
| `veiculos` | Catálogo (`nome`, `tipo`, `valor` tabela) |
| `clientes` | Cliente → concessionária (não usado nos KPIs principais do MVP) |
| `vendedores` | Vendedor → concessionária |
| `vendas` | Fato: `valor_pago`, `data_venda` + FKs |

### Objetos fora do escopo (não usar no dashboard)

Existem **10 views** em `public` que **não** aparecem no diagrama do curso:

`compradores`, `concessionaria_clientes`, `consulta_condicoes`, `costumer`, `lista_veiculos_compra_clientes`, `stg_costumer`, `stg_vendas`, `valores_suv_compacta`, `veiculos_mais_caros`, `vendedores_concessionarias`.

Motivo: evitar dependência de camada analítica/legacy não especificada; specs e critérios de aceite referem-se ao modelo de 7 tabelas.

## Relacionamentos (joins canônicos)

```
estados.id_estados = cidades.id_estados
cidades.id_cidades = concessionarias.id_cidades
concessionarias.id_concessionarias = vendas.id_concessionarias
concessionarias.id_concessionarias = vendedores.id_concessionarias
vendedores.id_vendedores = vendas.id_vendedores
veiculos.id_veiculos = vendas.id_veiculos
clientes.id_clientes = vendas.id_clientes
```

**Geografia (CEO — estado/cidade):**

```sql
vendas v
JOIN concessionarias c ON c.id_concessionarias = v.id_concessionarias
JOIN cidades ci ON ci.id_cidades = c.id_cidades
JOIN estados e ON e.id_estados = ci.id_estados
```

**Comercial (desconto, modelos, ranking):**

```sql
vendas v
JOIN veiculos ve ON ve.id_veiculos = v.id_veiculos
JOIN vendedores vd ON vd.id_vendedores = v.id_vendedores
JOIN concessionarias c ON c.id_concessionarias = v.id_concessionarias
```

Desconto unitário (spec Fernanda): `ve.valor - v.valor_pago` (positivo = vendido abaixo da tabela).

## Colunas críticas (filtro e métricas)

| Uso | Tabela.coluna |
|-----|----------------|
| Filtro de período (obrigatório em SQL) | `vendas.data_venda` |
| Faturamento | `SUM(vendas.valor_pago)` |
| Quantidade | `COUNT(vendas.id_vendas)` ou `COUNT(*)` |
| Ticket médio | `SUM(valor_pago) / COUNT(*)` |
| Nome da unidade | `concessionarias.concessionaria` |
| Região | `estados.estado`, `estados.sigla`, `cidades.cidade` |
| Modelo | `veiculos.nome`, `veiculos.tipo` |
| Preço tabela | `veiculos.valor` |

Tipos no servidor: valores monetários `numeric`; datas `timestamp with time zone` (compatível com filtro por intervalo).

## Snapshot dos dados (sanidade — pode mudar)

Contagens observadas na exploração:

| Entidade | Quantidade |
|----------|------------|
| `estados` | 27 |
| `cidades` | 27 |
| `concessionarias` | 29 |
| `vendedores` | 53 |
| `veiculos` (modelos distintos no catálogo) | 8 |
| `clientes` | 1433 |
| `vendas` | 1433 |

**Faixa de `data_venda`:** `2026-10-30` a `2026-11-04` (janela curta). Definir **default do filtro** na UI cobrindo esse intervalo ou “últimos 7 dias” até o `MAX(data_venda)`, para não exibir painel vazio.

**Concessionárias sem venda:** no recorte global atual, todas as 29 unidades têm pelo menos uma venda; no **período filtrado** ainda assim usar `LEFT JOIN` + `COALESCE(..., 0)` para atender Ricardo (unidade sem venda no mês = zero).

**Desconto vs tabela (join `vendas` + `veiculos`):** no snapshot, **1433** vendas com `valor_pago < valor`; **0** acima ou iguais. UI deve continuar prevendo venda acima da tabela (spec), mesmo que hoje não ocorra.

**Modelos mais vendidos (contagem):** AgileXplorer (238), ElegantCruise (236), WorkMaster (218), DoubleDuty (206), TrailConqueror (171), VoyageRoamer (163), EcoPrestige (121), SpeedFury (81).

## Implicações técnicas (CIO)

- Volume atual é modesto, mas a regra permanece: **nunca** `SELECT` em `vendas` sem `WHERE data_venda BETWEEN :inicio AND :fim`.
- Consultas com join geográfico ou comercial: cache **15–20 min**; agregados simples só em `vendas`: **~1 min**.
- Não há coluna de “lead” ou “estoque” — confirma funil e pátio fora do escopo.

## Atualização deste documento

Reexecutar contagens e `MIN`/`MAX(data_venda)` após cargas ETL ou ao validar bugs de período. Não substituir alterações de spec — apenas informar implementação.
