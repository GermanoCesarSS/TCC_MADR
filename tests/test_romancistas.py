from http import HTTPStatus

from tcc_madr.schemas.schema_romancistas import RomancistasPublic
from tests.conftest import RomancistasFactory


def test_romancistas_post_name_conflit(session, client, token):
    _romancistas = RomancistasFactory()
    session.add(_romancistas)
    session.commit()
    session.refresh(_romancistas)
    response = client.post(
        '/romancistas',
        headers={'Authorization': f'Bearer {token}'},
        json={'nome': _romancistas.nome},
    )
    assert response.json() == {'detail': 'romancista já consta no MADR'}
    assert response.status_code == HTTPStatus.CONFLICT


def test_romancistas_post(session, client, token):
    session.bulk_save_objects(RomancistasFactory.create_batch(41))
    response = client.post(
        '/romancistas',
        headers={'Authorization': f'Bearer {token}'},
        json={'nome': 'clarice lispector'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 42, 'nome': 'Clarice Lispector'}


def test_romancistas_delete_not_found(client, token):
    response = client.delete(
        '/romancistas/369',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_romancistas_delete(session, client, token):
    _romancistas = RomancistasFactory()
    session.add(_romancistas)
    session.commit()
    session.refresh(_romancistas)
    response = client.delete(
        f'/romancistas/{_romancistas.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Romancista deletada no MADR'}


def test_romancistas_patch_not_found(client, token):
    response = client.patch(
        '/romancistas/369',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'nome': 'teste',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_romancistas_patch_conflit(session, client, token):
    _romancistas = RomancistasFactory()
    session.add(_romancistas)
    session.commit()
    session.refresh(_romancistas)

    response = client.patch(
        f'/romancistas/{_romancistas.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'nome': _romancistas.nome},
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'romancista já consta no MADR'}


def test_romancistas_patch(session, client, token):
    session.bulk_save_objects(RomancistasFactory.create_batch(41))
    _romancistas = RomancistasFactory()
    session.add(_romancistas)
    session.commit()
    session.refresh(_romancistas)

    response = client.patch(
        f'/romancistas/{_romancistas.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'nome': 'clarice  l_ispector '},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': _romancistas.id,
        'nome': 'Clarice Lispector',
    }


def test_romancistas_get_not_found(client, token):
    response = client.get(
        '/romancistas/369', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_romancistas_get(session, client, token):
    _romancistas = RomancistasFactory(nome='machado de assis')
    session.add(_romancistas)
    session.commit()
    session.refresh(_romancistas)
    response = client.get(
        f'/romancistas/{_romancistas.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': 1, 'nome': 'Machado De Assis'}


def test_romancistas_get_all_nulo(client, token):
    response = client.get(
        '/romancistas/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'romancistas': []}


def test_romancistas_get_all(session, client, token):
    _romancistas = RomancistasFactory()
    session.add(_romancistas)
    session.commit()
    session.refresh(_romancistas)
    response = client.get(
        '/romancistas/', headers={'Authorization': f'Bearer {token}'}
    )
    romancistas_schema = RomancistasPublic.model_validate(
        _romancistas
    ).model_dump()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'romancistas': [romancistas_schema]}


def test_romancistas_get_filter_nome(session, client, token):
    _romancistas1 = RomancistasFactory(nome='machado de assis')
    _romancistas2 = RomancistasFactory(nome='clarice lispector')
    _romancistas3 = RomancistasFactory(nome='josé de alencar')
    _romancistas4 = RomancistasFactory(nome='E')
    session.add(_romancistas1)
    session.add(_romancistas2)
    session.add(_romancistas3)
    session.add(_romancistas4)
    session.commit()
    response = client.get(
        '/romancistas/?nome=a', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'romancistas': [
            {'nome': 'Machado De Assis', 'id': 1},
            {'nome': 'Clarice Lispector', 'id': 2},
            {'nome': 'José De Alencar', 'id': 3},
        ]
    }
