from __future__ import annotations

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
)
from sqlalchemy.engine import Engine

metadata = MetaData()

fruits_table = Table(
    "fruits",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(64), nullable=False),
    Column("price", Float, nullable=False),
    Column("in_season", Boolean, nullable=False, default=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
)


def make_engine(database_url: str) -> Engine:
    return create_engine(database_url, pool_pre_ping=True, future=True)


def init_schema(engine: Engine) -> None:
    metadata.create_all(engine)
