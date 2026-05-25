from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    store_backend: str  # "memory" | "mysql"
    db_host: str | None
    db_port: int
    db_name: str
    db_user: str | None
    db_password: str | None

    @property
    def database_url(self) -> str:
        if not (self.db_host and self.db_user and self.db_password):
            raise RuntimeError(
                "MySQL backend requested but DB_HOST/DB_USER/DB_PASSWORD are not all set"
            )
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


def load_settings() -> Settings:
    return Settings(
        store_backend=os.environ.get("STORE_BACKEND", "memory").lower(),
        db_host=os.environ.get("DB_HOST"),
        db_port=int(os.environ.get("DB_PORT", "3306")),
        db_name=os.environ.get("DB_NAME", "fruitapi"),
        db_user=os.environ.get("DB_USER"),
        db_password=os.environ.get("DB_PASSWORD"),
    )
