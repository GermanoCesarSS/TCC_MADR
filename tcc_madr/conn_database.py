from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from tcc_madr.settings import Settings

engine = create_engine(Settings().DATABASE_URL)


# Cria sessao no banco de dados
def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
