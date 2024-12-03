import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from tcc_madr.app import app
from tcc_madr.conn_database import get_session
from tcc_madr.models import Conta, Livro, table_registry
from tcc_madr.security import get_password_hash


class ContaFactory(factory.Factory):
    class Meta:
        model = Conta

    username = factory.Sequence(lambda n: f'teste{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@teste.com')
    senha = factory.LazyAttribute(lambda obj: f'{obj.username}senha')


class LivroFactory(factory.Factory):
    class Meta:
        model = Livro

    titulo = factory.Sequence(lambda n: f'teste{n}')
    ano = factory.Sequence(lambda n: 2000 + n)
    romancista_id = 1


@pytest.fixture
def client(session):
    def fake_session():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = fake_session

        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    ContaFactory.reset_sequence(1)
    LivroFactory.reset_sequence(1)


@pytest.fixture
def conta(session):
    pwd = 'teste'
    conta = ContaFactory(senha=get_password_hash(pwd))

    session.add(conta)
    session.commit()
    session.refresh(conta)

    conta.clean_senha = pwd  # Monkey Patch

    return conta


@pytest.fixture
def other_conta(session):
    pwd = 'teste'
    conta = ContaFactory(senha=get_password_hash(pwd))

    session.add(conta)
    session.commit()
    session.refresh(conta)

    conta.clean_senha = pwd  # Monkey Patch

    return conta


@pytest.fixture
def token(client, conta):
    response = client.post(
        '/auth/token/',
        data={'username': conta.email, 'password': conta.clean_senha},
    )
    return response.json()['access_token']
