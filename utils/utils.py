import re


def only_number(value: str) -> float:
    """
    Remove todos os caracteres menos dígitos e retorna um flat

    Args:
        value (str): Valor em formato string

    Returns:
        float
    """
    result = re.sub(r"[^0-9.]", "", value)
    return float(result)
