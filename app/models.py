from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class FruitBase(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    price: float = Field(ge=0)
    in_season: bool = False


class FruitCreate(FruitBase):
    pass


class FruitUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=64)
    price: Optional[float] = Field(default=None, ge=0)
    in_season: Optional[bool] = None


class Fruit(FruitBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


def utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)
