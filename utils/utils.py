import re
from unidecode import unidecode


def only_number(value: str) -> float:
    """
    Remove todos os caracteres menos dígitos e retorna um float

    Args:
        value (str): Valor em formato string

    Returns:
        float
    """
    result = re.sub(r"[^0-9.]", "", value)
    return float(result)


def clean_string(my_string: str, is_description: bool=False) -> str:
    """
    Tratamento de string em situações genéricas: remoção de espaços no início
    e no final, unidecode, conversão em maiúsculas e troca dos espaços
    restantes por underline _
    Caso seja um texto de descrição, será feita a remoção de espaços no início
    e no final, remoção de tegs HTML e remoção de quebras de linha

    Args:
        value (str): Valor em formato string
        is_description (bool, optional): flag para o tratamento de descrições

    Returns:
        string formatada
    """
    my_string = my_string.strip()
    if is_description:
        clean = re.compile('<.*?>')
        my_string = re.sub(clean, '', my_string)
        my_string = ' '.join(my_string.split())
    else:
        my_string = unidecode(my_string.replace(' ', '_')).upper()

    return my_string
