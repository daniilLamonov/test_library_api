from fastapi import APIRouter
from .endpoints.users import router as users_router
from .endpoints.books import router as books_router
router = APIRouter()

router.include_router(users_router)
router.include_router(books_router)