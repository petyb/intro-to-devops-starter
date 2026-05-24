"""Integration tests — hit a running FruitAPI over HTTP.

Set FRUITAPI_BASE_URL to point at the target (e.g. http://localhost:8000).
If unset, the tests will be skipped — CI sets it when starting the container.
"""

from __future__ import annotations

import os
import time

import httpx
import pytest

BASE_URL = os.environ.get("FRUITAPI_BASE_URL")


pytestmark = pytest.mark.skipif(
    not BASE_URL, reason="FRUITAPI_BASE_URL not set; skipping integration tests"
)


@pytest.fixture(scope="module")
def http() -> httpx.Client:
    assert BASE_URL is not None
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as c:
        deadline = time.time() + 30
        while time.time() < deadline:
            try:
                r = c.get("/health")
                if r.status_code == 200:
                    break
            except httpx.HTTPError:
                pass
            time.sleep(0.5)
        else:
            raise RuntimeError(f"FruitAPI never became healthy at {BASE_URL}")
        yield c


def _reset(http: httpx.Client) -> None:
    for f in http.get("/fruits").json():
        http.delete(f"/fruits/{f['id']}")


def test_health(http):
    r = http.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_crud_lifecycle(http):
    _reset(http)

    r = http.post("/fruits", json={"name": "pear", "price": 2.5, "in_season": True})
    assert r.status_code == 201
    created = r.json()
    fruit_id = created["id"]
    assert created["name"] == "pear"

    r = http.get(f"/fruits/{fruit_id}")
    assert r.status_code == 200
    assert r.json()["name"] == "pear"

    r = http.put(f"/fruits/{fruit_id}", json={"price": 3.0})
    assert r.status_code == 200
    assert r.json()["price"] == 3.0

    r = http.delete(f"/fruits/{fruit_id}")
    assert r.status_code == 204

    r = http.get(f"/fruits/{fruit_id}")
    assert r.status_code == 404


def test_cheapest_matches_min_of_list(http):
    _reset(http)
    for f in [
        {"name": "a", "price": 5.0, "in_season": True},
        {"name": "b", "price": 1.25, "in_season": False},
        {"name": "c", "price": 3.0, "in_season": True},
    ]:
        assert http.post("/fruits", json=f).status_code == 201

    all_prices = [f["price"] for f in http.get("/fruits").json()]
    cheapest = http.get("/fruits/cheapest").json()
    assert cheapest["price"] == min(all_prices)


def test_post_appears_in_list(http):
    _reset(http)
    r = http.post("/fruits", json={"name": "fig", "price": 4.2, "in_season": False})
    assert r.status_code == 201
    listing = http.get("/fruits").json()
    assert any(f["name"] == "fig" for f in listing)


def test_post_empty_body_rejected(http):
    r = http.post("/fruits", json={})
    assert r.status_code == 422
