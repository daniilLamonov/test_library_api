from httpx import AsyncClient

async def test_example(auth_client: AsyncClient):
    response = await auth_client.post("/books/create", json={
            "title": "string",
            "author": "string",
            "year_of_publish": "string",
            "isbn": "string",
            "count": 1
        })
    assert response.status_code == 200

async def test_try_borrow_4_book(auth_client: AsyncClient):
    response = await auth_client.post("/library/give_book", params={
        "book_id": "273b6062-f1aa-4779-a8c1-c7decc305f0f",
        "reader_id": "91e8d190-7ee6-483c-8ed4-1153a7c348c4",
        "quantity": 1
    })
    assert response.status_code == 409