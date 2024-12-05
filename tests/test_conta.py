from http import HTTPStatus

from tcc_madr.schemas.schema_conta import ContaPublic
from tests.conftest import ContaFactory

# conta post


def test_post_conta(session, client):
    session.bulk_save_objects(ContaFactory.create_batch(9))
    session.commit()

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


def test_post_conta_email_conflict(client, conta):
    response = client.post(
        '/conta/',
        json={
            'username': 'teste',
            'email': conta.email,
            'senha': 'teste',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'conta já consta no MADR'}


def test_post_conta_username_conflict(client, conta):
    response = client.post(
        '/conta/',
        json={
            'username': conta.username,
            'email': 'teste@teste.com',
            'senha': 'teste',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'conta já consta no MADR'}


# conta get


def test_get_conta(client, conta, token):
    response = client.get(
        '/conta',
        headers={'Authorization': f'Bearer {token}'},
    )
    conta_schema = ContaPublic.model_validate(conta).model_dump()

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'contas': [conta_schema]}


# conta put


def test_put_conta_username(client, conta, token):
    response = client.put(
        f'/conta/{conta.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'username': 'testusername2'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': conta.id,
        'username': 'testusername2',
        'email': conta.email,
    }


def test_put_conta(client, conta, token):
    response = client.put(
        f'/conta/{conta.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'testusername2',
            'email': 'teste@test2.com',
            'senha': '123',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': conta.id,
        'username': 'testusername2',
        'email': 'teste@test2.com',
    }


def test_put_conta_fornidden(client, other_conta, token):
    response = client.put(
        f'/conta/{other_conta.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'id': other_conta.id,
            'username': 'testusername2',
            'email': 'teste@test2.com',
            'senha': '123',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Não autorizado'}


def test_put_conta_username_conflict(client, conta, other_conta, token):
    response = client.put(
        f'/conta/{conta.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': other_conta.username,
            'email': 'teste@teste.com',
            'senha': 'teste',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'conta já consta no MADR'}


# conta delete


def test_delete_conta_fornidden(client, other_conta, token):
    response = client.delete(
        f'/conta/{other_conta.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'Sem permisao para excluir esse usuario'
    }


def test_delete_conta(client, conta, token):
    response = client.delete(
        f'/conta/{conta.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Conta deletada com sucesso'}
