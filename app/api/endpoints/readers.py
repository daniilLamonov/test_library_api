from fastapi import APIRouter, HTTPException

from app.api.deps import CurrentUser
from app.api.schemas.readers import ReaderSchema, ReaderUpdateSchema
from app.repo.books import BookRepo
from app.repo.library import LibraryRepo
from app.repo.readers import ReaderRepo

router = APIRouter(prefix="/readers", tags=["readers"])

@router.get("/")
async def reader_list(cu: CurrentUser):
    return await ReaderRepo.get_all()

@router.post("/add_reader", response_model=ReaderSchema)
async def reader_add(creds: ReaderSchema, cu: CurrentUser):
    reader_in_db = await ReaderRepo.get_one_or_none(email=creds.email)
    if reader_in_db:
        raise HTTPException(status_code=409, detail="Reader already exists")
    return await ReaderRepo.create(creds.model_dump())

@router.delete("/delete_reader/{reader_uuid}")
async def reader_delete(reader_uuid: str):
    readers_to_del = await ReaderRepo.delete(uuid=reader_uuid)
    if not readers_to_del:
        raise HTTPException(status_code=404, detail="Reader not found")
    return {"success": True}

@router.patch("/update_reader/{reader_uuid}", response_model=ReaderSchema)
async def reader_update(reader_uuid: str, data: ReaderUpdateSchema, cu: CurrentUser):
    reader_in_db = await ReaderRepo.get_one_or_none(uuid=reader_uuid)
    if reader_in_db:
        update_data = {k: v for k, v in data if v is not None}
        return await ReaderRepo.update(reader_uuid, update_data)
    raise HTTPException(status_code=404, detail="Reader not found")

@router.get("/books/{reader_uuid}", description="Get a list of books of reader by id")
async def reader_books(reader_uuid: str, cu: CurrentUser):
    reader = await ReaderRepo.get_one_or_none(uuid=reader_uuid)
    if reader:
        books = []
        borrows = await LibraryRepo.get_debts(reader_uuid=reader.uuid)
        for borrow in borrows:
            book = await BookRepo.get_one_or_none(uuid=borrow.book_uuid)
            books.append(book)
        return books
    raise HTTPException(status_code=404, detail="Reader not found")