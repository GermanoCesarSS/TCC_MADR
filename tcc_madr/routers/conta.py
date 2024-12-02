from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from tcc_madr.conn_database import get_session
from tcc_madr.models import Conta
from tcc_madr.schemas import ContaPublic, ContaSchema
from tcc_madr.security import get_password_hash

router = APIRouter(prefix='/conta', tags=['conta'])

T_Session = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=ContaPublic)
def post_conta(_conta: ContaSchema, session: T_Session):
    db_user = session.scalar(
        select(Conta).where(
            (Conta.username == _conta.username) | (Conta.email == _conta.email)
        )
    )

    if db_user:
        if db_user.username == _conta.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username ja existe',
            )
        elif db_user.email == _conta.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email ja existe',
            )

    db_conta = Conta(
        username=_conta.username,
        email=_conta.email,
        senha=get_password_hash(_conta.senha),
    )
    session.add(db_conta)
    session.commit()
    session.refresh(db_conta)

    return db_conta
