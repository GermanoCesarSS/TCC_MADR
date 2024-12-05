import re
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from tcc_madr.conn_database import get_session
from tcc_madr.models import Conta
from tcc_madr.security import get_current_user

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentConta = Annotated[Conta, Depends(get_current_user)]
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


def sanitize_input(texto: str) -> str:
    # Converter para minúsculas
    sanitized = texto.lower()

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


def sanitize_input_up(texto: str) -> str:
    # Remover espaços extras no início e no fim
    sanitized = texto.strip()

    # Substituir múltiplos espaços por um único espaço
    sanitized = re.sub(r'\s+', ' ', sanitized)

    # Remover pontuações (mantendo caracteres acentuados e espaços)
    # sanitized = re.sub(r'[^\w\sÀ-ÿ]', '', sanitized)
    # Remover pontuações (excluindo letras, números,
    # espaços e caracteres acentuados)
    # A expressão [^A-Za-z0-9\sÀ-ÿ] remove tudo que não for
    # letra, número, espaço ou acentuado
    sanitized = re.sub(r'[^A-Za-z0-9\sÀ-ÿ]', '', sanitized)

    # Tornar a primeira letra de cada palavra maiúscula
    sanitized = sanitized.title()

    return sanitized
