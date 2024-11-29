from http import HTTPStatus

from fastapi.testclient import TestClient

from tcc_madr.app import app

client = TestClient(app)


def test_ola_mundo():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}
