from app.core import settings

settings.MODE = "TEST"

import json
from datetime import datetime

import httpx
import pytest

from sqlalchemy import insert

from app.db.database import engine, Base, async_session
from app.db.models import Users, Readers, Books, Borrows
from app.main import app as fastapi_app
from app.core import settings




@pytest.fixture(scope="session", autouse=True)
async def prepare_db():
    assert settings.MODE == "TEST"

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    def open_json_mock_file(name):
        with open(f"tests/mock_{name}.json", "r") as f:
            return json.load(f)

    users = open_json_mock_file("users")
    borrows = open_json_mock_file("borrows")
    readers = open_json_mock_file("readers")
    books = open_json_mock_file("books")

    for borrow in borrows:
        borrow["borrow_date"] = datetime.fromisoformat(borrow["borrow_date"])

    async with async_session() as session:
        await session.execute(insert(Users).values(users))
        await session.execute(insert(Readers).values(readers))
        await session.execute(insert(Books).values(books))
        await session.execute(insert(Borrows).values(borrows))
        await session.commit()

@pytest.fixture(scope="session")
async def client():
    transport = httpx.ASGITransport(app=fastapi_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client

@pytest.fixture(scope='session')
async def auth_client():
    transport = httpx.ASGITransport(app=fastapi_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("users/login",
                          data={"username": "user@example.com", "password": "stringst"})
        assert response.status_code == 200
        assert "access_token" in response.json()
        token = response.json()["access_token"]
        client.headers = {
            **client.headers,
            "Authorization": f"Bearer {token}"
        }
        yield client
