import pytest

from src.database import _assert_read_only

WRITE_QUERIES = [
    "INSERT INTO vendas (valor_pago) VALUES (10)",
    "UPDATE vendas SET valor_pago = 0",
    "DELETE FROM vendas",
    "DROP TABLE vendas",
    "ALTER TABLE vendas ADD COLUMN x int",
    "TRUNCATE vendas",
    "CREATE TABLE x (id int)",
    "GRANT SELECT ON vendas TO someone",
    "REVOKE SELECT ON vendas FROM someone",
    "MERGE INTO vendas USING x ON true WHEN MATCHED THEN UPDATE SET valor_pago = 0",
]

READ_QUERIES = [
    "SELECT id_vendas, valor_pago FROM vendas WHERE data_venda BETWEEN :inicio AND :fim",
    "WITH totais AS (SELECT SUM(valor_pago) AS total FROM vendas) SELECT * FROM totais",
]


@pytest.mark.parametrize("sql", WRITE_QUERIES)
def test_assert_read_only_rejects_write_statements(sql):
    with pytest.raises(ValueError):
        _assert_read_only(sql)


@pytest.mark.parametrize("sql", READ_QUERIES)
def test_assert_read_only_accepts_select_statements(sql):
    _assert_read_only(sql)
