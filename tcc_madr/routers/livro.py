from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from tcc_madr.conn_database import get_session
from tcc_madr.models import Conta
from tcc_madr.security import get_current_user

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentConta = Annotated[Conta, Depends(get_current_user)]

router = APIRouter(prefix='/livro', tags=['livro'])


@router.post()
def asfasfa(
    session: T_Session,
    current_conta: T_CurrentConta,
): ...
