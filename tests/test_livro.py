from http import HTTPStatus

from tcc_madr.schemas.schema_livro import LivroPublic
from tcc_madr.utils import sanitize_input
from tests.conftest import LivroFactory


def test_livro_post_titulo_conflit(session, client, token):
    _titulo = 'teste'
    session.bulk_save_objects(LivroFactory.create_batch(1, titulo=_titulo))
    response = client.post(
        '/livro',
        headers={'Authorization': f'Bearer {token}'},
        json={'titulo': _titulo, 'ano': 1234, 'romancista_id': 1},
    )
    assert response.status_code == HTTPStatus.CONFLICT


def test_livro_post(session, client, token):
    session.bulk_save_objects(LivroFactory.create_batch(2))
    response = client.post(
        '/livro',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'ano': 1973,
            'titulo': 'Café Da Manhã Dos Campeões',
            'romancista_id': 42,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 3,
        'ano': 1973,
        'titulo': 'café da manhã dos campeões',
        'romancista_id': 42,
    }


def test_livro_delete_not_found(client, token):
    response = client.delete(
        '/livro/369', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro nao encontrado.'}


def test_livro_delete(session, client, token):
    _livro = LivroFactory()

    session.add(_livro)
    session.commit()
    session.refresh(_livro)

    response = client.delete(
        f'/livro/{_livro.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Livro deletado no MADR'}


def test_livro_patch_not_found(client, token):
    rs = client.patch(
        '/livro/369',
        headers={'Authorization': f'Bearer {token}'},
        json={'titulo': 'teste', 'ano': 2000, 'romancista_id': 1},
    )
    assert rs.status_code == HTTPStatus.NOT_FOUND
    assert rs.json() == {'detail': 'Livro nao encontrado.'}


def test_livro_patch_titulo_conflit(session, client, token):
    session.bulk_save_objects(LivroFactory.create_batch(2))
    response = client.patch(
        '/livro/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'titulo': 'teste2',
            'ano': 1974,
            'romancista_id': 1,
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Titulo repetido.'}


def test_livro_patch(session, client, token):
    _livro = LivroFactory(titulo='C_afé da manhã dos campeões')
    session.add(_livro)
    session.commit()
    session.refresh(_livro)

    rs = client.patch(
        f'/livro/{_livro.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'ano': 1974},
    )
    assert rs.status_code == HTTPStatus.CREATED
    assert rs.json() == {
        'ano': 1974,
        'titulo': 'café da manhã dos campeões',
        'romancista_id': 1,
    }


def test_livro_get_not_found(client, token):
    rs = client.get(
        '/livro/369',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert rs.status_code == HTTPStatus.NOT_FOUND
    assert rs.json() == {'detail': 'Livro nao encontrado.'}


def test_livro_get(session, client, token):
    _livro = LivroFactory(ano=1974, titulo='cA_fé da manhã dos campeões')
    _livro.titulo = sanitize_input(_livro.titulo)
    session.add(_livro)
    session.commit()

    rs = client.get(
        '/livro/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert rs.status_code == HTTPStatus.OK
    assert rs.json() == {
        'id': 1,
        'ano': 1974,
        'titulo': 'café da manhã dos campeões',
        'romancista_id': 1,
    }


def test_livro_get_all_null(client, token):
    rs = client.get('/livro/', headers={'Authorization': f'Bearer {token}'})
    assert rs.status_code == HTTPStatus.OK
    assert rs.json() == {'livros': []}


def test_livro_get_all(session, client, token):
    _livro = LivroFactory()
    session.add(_livro)
    session.commit()
    session.refresh(_livro)
    user_schema = LivroPublic.model_validate(_livro).model_dump()

    rs = client.get('/livro/', headers={'Authorization': f'Bearer {token}'})
    assert rs.status_code == HTTPStatus.OK
    assert rs.json() == {'livros': [user_schema]}


def test_livro_get_filter_ano(session, client, token):
    expected_livro = 2
    _ano: int = 1900

    session.bulk_save_objects(LivroFactory.create_batch(2, ano=_ano))
    _livro = LivroFactory(ano=2000)
    session.add(_livro)
    session.commit()

    response = client.get(
        f'/livro/?ano={_ano}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['livros']) == expected_livro


def test_livro_get_filter_titulo(session, client, token):
    expected_livro = 2
    _titulo = 'teste'

    session.bulk_save_objects(LivroFactory.create_batch(2))
    _livro = LivroFactory(titulo='a')
    session.add(_livro)
    session.commit()

    response = client.get(
        f'/livro/?titulo={_titulo}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['livros']) == expected_livro


def test_livro_get_filter_romancista_id(session, client, token):
    expected_livro = 2
    _romancista_id = 10

    session.bulk_save_objects(
        LivroFactory.create_batch(2, romancista_id=_romancista_id)
    )
    _livro = LivroFactory(romancista_id=2)
    session.add(_livro)
    session.commit()

    response = client.get(
        f'/livro/?romancista_id={_romancista_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['livros']) == expected_livro


def test_livro_get_filter(session, client, token):
    expected_livro = 1

    session.bulk_save_objects(
        LivroFactory.create_batch(
            4,
        )
    )
    _livro = LivroFactory(titulo='café', ano=1900, romancista_id=10)
    session.add(_livro)
    session.commit()
    session.refresh(_livro)
    livro_schema = LivroPublic.model_validate(_livro).model_dump()

    response = client.get(
        f'/livro/?titulo={_livro.titulo}&ano={_livro.ano}&romancista_id{_livro.romancista_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['livros']) == expected_livro
    assert response.json() == {'livros': [livro_schema]}
