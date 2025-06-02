from sqlalchemy import select

from app.db.database import async_session
from app.db.models import Readers
from app.repo.base import BaseRepo

from sqlalchemy.orm import joinedload

class ReaderRepo(BaseRepo):
    model = Readers

    @classmethod
    async def get_one_or_none(cls, **filters):
        async with async_session() as session:
            query = select(cls.model).options(joinedload(cls.model.borrowed_books)).filter_by(**filters)
            result = await session.execute(query)
            return result.scalar()