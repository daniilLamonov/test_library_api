from datetime import datetime

from sqlalchemy import update, select
from sqlalchemy.exc import IntegrityError

from app.db.database import async_session
from app.db.models import Borrows
from app.repo.base import BaseRepo


class LibraryRepo(BaseRepo):
    model = Borrows

    @classmethod
    async def return_book(cls, reader_uuid: str, book_uuid: str):
        async with async_session() as session:
            subqury = (
                select(cls.model)
                .where(
                    (cls.model.reader_uuid == reader_uuid)
                    & (cls.model.book_uuid == book_uuid)
                    & (cls.model.return_date.is_(None))
                )
                .order_by(cls.model.borrow_date)
                .limit(1)
                .cte("to_update")
            )
            query = (
                update(cls.model)
                .where(cls.model.id == subqury.c.id)
                .values({"return_date": datetime.now().replace(tzinfo=None)})
                .returning(cls.model)
            )
            try:
                result = await session.execute(query)
                await session.commit()
                return result.scalar_one_or_none()
            except IntegrityError as e:
                raise e

    @classmethod
    async def get_debts(cls, reader_uuid: str):
        async with async_session() as session:
            query = (
                select(cls.model)
                .where(cls.model.return_date.is_(None))
                .filter_by(reader_uuid=reader_uuid)
            )
            result = await session.execute(query)
            return result.scalars().all()
