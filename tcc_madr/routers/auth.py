from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from tcc_madr.conn_database import get_session
from tcc_madr.models import Conta
from tcc_madr.schemas.schema_conta import Token
from tcc_madr.security import (
    create_access_token,
    get_current_user,
    verify_password,
)

router = APIRouter(prefix='/auth', tags=['auth'])


T_Session = Annotated[Session, Depends(get_session)]
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token/', response_model=Token)
def login_for_access_token(
    form_data: T_OAuth2Form,
    session: T_Session,
):
    _conta = session.scalar(
        select(Conta).where(Conta.email == form_data.username)
    )

    if not _conta or not verify_password(form_data.password, _conta.senha):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Email ou senha errado'
        )
    access_token = create_access_token(data={'sub': _conta.email})
    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.post('/refresh_token', response_model=Token)
def refresh_access_token(conta: Conta = Depends(get_current_user)):
    new_access_token = create_access_token(data={'sub': conta.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}
