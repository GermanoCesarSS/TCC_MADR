from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from tcc_madr.conn_database import get_session
from tcc_madr.models import Conta
from tcc_madr.schemas.schema import Message
from tcc_madr.schemas.schema_conta import ContaList, ContaPublic, ContaSchema
from tcc_madr.security import get_current_user, get_password_hash

router = APIRouter(prefix='/conta', tags=['conta'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentConta = Annotated[Conta, Depends(get_current_user)]


@router.get('/', response_model=ContaList)
def get_conta(
    session: T_Session,
    current_conta: T_CurrentConta,
    limit: int = 10,
    skip: int = 0,
):
    db_conta = session.scalars(select(Conta).limit(limit).offset(skip))
    return {'contas': db_conta}


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


@router.put(
    '/{conta_id}', status_code=HTTPStatus.CREATED, response_model=ContaPublic
)
def put_conta(
    conta_id: int,
    _conta: ContaSchema,
    session: T_Session,
    current_conta: T_CurrentConta,
):
    if current_conta.id != conta_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Sem permisao para esse usuario',
        )

    current_conta.username = _conta.username
    current_conta.email = _conta.email
    current_conta.senha = get_password_hash(_conta.senha)

    try:
        session.commit()
        session.refresh(current_conta)
        return current_conta

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username ou Email ja existe',
        )


@router.delete('/{conta_id}', response_model=Message)
def delete_conta(
    conta_id: int, current_conta: T_CurrentConta, session: T_Session
):
    if current_conta.id != conta_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Sem permisao para excluir esse usuario',
        )

    session.delete(current_conta)
    session.commit()

    return {'message': 'Conta deletada com sucesso'}
