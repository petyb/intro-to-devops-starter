from app.models import FruitCreate
from app.store import InMemoryStore


def test_response_helper_shape():
    store = InMemoryStore()
    fruit = store.create(FruitCreate(name="kiwi", price=2.0, in_season=True))
    dumped = fruit.model_dump()
    assert dumped["id"] == 1
    assert dumped["name"] == "kiwi"
    assert dumped["price"] == 2.0
    assert dumped["in_season"] is True
    assert "created_at" in dumped


def test_health_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_list_fruits_positive(seeded_client):
    r = seeded_client.get("/fruits")
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, list)
    assert len(body) == 3
    names = {f["name"] for f in body}
    assert names == {"apple", "banana", "cherry"}


def test_list_fruits_filter_in_season_true(seeded_client):
    r = seeded_client.get("/fruits", params={"in_season": "true"})
    assert r.status_code == 200
    names = {f["name"] for f in r.json()}
    assert names == {"apple", "cherry"}


def test_list_fruits_filter_in_season_false(seeded_client):
    r = seeded_client.get("/fruits", params={"in_season": "false"})
    assert r.status_code == 200
    names = {f["name"] for f in r.json()}
    assert names == {"banana"}


def test_cheapest_positive(seeded_client):
    r = seeded_client.get("/fruits/cheapest")
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "banana"
    assert body["price"] == 0.5


def test_cheapest_empty_returns_404(client):
    r = client.get("/fruits/cheapest")
    assert r.status_code == 404


def test_get_unknown_id_returns_404(client):
    r = client.get("/fruits/999")
    assert r.status_code == 404


def test_create_invalid_body_missing_name(client):
    r = client.post("/fruits", json={"price": 1.0})
    assert r.status_code == 422


def test_create_invalid_body_wrong_type(client):
    r = client.post("/fruits", json={"name": "x", "price": "free"})
    assert r.status_code == 422


def test_create_negative_price_rejected(client):
    r = client.post("/fruits", json={"name": "x", "price": -1})
    assert r.status_code == 422


def test_update_unknown_id_returns_404(client):
    r = client.put("/fruits/999", json={"price": 2.0})
    assert r.status_code == 404


def test_delete_unknown_id_returns_404(client):
    r = client.delete("/fruits/999")
    assert r.status_code == 404
