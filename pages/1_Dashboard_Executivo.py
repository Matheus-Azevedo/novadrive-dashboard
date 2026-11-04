"""Dashboard Executivo (spec 02) — visão de vendas para o CEO."""

import calendar
from datetime import date

import plotly.express as px
import streamlit as st

from src.database import DatabaseConnectionError
from src.formatacao import formatar_moeda
from src.projecao import calcular_run_rate
from src.queries import (
    evolucao_diaria_periodo,
    faturamento_por_cidade_periodo,
    faturamento_por_estado_periodo,
    resumo_vendas_periodo,
    vendas_por_concessionaria_periodo,
)

st.set_page_config(page_title="NovaDrive — Dashboard Executivo", layout="wide")
st.title("Dashboard Executivo")

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
    resumo = resumo_vendas_periodo(data_inicio, data_fim)
    evolucao = evolucao_diaria_periodo(data_inicio, data_fim)
    por_concessionaria = vendas_por_concessionaria_periodo(data_inicio, data_fim)
    por_estado = faturamento_por_estado_periodo(data_inicio, data_fim)
    por_cidade = faturamento_por_cidade_periodo(data_inicio, data_fim)
except DatabaseConnectionError as exc:
    st.error(str(exc))
    st.stop()

faturamento_total = float(resumo["faturamento_total"].iloc[0])
quantidade_total = int(resumo["quantidade"].iloc[0])
ticket_medio = float(resumo["ticket_medio"].iloc[0])

col1, col2, col3 = st.columns(3)
col1.metric("Faturamento total", formatar_moeda(faturamento_total))
col2.metric("Veículos vendidos", quantidade_total)
col3.metric("Ticket médio", formatar_moeda(ticket_medio))

if data_inicio.year == hoje.year and data_inicio.month == hoje.month:
    try:
        resumo_mes = resumo_vendas_periodo(inicio_mes_atual, hoje)
        valor_mtd = float(resumo_mes["faturamento_total"].iloc[0])
        dias_no_mes = calendar.monthrange(hoje.year, hoje.month)[1]
        run_rate = calcular_run_rate(valor_mtd, hoje.day, dias_no_mes)
        st.metric(
            "Projeção de fechamento do mês",
            formatar_moeda(run_rate),
            help=(
                "Estimativa simples de run-rate (ritmo de vendas até hoje "
                "projetado para o mês inteiro) — não é previsão estatística."
            ),
        )
    except DatabaseConnectionError as exc:
        st.warning(f"Não foi possível calcular a projeção: {exc}")

st.subheader("Evolução no período")
metrica_evolucao = st.radio(
    "Métrica",
    ["Faturamento", "Quantidade"],
    horizontal=True,
    label_visibility="collapsed",
)
if evolucao.empty:
    st.info("Nenhuma venda no período selecionado.")
else:
    coluna = "faturamento" if metrica_evolucao == "Faturamento" else "quantidade"
    fig_evolucao = px.line(evolucao, x="dia", y=coluna, markers=True)
    st.plotly_chart(fig_evolucao, use_container_width=True)

st.subheader("Comparação entre concessionárias")
fig_concessionarias = px.bar(
    por_concessionaria,
    x="concessionaria",
    y="faturamento",
    hover_data=["quantidade"],
    labels={"concessionaria": "Concessionária", "faturamento": "Faturamento (R$)"},
)
st.plotly_chart(fig_concessionarias, use_container_width=True)

tab_estado, tab_cidade = st.tabs(["Por estado", "Por cidade"])
with tab_estado:
    if por_estado.empty:
        st.info("Nenhuma venda no período selecionado.")
    else:
        fig_estados = px.bar(
            por_estado,
            x="estado",
            y="faturamento",
            hover_data=["quantidade", "sigla"],
            labels={"estado": "Estado", "faturamento": "Faturamento (R$)"},
        )
        st.plotly_chart(fig_estados, use_container_width=True)
with tab_cidade:
    if por_cidade.empty:
        st.info("Nenhuma venda no período selecionado.")
    else:
        por_cidade_rotulo = por_cidade.assign(
            label=por_cidade["cidade"] + " (" + por_cidade["sigla"] + ")"
        )
        fig_cidades = px.bar(
            por_cidade_rotulo,
            x="label",
            y="faturamento",
            hover_data=["quantidade"],
            labels={"label": "Cidade", "faturamento": "Faturamento (R$)"},
        )
        st.plotly_chart(fig_cidades, use_container_width=True)
