from __future__ import annotations

from threading import Lock
from typing import Optional, Protocol

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.engine import Engine

from .config import load_settings
from .db import fruits_table, init_schema, make_engine
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


class MySQLStore:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def _row_to_fruit(self, row) -> Fruit:
        return Fruit(
            id=row.id,
            name=row.name,
            price=row.price,
            in_season=row.in_season,
            created_at=row.created_at,
        )

    def list(self, in_season: Optional[bool] = None) -> list[Fruit]:
        stmt = select(fruits_table)
        if in_season is not None:
            stmt = stmt.where(fruits_table.c.in_season == in_season)
        with self._engine.connect() as conn:
            rows = conn.execute(stmt).all()
        return [self._row_to_fruit(r) for r in rows]

    def get(self, fruit_id: int) -> Optional[Fruit]:
        stmt = select(fruits_table).where(fruits_table.c.id == fruit_id)
        with self._engine.connect() as conn:
            row = conn.execute(stmt).first()
        return self._row_to_fruit(row) if row else None

    def cheapest(self) -> Optional[Fruit]:
        stmt = select(fruits_table).order_by(fruits_table.c.price.asc()).limit(1)
        with self._engine.connect() as conn:
            row = conn.execute(stmt).first()
        return self._row_to_fruit(row) if row else None

    def create(self, data: FruitCreate) -> Fruit:
        now = utcnow()
        with self._engine.begin() as conn:
            result = conn.execute(
                insert(fruits_table).values(
                    name=data.name,
                    price=data.price,
                    in_season=data.in_season,
                    created_at=now,
                )
            )
            new_id = result.inserted_primary_key[0]
        return Fruit(
            id=new_id,
            name=data.name,
            price=data.price,
            in_season=data.in_season,
            created_at=now,
        )

    def update(self, fruit_id: int, data: FruitUpdate) -> Optional[Fruit]:
        patch = data.model_dump(exclude_unset=True)
        if not patch:
            return self.get(fruit_id)
        with self._engine.begin() as conn:
            result = conn.execute(
                update(fruits_table)
                .where(fruits_table.c.id == fruit_id)
                .values(**patch)
            )
            if result.rowcount == 0:
                return None
        return self.get(fruit_id)

    def delete(self, fruit_id: int) -> bool:
        with self._engine.begin() as conn:
            result = conn.execute(
                delete(fruits_table).where(fruits_table.c.id == fruit_id)
            )
        return result.rowcount > 0

    def reset(self) -> None:
        with self._engine.begin() as conn:
            conn.execute(delete(fruits_table))


_store: Optional[Store] = None


def build_store() -> Store:
    settings = load_settings()
    if settings.store_backend == "mysql":
        engine = make_engine(settings.database_url)
        init_schema(engine)
        return MySQLStore(engine)
    return InMemoryStore()


def get_store() -> Store:
    global _store
    if _store is None:
        _store = build_store()
    return _store


def set_store(store: Store) -> None:
    """Test helper — swap the singleton."""
    global _store
    _store = store
