import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from tcc_madr.app import app
from tcc_madr.conn_database import get_session
from tcc_madr.models import Conta, table_registry
from tcc_madr.security import get_password_hash


class ContaFactory(factory.Factory):
    class Meta:
        model = Conta

    username = factory.Sequence(lambda n: f'teste_{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@teste.com')
    senha = factory.LazyAttribute(lambda obj: f'{obj.username}senha')


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

    with Session(engine) as _session:
        yield _session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def create_conta(session):
    pwd = 'teste'
    conta = ContaFactory(senha=get_password_hash(pwd))

    session.add(conta)
    session.commit()
    session.refresh(conta)

    conta.clean_senha = pwd  # Monkey Patch

    return conta


@pytest.fixture
def create_conta_all(session):
    def _create(n: int):
        pwd = 'teste'
        contas = ContaFactory.create_batch(n, senha=get_password_hash(pwd))

        session.add_all(contas)
        session.commit()

    return _create
