"""Análise Comercial (spec 03) — ferramenta operacional para o time comercial."""

from datetime import date

import plotly.express as px
import streamlit as st

from src.database import DatabaseConnectionError
from src.formatacao import formatar_moeda
from src.queries import (
    comparacao_comercial_concessionarias_periodo,
    desconto_medio_por_vendedor_periodo,
    listar_concessionarias,
    modelos_mais_vendidos_periodo,
    ranking_vendedores_periodo,
)

st.set_page_config(page_title="NovaDrive — Análise Comercial", layout="wide")
st.title("Análise Comercial")
st.caption(
    "Taxa de conversão de funil e veículos parados no pátio estão fora de escopo "
    "nesta versão: o banco não possui tabela de leads/visitas nem de estoque."
)

hoje = date.today()
inicio_mes_atual = hoje.replace(day=1)

periodo = st.sidebar.date_input(
    "Período",
    value=(inicio_mes_atual, hoje),
    max_value=hoje,
)
if not isinstance(periodo, tuple) or len(periodo) != 2:
    st.sidebar.info("Selecione a data inicial e final do período.")
    st.stop()
data_inicio, data_fim = periodo
if data_fim < data_inicio:
    st.error("A data final deve ser igual ou posterior à inicial.")
    st.stop()

try:
    concessionarias = listar_concessionarias()
except DatabaseConnectionError as exc:
    st.error(str(exc))
    st.stop()

opcoes = ["Todas"] + concessionarias["concessionaria"].tolist()
concessionaria_sel = st.sidebar.selectbox("Concessionária", opcoes)
if concessionaria_sel == "Todas":
    id_concessionaria = None
else:
    id_concessionaria = int(
        concessionarias.loc[
            concessionarias["concessionaria"] == concessionaria_sel,
            "id_concessionarias",
        ].iloc[0]
    )

try:
    ranking = ranking_vendedores_periodo(data_inicio, data_fim, id_concessionaria)
    modelos = modelos_mais_vendidos_periodo(data_inicio, data_fim, id_concessionaria)
    desconto = desconto_medio_por_vendedor_periodo(
        data_inicio, data_fim, id_concessionaria
    )
    comparacao = comparacao_comercial_concessionarias_periodo(data_inicio, data_fim)
except DatabaseConnectionError as exc:
    st.error(str(exc))
    st.stop()

st.subheader("Ranking de vendedores")
ranking = ranking.copy()
ranking["ticket_medio"] = (ranking["faturamento"] / ranking["quantidade"]).where(
    ranking["quantidade"] > 0, 0
)
st.dataframe(
    ranking.assign(
        faturamento=ranking["faturamento"].map(formatar_moeda),
        ticket_medio=ranking["ticket_medio"].map(formatar_moeda),
    ),
    use_container_width=True,
    hide_index=True,
)

st.subheader("Modelos mais vendidos")
if modelos.empty:
    st.info("Nenhuma venda no período selecionado.")
else:
    fig_modelos = px.pie(
        modelos,
        values="quantidade",
        names="modelo",
        hover_data=["tipo", "faturamento"],
    )
    st.plotly_chart(fig_modelos, use_container_width=True)

st.subheader("Desconto médio por vendedor")
if desconto.empty:
    st.info("Nenhuma venda no período selecionado.")
else:
    st.dataframe(
        desconto.assign(
            desconto_medio=desconto["desconto_medio"].map(formatar_moeda),
            desconto_percentual_medio=desconto["desconto_percentual_medio"].map(
                lambda v: f"{v:.1%}"
            ),
        ),
        use_container_width=True,
        hide_index=True,
    )

st.subheader("Comparação entre concessionárias")
st.dataframe(
    comparacao.assign(
        faturamento=comparacao["faturamento"].map(formatar_moeda),
        ticket_medio=comparacao["ticket_medio"].map(formatar_moeda),
        desconto_medio=comparacao["desconto_medio"].map(formatar_moeda),
    ),
    use_container_width=True,
    hide_index=True,
)
