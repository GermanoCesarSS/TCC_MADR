from http import HTTPStatus

from tcc_madr.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)


def test_password():
    passoword_hash = get_password_hash('teste')
    valida = verify_password('teste', passoword_hash)
    assert valida is True


def test_jwt_invalid_token(client):
    response = client.post(
        '/auth/refresh_token', headers={'Authorization': 'Bearer'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_credentials_exception_email__exercicio(client):
    token = create_access_token({})

    response = client.delete(
        '/conta/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_credentials_exception_user__exercicio(client):
    data = {'sub': '666@test.com'}
    token = create_access_token(data)

    response = client.delete(
        '/conta/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
