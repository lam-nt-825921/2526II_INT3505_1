from fastapi import APIRouter
from . import auth, users, books, collections

router = APIRouter()
router.include_router(auth.router)
router.include_router(users.router)
router.include_router(books.router)
router.include_router(collections.router)
