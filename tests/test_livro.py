def test_livro_post(client, token, livro):
    response = client.post(
        '/livro',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test todo',
            'description': 'Test todo description',
            'state': 'draft',
        },
    )


def test_livro_post(client, token, livro):
    response = client.post(
        '/livro',
        headers={'Authorization': f'Bearer {token}'},
        json={
                "ano": 1973,
                "titulo": "Café Da Manhã Dos Campeões",
                "romancista_id": 42
        }
    )
