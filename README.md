# novadrive-dashboard

Dashboard gerencial **somente leitura** (Streamlit + PostgreSQL) — case **NovaDrive Motors**, curso Spec-Driven Development.

## Funcionalidades

- **Dashboard Executivo** — KPIs, evolução, comparação por concessionária/estado/cidade, projeção run-rate
- **Análise Comercial** — ranking de vendedores, modelos mais vendidos, desconto médio, comparação entre unidades

## Pré-requisitos

- Python 3.11+
- Acesso ao PostgreSQL do case (usuário read-only)
- Arquivo `.env` na raiz (copie de `.env.example`)

## Instalação

```bash
python3 -m venv .venv   # ou: uv venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Executar

```bash
python -m streamlit run app.py
```

Abra `http://localhost:8501` e use a barra lateral para navegar entre as páginas.

## Testes

```bash
pytest tests/
```

## Estrutura SDD

```
specs/01-acesso-dados/     # Camada read-only (fundação)
specs/02-dashboard-executivo/
specs/03-analise-comercial/
docs/diagrama-banco-dados.png
docs/notas-banco.md
AGENTS.md                  # Regras para o Cursor Agent
```

Implementação na ordem das specs acima. Detalhes de negócio em `specs/*/requirements.md`.
