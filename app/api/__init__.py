from fastapi import APIRouter
from .endpoints.users import router as users_router
from .endpoints.books import router as books_router
from .endpoints.readers import router as readers_router
from .endpoints.library import router as lib_router
router = APIRouter()

router.include_router(users_router)
router.include_router(books_router)
router.include_router(readers_router)
router.include_router(lib_router)