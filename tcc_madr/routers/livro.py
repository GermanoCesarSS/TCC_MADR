from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from tcc_madr.models import Livro
from tcc_madr.schemas.schema import Message
from tcc_madr.schemas.schema_livro import (
    LivroList,
    LivroPublic,
    LivroSchema,
    LivroUpdate,
)
from tcc_madr.utils import T_CurrentConta, T_Session, sanitize_input

router = APIRouter(prefix='/livro', tags=['livro'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=LivroPublic)
def livro_post(
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
            detail='livro já consta no MADR',
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


@router.delete(
    '/{livro_id}', status_code=HTTPStatus.OK, response_model=Message
)
def livro_delete(
    livro_id: int,
    session: T_Session,
    current_conta: T_CurrentConta,
):
    db_livro = session.scalar(select(Livro).where(Livro.id == livro_id))
    if not db_livro:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, detail='Livro não consta no MADR'
        )

    session.delete(db_livro)
    session.commit()

    return {'message': 'Livro deletado no MADR'}


@router.patch(
    '/{livro_id}', status_code=HTTPStatus.CREATED, response_model=LivroPublic
)
def livro_path(
    livro_id: int,
    new_livro: LivroUpdate,
    session: T_Session,
    current_conta: T_CurrentConta,
):
    db_livro = session.scalar(select(Livro).where(Livro.id == livro_id))

    if not db_livro:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, detail='Livro não consta no MADR'
        )

    if session.scalar(select(Livro).where(Livro.titulo == new_livro.titulo)):
        raise HTTPException(
            HTTPStatus.CONFLICT, detail='livro já consta no MADR'
        )

    for key, value in new_livro.model_dump(exclude_unset=True).items():
        setattr(db_livro, key, value)

    # db_livro.titulo = sanitize_input(db_livro.titulo)
    session.add(db_livro)
    session.commit()
    session.refresh(db_livro)

    return db_livro


@router.get('/{livro_id}', response_model=LivroPublic)
def livro_get(
    session: T_Session,
    current_conta: T_CurrentConta,
    livro_id: int,
):
    db_livro = session.scalar(select(Livro).where(Livro.id == livro_id))
    if not db_livro:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Livro não consta no MADR'
        )
    return db_livro


@router.get('/', response_model=LivroList)
def livro_get_all(
    session: T_Session,
    current_conta: T_CurrentConta,
    ano: int | None = None,
    titulo: str | None = None,
    romancista_id: int | None = None,
    limit: int = 20,
    skip: int = 0,
):
    query = session.query(Livro)

    if ano is not None:
        query = query.filter(Livro.ano == ano)

    if titulo is not None:
        titulo = sanitize_input(titulo)
        query = query.filter(Livro.titulo.ilike(f'%{titulo}%'))

    if romancista_id is not None:
        query = query.filter(Livro.romancista_id == romancista_id)

    query = query.limit(limit).offset(skip)
    db_livro = query.all()

    return {'livros': db_livro}
