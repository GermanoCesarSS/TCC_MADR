import re


def sanitize_input(input_str: str) -> str:
    """
    Sanitiza a string de entrada de acordo com as regras definidas:
    - Converte para minúsculas.
    - Remove espaços extras.
    - Remove pontuações indesejadas.
    Args:
        input_str (str): A string a ser sanitizada.
    Returns:
        str: A string sanitizada.
    """

    # Converter para minúsculas
    sanitized = input_str.lower()

    # Remover espaços extras no início e no fim
    sanitized = sanitized.strip()

    # Substituir múltiplos espaços por um único espaço
    sanitized = re.sub(r'\s+', ' ', sanitized)

    # Remover pontuações (mantendo caracteres acentuados e espaços)
    # sanitized = re.sub(r'[^\w\sÀ-ÿ]', '', sanitized)
    # Remover pontuações (excluindo letras, números,
    # espaços e caracteres acentuados)
    # A expressão [^A-Za-z0-9\sÀ-ÿ] remove tudo que não for
    # letra, número, espaço ou acentuado
    sanitized = re.sub(r'[^A-Za-z0-9\sÀ-ÿ]', '', sanitized)

    return sanitized
