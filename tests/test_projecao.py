import pytest

from src.projecao import calcular_run_rate


def test_calcular_run_rate_projeta_ritmo_atual():
    assert calcular_run_rate(100, 10, 30) == pytest.approx(300)


def test_calcular_run_rate_meio_do_mes():
    assert calcular_run_rate(1000, 15, 30) == pytest.approx(2000)


def test_calcular_run_rate_dia_zero_nao_divide_por_zero():
    assert calcular_run_rate(500, 0, 30) == 0.0
