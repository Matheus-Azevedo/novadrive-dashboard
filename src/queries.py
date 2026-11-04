"""Consultas agregadas base sobre `vendas`, reutilizáveis pelos dashboards."""

from datetime import date

import pandas as pd
import streamlit as st

from src.database import run_query

_RESUMO_VENDAS_SQL = """
    SELECT
        COALESCE(SUM(valor_pago), 0) AS faturamento_total,
        COUNT(*) AS quantidade,
        COALESCE(AVG(valor_pago), 0) AS ticket_medio
    FROM vendas
    WHERE data_venda BETWEEN :inicio AND :fim
"""

_EVOLUCAO_DIARIA_SQL = """
    SELECT
        DATE(data_venda) AS dia,
        SUM(valor_pago) AS faturamento,
        COUNT(*) AS quantidade
    FROM vendas
    WHERE data_venda BETWEEN :inicio AND :fim
    GROUP BY DATE(data_venda)
    ORDER BY dia
"""

_VENDAS_POR_CONCESSIONARIA_SQL = """
    SELECT
        c.concessionaria,
        COALESCE(SUM(v.valor_pago), 0) AS faturamento,
        COUNT(v.id_vendas) AS quantidade
    FROM concessionarias c
    LEFT JOIN vendas v
        ON v.id_concessionarias = c.id_concessionarias
        AND v.data_venda BETWEEN :inicio AND :fim
    GROUP BY c.concessionaria
    ORDER BY faturamento DESC
"""

_FATURAMENTO_POR_ESTADO_SQL = """
    SELECT
        e.estado,
        e.sigla,
        SUM(v.valor_pago) AS faturamento,
        COUNT(*) AS quantidade
    FROM vendas v
    JOIN concessionarias c ON c.id_concessionarias = v.id_concessionarias
    JOIN cidades ci ON ci.id_cidades = c.id_cidades
    JOIN estados e ON e.id_estados = ci.id_estados
    WHERE v.data_venda BETWEEN :inicio AND :fim
    GROUP BY e.estado, e.sigla
    ORDER BY faturamento DESC
"""

_FATURAMENTO_POR_CIDADE_SQL = """
    SELECT
        ci.cidade,
        e.sigla,
        SUM(v.valor_pago) AS faturamento,
        COUNT(*) AS quantidade
    FROM vendas v
    JOIN concessionarias c ON c.id_concessionarias = v.id_concessionarias
    JOIN cidades ci ON ci.id_cidades = c.id_cidades
    JOIN estados e ON e.id_estados = ci.id_estados
    WHERE v.data_venda BETWEEN :inicio AND :fim
    GROUP BY ci.cidade, e.sigla
    ORDER BY faturamento DESC
"""

_LISTAR_CONCESSIONARIAS_SQL = """
    SELECT id_concessionarias, concessionaria
    FROM concessionarias
    ORDER BY concessionaria
"""

_RANKING_VENDEDORES_SQL = """
    SELECT
        vd.nome AS vendedor,
        c.concessionaria,
        COALESCE(SUM(v.valor_pago), 0) AS faturamento,
        COUNT(v.id_vendas) AS quantidade
    FROM vendedores vd
    JOIN concessionarias c ON c.id_concessionarias = vd.id_concessionarias
    LEFT JOIN vendas v
        ON v.id_vendedores = vd.id_vendedores
        AND v.data_venda BETWEEN :inicio AND :fim
    WHERE (:id_concessionaria IS NULL OR vd.id_concessionarias = :id_concessionaria)
    GROUP BY vd.nome, c.concessionaria
    ORDER BY faturamento DESC
"""

_MODELOS_MAIS_VENDIDOS_SQL = """
    SELECT
        vz.nome AS modelo,
        vz.tipo,
        COUNT(v.id_vendas) AS quantidade,
        COALESCE(SUM(v.valor_pago), 0) AS faturamento
    FROM vendas v
    JOIN veiculos vz ON vz.id_veiculos = v.id_veiculos
    WHERE v.data_venda BETWEEN :inicio AND :fim
        AND (:id_concessionaria IS NULL OR v.id_concessionarias = :id_concessionaria)
    GROUP BY vz.nome, vz.tipo
    ORDER BY quantidade DESC
"""

_DESCONTO_MEDIO_POR_VENDEDOR_SQL = """
    SELECT
        vd.nome AS vendedor,
        COALESCE(AVG(vz.valor - v.valor_pago), 0) AS desconto_medio,
        COALESCE(AVG((vz.valor - v.valor_pago) / NULLIF(vz.valor, 0)), 0)
            AS desconto_percentual_medio
    FROM vendas v
    JOIN vendedores vd ON vd.id_vendedores = v.id_vendedores
    JOIN veiculos vz ON vz.id_veiculos = v.id_veiculos
    WHERE v.data_venda BETWEEN :inicio AND :fim
        AND (:id_concessionaria IS NULL OR v.id_concessionarias = :id_concessionaria)
    GROUP BY vd.nome
    ORDER BY desconto_medio DESC
"""

_COMPARACAO_COMERCIAL_CONCESSIONARIAS_SQL = """
    SELECT
        c.concessionaria,
        COALESCE(SUM(v.valor_pago), 0) AS faturamento,
        COUNT(v.id_vendas) AS quantidade,
        COALESCE(AVG(v.valor_pago), 0) AS ticket_medio,
        COALESCE(AVG(vz.valor - v.valor_pago), 0) AS desconto_medio
    FROM concessionarias c
    LEFT JOIN vendas v
        ON v.id_concessionarias = c.id_concessionarias
        AND v.data_venda BETWEEN :inicio AND :fim
    LEFT JOIN veiculos vz ON vz.id_veiculos = v.id_veiculos
    GROUP BY c.concessionaria
    ORDER BY faturamento DESC
"""


def _period_params(data_inicio: date, data_fim: date) -> dict:
    return {"inicio": data_inicio, "fim": data_fim}


@st.cache_data(ttl=60)
def resumo_vendas_periodo(data_inicio: date, data_fim: date) -> pd.DataFrame:
    """Faturamento total, quantidade e ticket médio no período."""
    return run_query(_RESUMO_VENDAS_SQL, _period_params(data_inicio, data_fim))


@st.cache_data(ttl=60)
def evolucao_diaria_periodo(data_inicio: date, data_fim: date) -> pd.DataFrame:
    """Faturamento e quantidade por dia no período."""
    return run_query(_EVOLUCAO_DIARIA_SQL, _period_params(data_inicio, data_fim))


@st.cache_data(ttl=900)
def vendas_por_concessionaria_periodo(
    data_inicio: date, data_fim: date
) -> pd.DataFrame:
    """Faturamento e quantidade por concessionária (LEFT JOIN, zero se sem vendas)."""
    return run_query(
        _VENDAS_POR_CONCESSIONARIA_SQL, _period_params(data_inicio, data_fim)
    )


@st.cache_data(ttl=900)
def faturamento_por_estado_periodo(data_inicio: date, data_fim: date) -> pd.DataFrame:
    """Faturamento e quantidade por estado (join geográfico)."""
    return run_query(
        _FATURAMENTO_POR_ESTADO_SQL, _period_params(data_inicio, data_fim)
    )


@st.cache_data(ttl=900)
def faturamento_por_cidade_periodo(data_inicio: date, data_fim: date) -> pd.DataFrame:
    """Faturamento e quantidade por cidade."""
    return run_query(
        _FATURAMENTO_POR_CIDADE_SQL, _period_params(data_inicio, data_fim)
    )


@st.cache_data(ttl=60)
def listar_concessionarias() -> pd.DataFrame:
    """Lista id e nome de concessionárias para filtros."""
    return run_query(_LISTAR_CONCESSIONARIAS_SQL)


@st.cache_data(ttl=900)
def ranking_vendedores_periodo(
    data_inicio: date, data_fim: date, id_concessionaria: int | None = None
) -> pd.DataFrame:
    """Ranking de vendedores por faturamento e quantidade."""
    return run_query(
        _RANKING_VENDEDORES_SQL,
        {
            **_period_params(data_inicio, data_fim),
            "id_concessionaria": id_concessionaria,
        },
    )


@st.cache_data(ttl=900)
def modelos_mais_vendidos_periodo(
    data_inicio: date, data_fim: date, id_concessionaria: int | None = None
) -> pd.DataFrame:
    """Modelos mais vendidos no período."""
    return run_query(
        _MODELOS_MAIS_VENDIDOS_SQL,
        {
            **_period_params(data_inicio, data_fim),
            "id_concessionaria": id_concessionaria,
        },
    )


@st.cache_data(ttl=900)
def desconto_medio_por_vendedor_periodo(
    data_inicio: date, data_fim: date, id_concessionaria: int | None = None
) -> pd.DataFrame:
    """Desconto médio (tabela − pago) por vendedor; inclui vendas acima da tabela."""
    return run_query(
        _DESCONTO_MEDIO_POR_VENDEDOR_SQL,
        {
            **_period_params(data_inicio, data_fim),
            "id_concessionaria": id_concessionaria,
        },
    )


@st.cache_data(ttl=900)
def comparacao_comercial_concessionarias_periodo(
    data_inicio: date, data_fim: date
) -> pd.DataFrame:
    """Comparação comercial entre concessionárias."""
    return run_query(
        _COMPARACAO_COMERCIAL_CONCESSIONARIAS_SQL,
        _period_params(data_inicio, data_fim),
    )
