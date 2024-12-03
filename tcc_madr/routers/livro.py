from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from tcc_madr.conn_database import get_session
from tcc_madr.models import Conta, Livro
from tcc_madr.schemas.schema_livro import LivroPublic, LivroSchema
from tcc_madr.security import get_current_user

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentConta = Annotated[Conta, Depends(get_current_user)]

router = APIRouter(prefix='/livro', tags=['livro'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=LivroPublic)
def asfasfa(
    current_conta: T_CurrentConta,
    _livro: LivroSchema,
    session: T_Session,
):
    db_livro = session.scalar(
        select(Livro).where(Livro.titulo == _livro.titulo)
    )

    if db_livro:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Esse titulo ja existe!',
        )

    db_livro = Livro(
        ano=_livro.ano,
        titulo=_livro.titulo,
        romancista_id=_livro.romancista_id,
    )

    session.add(db_livro)
    session.commit()
    session.refresh(db_livro)

    return db_livro
