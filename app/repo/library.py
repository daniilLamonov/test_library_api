from app.db.models import Borrows
from app.repo.base import BaseRepo

class LibraryRepo(BaseRepo):
    model = Borrows

