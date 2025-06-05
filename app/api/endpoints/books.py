from typing import List

from fastapi import APIRouter, HTTPException

from app.api.deps import CurrentUser
from app.api.schemas.books import BookSchema, BookUpdateSchema
from app.repo.books import BookRepo

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/all", response_model=List[BookSchema])
async def get_books():
    books = await BookRepo.get_all()
    return books

@router.get("/{book_id}")
async def get_book(book_id: str):
    book = await BookRepo.get_one_or_none(uuid=book_id)
    return {"book": book}

@router.post("/create")
async def create_book(book_data: BookSchema, cu: CurrentUser):
    try:
        book = await BookRepo.create(book_data.model_dump())
    except Exception as e:
        if 'books_isbn_key' in str(e.orig):
            raise HTTPException(status_code=409, detail="Book with this ISBN already exists")
        raise HTTPException(status_code=500, detail="Error add book")
    return {"book": book}

@router.delete("/delete/{book_id}")
async def delete_book(book_id: str, cu: CurrentUser):
    book = await BookRepo.delete(uuid=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"success": True}
@router.patch("/update/{book_id}")
async def update_book(uuid: str, data: BookUpdateSchema, cu: CurrentUser):
    book = await BookRepo.get_one_or_none(uuid=uuid)
    if book:
        try:
            update_data = {k: v for k, v in data.dict().items() if v is not None}
            update_book = await BookRepo.update(book.uuid, update_data)
            return {"success": True,
                    "book": update_book}
        except Exception as e:
            if 'books_isbn_key' in str(e.orig):
                raise HTTPException(status_code=409, detail="Book with this ISBN already exists")
            raise HTTPException(status_code=500, detail="Error updating book")
    raise HTTPException(status_code=404, detail="Book not found")