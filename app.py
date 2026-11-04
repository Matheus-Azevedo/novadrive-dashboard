"""Smoke test da camada de acesso a dados (spec 01). Dashboards nas specs 02/03."""

import streamlit as st
from sqlalchemy import text

from src.database import DatabaseConnectionError, get_engine

st.set_page_config(page_title="NovaDrive — Conexão")
st.title("NovaDrive Dashboard")
st.caption("Use a barra lateral para abrir o Dashboard Executivo ou a Análise Comercial.")

try:
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    st.success("Conexão com o banco de dados estabelecida com sucesso.")
except DatabaseConnectionError as exc:
    st.error(str(exc))
