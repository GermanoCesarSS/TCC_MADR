from http import HTTPStatus

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
