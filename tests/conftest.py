import pytest
from fastapi.testclient import TestClient

from tcc_madr.app import app


@pytest.fixture
def client():
    return TestClient(app)
