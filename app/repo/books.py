from app.db.database import async_session
from app.db.models import Books
from app.repo.base import BaseRepo

from sqlalchemy import update


class BookRepo(BaseRepo):
    model = Books


