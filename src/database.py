"""Camada de conexão e execução de queries somente leitura no PostgreSQL."""

import os
import re
from logging import getLogger

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, URL
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

logger = getLogger(__name__)

_WRITE_KEYWORDS = (
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "GRANT",
    "REVOKE",
    "MERGE",
)
_WRITE_PATTERN = re.compile(
    r"\b(" + "|".join(_WRITE_KEYWORDS) + r")\b", flags=re.IGNORECASE
)


class DatabaseConnectionError(Exception):
    """Erro amigável de conexão/execução, sem detalhes sensíveis do banco."""


def _get_credential(key: str) -> str:
    try:
        if key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    value = os.getenv(key)
    if not value:
        raise DatabaseConnectionError(
            "Configuração de banco de dados ausente. Verifique as variáveis de "
            "ambiente da aplicação."
        )
    return value


def _assert_read_only(sql: str) -> None:
    if _WRITE_PATTERN.search(sql):
        raise ValueError(
            "Consulta rejeitada: apenas instruções de leitura (SELECT) são permitidas."
        )


@st.cache_resource
def get_engine() -> Engine:
    try:
        host = _get_credential("DB_HOST")
        port = _get_credential("DB_PORT")
        name = _get_credential("DB_NAME")
        user = _get_credential("DB_USER")
        password = _get_credential("DB_PASSWORD")
    except DatabaseConnectionError:
        raise
    except Exception as exc:
        logger.error("Falha ao carregar credenciais de banco de dados: %s", exc)
        raise DatabaseConnectionError(
            "Não foi possível carregar a configuração de conexão com o banco de dados."
        ) from exc

    url = URL.create(
        "postgresql+psycopg2",
        username=user,
        password=password,
        host=host,
        port=int(port),
        database=name,
    )
    return create_engine(url, pool_pre_ping=True).execution_options(
        postgresql_readonly=True
    )


def run_query(sql: str, params: dict | None = None) -> pd.DataFrame:
    """Executa uma query somente leitura e retorna o resultado como DataFrame."""
    _assert_read_only(sql)
    try:
        engine = get_engine()
        return pd.read_sql(text(sql), engine, params=params or {})
    except DatabaseConnectionError:
        raise
    except SQLAlchemyError as exc:
        logger.error("Erro ao executar consulta no banco de dados: %s", exc)
        raise DatabaseConnectionError(
            "Não foi possível conectar ao banco de dados no momento. Tente novamente "
            "em instantes."
        ) from exc
