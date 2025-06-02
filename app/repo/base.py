from multiprocessing.spawn import import_main_path

from sqlalchemy import select

from app.db.database import async_session


class BaseRepo:
    model = None

    @classmethod
    async def get_all(cls, **filters):
        async with async_session() as session:
            query = select(cls.model.filter_by(**filters))
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_one_or_none(cls, **filters):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def create(cls, data: dict):
        async with async_session() as session:
            obj = cls.model(**data)
            session.add(obj)
            await session.commit()
            return obj