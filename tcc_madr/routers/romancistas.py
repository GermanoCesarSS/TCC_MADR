from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from tcc_madr.models import Romancistas
from tcc_madr.schemas.schema import Message
from tcc_madr.schemas.schema_romancistas import (
    RomancistasList,
    RomancistasPublic,
    RomancistasSchema,
    RomancistasUpdata,
)
from tcc_madr.utils import T_CurrentConta, T_Session

router = APIRouter(prefix='/romancistas', tags=['romancistas'])


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=RomancistasPublic
)
def romancistas_post(
    current_conta: T_CurrentConta,
    _romancistas: RomancistasSchema,
    session: T_Session,
):
    db_romancistas = session.scalar(
        select(Romancistas).where(Romancistas.nome == _romancistas.nome)
    )

    if db_romancistas is not None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='romancista já consta no MADR',
        )

    db_romancistas = Romancistas(nome=_romancistas.nome)
    session.add(db_romancistas)
    session.commit()
    session.refresh(db_romancistas)

    return db_romancistas


@router.delete(
    '/{romancistas_id}', status_code=HTTPStatus.OK, response_model=Message
)
def romancistas_delete(
    romancistas_id: int,
    current_conta: T_CurrentConta,
    session: T_Session,
):
    db_romancistas = session.scalar(
        select(Romancistas).where(Romancistas.id == romancistas_id)
    )
    if not db_romancistas:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )

    session.delete(db_romancistas)
    session.commit()

    return {'message': 'Romancista deletada no MADR'}


@router.patch(
    '/{romancistas_id}',
    status_code=HTTPStatus.CREATED,
    response_model=RomancistasPublic,
)
def romancistas_patch(
    romancistas_id: int,
    new_romancistas: RomancistasUpdata,
    current_conta: T_CurrentConta,
    session: T_Session,
):
    db_romancistas = session.scalar(
        select(Romancistas).where(Romancistas.id == romancistas_id)
    )
    if not db_romancistas:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )

    if session.scalar(
        select(Romancistas).where(Romancistas.nome == new_romancistas.nome)
    ):
        raise HTTPException(
            HTTPStatus.CONFLICT,
            detail='romancista já consta no MADR',
        )

    for key, value in new_romancistas.model_dump(exclude_unset=True).items():
        setattr(db_romancistas, key, value)

    session.add(db_romancistas)
    session.commit()
    session.refresh(db_romancistas)

    return db_romancistas


@router.get(
    '/{romancistas_id}',
    response_model=RomancistasPublic,
)
def romancistas_get(
    romancistas_id: int, current_conta: T_CurrentConta, session: T_Session
):
    db_romancistas = session.scalar(
        select(Romancistas).where(Romancistas.id == romancistas_id)
    )

    if not db_romancistas:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, detail='Romancista não consta no MADR'
        )

    return db_romancistas


@router.get('/', status_code=HTTPStatus.OK, response_model=RomancistasList)
def romancistas_get_all(
    current_conta: T_CurrentConta,
    session: T_Session,
    nome: str | None = None,
    limit: int = 20,
    skip: int = 0,
):
    query = session.query(Romancistas)

    if nome is not None:
        query = query.filter(Romancistas.nome == nome)

    query = query.limit(limit).offset(skip)
    db_romancistas = query.all()

    return {'romancistas': db_romancistas}
