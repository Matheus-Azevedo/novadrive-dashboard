import inspect
import re

from src import queries

_WRITE_PATTERN = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|CREATE|GRANT|REVOKE|MERGE)\b",
    flags=re.IGNORECASE,
)

_SQL_CONSTANTS = [
    value
    for name, value in vars(queries).items()
    if name.isupper() and isinstance(value, str)
]


def test_no_query_constant_contains_write_sql():
    assert _SQL_CONSTANTS, "nenhuma constante de SQL encontrada em src/queries.py"
    for sql in _SQL_CONSTANTS:
        assert not _WRITE_PATTERN.search(sql), f"SQL de escrita encontrado: {sql!r}"


def test_no_query_function_contains_write_sql():
    for name, func in inspect.getmembers(queries, inspect.isfunction):
        source = inspect.getsource(func)
        assert not _WRITE_PATTERN.search(source), (
            f"possível SQL de escrita na função {name}"
        )


def test_queries_touching_vendas_filter_by_data_venda():
    for sql in _SQL_CONSTANTS:
        if re.search(r"\bvendas\b", sql, flags=re.IGNORECASE):
            assert "data_venda BETWEEN" in sql, (
                f"consulta em `vendas` sem filtro de período: {sql!r}"
            )
