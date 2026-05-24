from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status

from .models import Fruit, FruitCreate, FruitUpdate
from .store import Store, get_store

app = FastAPI(title="FruitAPI", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/fruits", response_model=list[Fruit])
def list_fruits(
    in_season: Optional[bool] = None,
    store: Store = Depends(get_store),
) -> list[Fruit]:
    return store.list(in_season=in_season)


@app.get("/fruits/cheapest", response_model=Fruit)
def cheapest_fruit(store: Store = Depends(get_store)) -> Fruit:
    fruit = store.cheapest()
    if fruit is None:
        raise HTTPException(status_code=404, detail="no fruits")
    return fruit


@app.get("/fruits/{fruit_id}", response_model=Fruit)
def get_fruit(fruit_id: int, store: Store = Depends(get_store)) -> Fruit:
    fruit = store.get(fruit_id)
    if fruit is None:
        raise HTTPException(status_code=404, detail="fruit not found")
    return fruit


@app.post("/fruits", response_model=Fruit, status_code=status.HTTP_201_CREATED)
def create_fruit(payload: FruitCreate, store: Store = Depends(get_store)) -> Fruit:
    return store.create(payload)


@app.put("/fruits/{fruit_id}", response_model=Fruit)
def update_fruit(
    fruit_id: int, payload: FruitUpdate, store: Store = Depends(get_store)
) -> Fruit:
    fruit = store.update(fruit_id, payload)
    if fruit is None:
        raise HTTPException(status_code=404, detail="fruit not found")
    return fruit


@app.delete("/fruits/{fruit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fruit(fruit_id: int, store: Store = Depends(get_store)) -> None:
    if not store.delete(fruit_id):
        raise HTTPException(status_code=404, detail="fruit not found")
    return None
