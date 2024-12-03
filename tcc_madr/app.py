from http import HTTPStatus

from fastapi import FastAPI

from tcc_madr.routers import auth, conta, livro, romancistas
from tcc_madr.schemas.schema import Message

app = FastAPI()
app.include_router(conta.router)
app.include_router(auth.router)
app.include_router(livro.router)
app.include_router(romancistas.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}
