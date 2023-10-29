from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    AsyncEngine,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta
from config import settings


# 'postgresql://<username>:<password>@<ip-adress/hostname>:portnumber/<database_name>'
POSTGRES_DATABASE_URL: str = f"postgresql+asyncpg://{settings.db_username}:{settings.db_password}@{settings.db_hostname}/{settings.db_name}"


engine: AsyncEngine = create_async_engine(
    POSTGRES_DATABASE_URL,
    echo=True,
    future=True,
)


async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=True,
    autocommit=False,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        assert isinstance(session, AsyncSession)
        yield session


Base: DeclarativeMeta = declarative_base(cls=AsyncAttrs)


async def connect() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)
        print("database is connected successfully...")


async def disconnect() -> None:
    if engine:
        await engine.dispose()
        print("database is disconnected successfully...")
