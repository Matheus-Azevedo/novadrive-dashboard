"""Formatação de valores para exibição nas páginas Streamlit."""


def formatar_moeda(valor: float) -> str:
    """Moeda no padrão brasileiro (R$ 1.234,56)."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
