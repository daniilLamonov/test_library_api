from app.db.models import Reader
from app.repo.base import BaseRepo


class ReaderRepo(BaseRepo):
    model = Reader