"""Projeção simples (run-rate) de fechamento do mês. Sem I/O."""


def calcular_run_rate(
    valor_vendido_ate_hoje: float, dia_do_mes: int, dias_no_mes: int
) -> float:
    """Estima fechamento do mês: valor / dias_decorridos × dias_no_mês."""
    if dia_do_mes <= 0:
        return 0.0
    return valor_vendido_ate_hoje / dia_do_mes * dias_no_mes
