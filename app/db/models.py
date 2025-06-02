import uuid

from sqlalchemy.orm import mapped_column, Mapped, validates
from uuid import UUID

from .database import Base

class Users(Base):
    __tablename__ = 'users'
    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

class Books(Base):
    __tablename__ = 'books'
    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str]
    author: Mapped[str]
    year_of_publish: Mapped[str] = mapped_column(nullable=True)
    isbn: Mapped[str] = mapped_column(unique=True, nullable=True)
    count: Mapped[int] = mapped_column(default=1)
    @validates(count)
    def validate(self, count):
        if count < 1:
            raise ValueError('Book count must be greater than zero.')
        return count

class Reader(Base):
    __tablename__ = 'readers'
    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
