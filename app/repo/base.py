
from sqlalchemy import select, delete, update

from app.db.database import async_session


class BaseRepo:
    model = None

    @classmethod
    async def get_all(cls, **filters):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filters)
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

    @classmethod
    async def update(cls, obj_id: str, data: dict):
        async with async_session() as session:
            query = (
                update(cls.model)
                .where(cls.model.uuid == obj_id)
                .values(**data)
                .returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()

    @classmethod
    async def delete(cls, **obj):
        async with async_session() as session:
            query = delete(cls.model).filter_by(**obj).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()