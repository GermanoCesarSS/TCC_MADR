from http import HTTPStatus


def test_ola_mundo(client):
    response = client.get(
        '/',
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'mensagem': 'Olá Mundo!'}
