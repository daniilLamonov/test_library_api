from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from app.repo.books import BookRepo
from app.repo.library import LibraryRepo
from app.repo.readers import ReaderRepo

router = APIRouter(prefix="/library", tags=["library"])

@router.post("/give_book")
async def give_book(book_id: str, reader_id: str):
    book = await BookRepo.get_one_or_none(uuid=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.count < 1:
        raise HTTPException(status_code=404, detail="No more books")
    reader = await ReaderRepo.get_one_or_none(uuid=reader_id)
    if reader is None:
        raise HTTPException(status_code=404, detail="Reader not found")
    borrow = await LibraryRepo.create({
        "reader_uuid": reader.uuid,
        "book_uuid": book.uuid,
        "date": datetime.now().replace(tzinfo=None),
    })
    if borrow is None:
        raise HTTPException(status_code=500, detail="Cannot give book")

    await BookRepo.update(book_id, {"count": book.count - 1})
    return borrow



@router.post("/return_book")
async def return_book(book_id: str, reader_id: str):
    book = await BookRepo.get_one_or_none(uuid=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.count < 1:
        raise HTTPException(status_code=404, detail="No more books")
    reader = await ReaderRepo.get_one_or_none(uuid=reader_id)
    if reader is None:
        raise HTTPException(status_code=404, detail="Reader not found")
    borrow = await LibraryRepo.delete(reader_uuid=reader.uuid, book_uuid=book.uuid)
    if borrow is None:
        raise HTTPException(status_code=500, detail="Cannot return book")
    await BookRepo.update(book_id, {"count": book.count + 1})
    return {"success": True}
