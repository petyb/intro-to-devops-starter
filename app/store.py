from __future__ import annotations

from threading import Lock
from typing import Optional, Protocol

from .models import Fruit, FruitCreate, FruitUpdate, utcnow


class Store(Protocol):
    def list(self, in_season: Optional[bool] = None) -> list[Fruit]: ...
    def get(self, fruit_id: int) -> Optional[Fruit]: ...
    def cheapest(self) -> Optional[Fruit]: ...
    def create(self, data: FruitCreate) -> Fruit: ...
    def update(self, fruit_id: int, data: FruitUpdate) -> Optional[Fruit]: ...
    def delete(self, fruit_id: int) -> bool: ...
    def reset(self) -> None: ...


class InMemoryStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._next_id = 1
        self._fruits: dict[int, Fruit] = {}

    def list(self, in_season: Optional[bool] = None) -> list[Fruit]:
        with self._lock:
            items = list(self._fruits.values())
        if in_season is None:
            return items
        return [f for f in items if f.in_season is in_season]

    def get(self, fruit_id: int) -> Optional[Fruit]:
        with self._lock:
            return self._fruits.get(fruit_id)

    def cheapest(self) -> Optional[Fruit]:
        with self._lock:
            items = list(self._fruits.values())
        if not items:
            return None
        return min(items, key=lambda f: f.price)

    def create(self, data: FruitCreate) -> Fruit:
        with self._lock:
            fruit = Fruit(
                id=self._next_id,
                created_at=utcnow(),
                **data.model_dump(),
            )
            self._fruits[fruit.id] = fruit
            self._next_id += 1
            return fruit

    def update(self, fruit_id: int, data: FruitUpdate) -> Optional[Fruit]:
        with self._lock:
            existing = self._fruits.get(fruit_id)
            if existing is None:
                return None
            patch = data.model_dump(exclude_unset=True)
            updated = existing.model_copy(update=patch)
            self._fruits[fruit_id] = updated
            return updated

    def delete(self, fruit_id: int) -> bool:
        with self._lock:
            return self._fruits.pop(fruit_id, None) is not None

    def reset(self) -> None:
        with self._lock:
            self._fruits.clear()
            self._next_id = 1


_store: Store = InMemoryStore()


def get_store() -> Store:
    return _store
