from http import HTTPStatus


def test_conta_schema(client, create_conta_all):
    create_conta_all(9)
    response = client.post(
        '/conta/',
        json={
            'username': 'fausto',
            'email': 'fausto@fausto.com',
            'senha': '1234567',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 10,
        'email': 'fausto@fausto.com',
        'username': 'fausto',
    }
