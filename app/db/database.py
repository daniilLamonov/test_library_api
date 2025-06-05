from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core import settings

if settings.MODE == "TEST":
    database_url = settings.get_test_db_url
    database_params = {"poolclass": NullPool}
else:
    database_url = settings.get_db_url
    database_params = {}

engine = create_async_engine(database_url, **database_params)

async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    pass