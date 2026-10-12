import pytest
from fastapi.testclient import TestClient

from orders_api.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def ana():
    return {"Authorization": "Bearer token-ana"}


@pytest.fixture
def bruno():
    return {"Authorization": "Bearer token-bruno"}
