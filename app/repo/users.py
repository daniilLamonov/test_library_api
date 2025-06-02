from app.db.models import Users
from app.repo.base import BaseRepo


class UserRepo(BaseRepo):
    model = Users
