import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.store import get_store


@pytest.fixture
def client() -> TestClient:
    get_store().reset()
    return TestClient(app)


@pytest.fixture
def seeded_client(client: TestClient) -> TestClient:
    fruits = [
        {"name": "apple", "price": 1.5, "in_season": True},
        {"name": "banana", "price": 0.5, "in_season": False},
        {"name": "cherry", "price": 4.0, "in_season": True},
    ]
    for f in fruits:
        r = client.post("/fruits", json=f)
        assert r.status_code == 201
    return client
