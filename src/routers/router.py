from fastapi import APIRouter

from src.routers.auth.router import router as auth_router
from src.routers.books.router import router as books_router
from src.routers.author.router import router as author_router

router = APIRouter(prefix="/v1/api")

router.include_router(router=auth_router)
router.include_router(router=books_router)
router.include_router(router=author_router)