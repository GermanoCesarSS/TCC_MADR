from http import HTTPStatus

from fastapi import APIRouter

from tcc_madr.models import RomancistasLivrosView
from tcc_madr.schemas.schema_romancistas_livro import RomancistasLivrosViewList
from tcc_madr.utils import T_CurrentConta, T_Session, sanitize_input_up

router = APIRouter(
    prefix='/romancistas_livro_view', tags=['romancistas_livro_view']
)


@router.get(
    '/', status_code=HTTPStatus.OK, response_model=RomancistasLivrosViewList
)
def romancistas_livro_view_get_all(
    current_conta: T_CurrentConta,
    session: T_Session,
    romancista_nome: str | None = None,
    limit: int = 20,
    skip: int = 0,
):
    query = session.query(RomancistasLivrosView)

    if romancista_nome is not None:
        romancista_nome = sanitize_input_up(romancista_nome)
        query = query.filter(
            RomancistasLivrosView.romancista_nome.ilike(f'%{romancista_nome}%')
        )

    query = query.limit(limit).offset(skip)
    _db = query.all()

    return {'romancistas_livro_view': _db}
