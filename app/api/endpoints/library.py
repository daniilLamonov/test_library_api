from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from app.repo.books import BookRepo
from app.repo.library import LibraryRepo
from app.repo.readers import ReaderRepo

router = APIRouter(prefix="/library", tags=["library"])


@router.post("/give_book")
async def give_book(book_id: str, reader_id: str, quantity: int):
    book = await BookRepo.get_one_or_none(uuid=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.count < 1:
        raise HTTPException(status_code=404, detail="No more books")
    reader = await ReaderRepo.get_one_or_none(uuid=reader_id)
    if reader is None:
        raise HTTPException(status_code=404, detail="Reader not found")
    debts = await LibraryRepo.get_debts(reader.uuid)
    quantity_all = quantity
    for debt in debts:
        quantity_all += debt.quantity
    if quantity_all > 3:
        raise HTTPException(status_code=409, detail="Cannot give more than 3 books")
    borrow = await LibraryRepo.create(
        {
            "reader_uuid": reader.uuid,
            "book_uuid": book.uuid,
            "borrow_date": datetime.now().replace(tzinfo=None),
            "quantity": quantity,
        }
    )
    if borrow is None:
        raise HTTPException(status_code=500, detail="Cannot give book")

    await BookRepo.update(book_id, {"count": book.count - 1})
    return borrow


@router.post("/return_book")
async def return_book(book_id: str, reader_id: str):
    book = await BookRepo.get_one_or_none(uuid=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    reader = await ReaderRepo.get_one_or_none(uuid=reader_id)
    if reader is None:
        raise HTTPException(status_code=404, detail="Reader not found")
    borrow = await LibraryRepo.return_book(
        reader.uuid, book.uuid
    )
    if borrow is None:
        raise HTTPException(status_code=409, detail="Client dont have this book or this book already returned")
    await BookRepo.update(book_id, {"count": book.count + 1})
    return borrow
