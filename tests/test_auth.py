from http import HTTPStatus

from freezegun import freeze_time


def test_get_token(client, conta):
    response = client.post(
        '/auth/token/',
        data={
            'username': conta.email,
            'password': conta.clean_senha,
        },
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token  # token[access_token]


def test_token_expired_after_time(client, conta):
    with freeze_time('2024-11-26 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': conta.email, 'password': conta.clean_senha},
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2024-11-26 13:31:00'):
        response = client.delete(
            f'/conta/{conta.id}', headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_invalid_password(client, conta):
    response = client.post(
        '/auth/token',
        data={'username': conta.email, 'password': 'senha_muito-segura'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email ou senha errado'}


def test_token_invalid_email(client, conta):
    response = client.post(
        '/auth/token',
        data={'username': 'email@teste.com', 'password': conta.clean_senha},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email ou senha errado'}


def test_refresh_token(client, token):
    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


def test_token_expired_dont_refresh(client, conta):
    with freeze_time('2024-11-26 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': conta.email, 'password': conta.clean_senha},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2024-11-26 13:31:00'):
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
