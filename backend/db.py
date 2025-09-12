from typing import Annotated, Any
from collections.abc import AsyncGenerator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from backend.repository import queries
from fastapi import Depends
from backend.config import (
    POSTGRES_USERNAME,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DATABASE,
    POSTGRES_SSLMODE,
)


class PostgresDatabase:
    url: str
    engine: AsyncEngine

    def __init__(self) -> None:
        self.url = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}?ssl={POSTGRES_SSLMODE}"
        self.engine = create_async_engine(url=self.url)


database: PostgresDatabase = PostgresDatabase()


async def get_store() -> AsyncGenerator[Any, Any]:
    async with database.engine.begin() as conn:
        _store = queries.AsyncQuerier(conn=conn)
        yield _store


async def get_health() -> AsyncGenerator[Any, Any]:
    async with database.engine.begin() as conn:
        try:
            await conn.execute(text("SELECT 1"))
            yield True
        except Exception:
            yield False


Store = Annotated[queries.AsyncQuerier, Depends(get_store)]
Healthcheck = Annotated[bool, Depends(get_health)]
