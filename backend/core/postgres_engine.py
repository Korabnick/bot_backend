from typing import AsyncGenerator, Union

from fastapi import Depends
from sqlalchemy import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from backend.core.config import settings
from backend.core.postgres import DBWork


def create_engine() -> AsyncEngine:
    return create_async_engine(
        settings.DB_URL,
        poolclass=AsyncAdaptedQueuePool,
        connect_args={
            'statement_cache_size': 0,
        },
    )


def create_session(engine: Union[AsyncEngine, None] = None) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine or create_engine(),
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )


engine = create_engine()
async_session = create_session(engine)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_db_work(session: AsyncSession = Depends(get_session)) -> DBWork:
    return DBWork(session)
