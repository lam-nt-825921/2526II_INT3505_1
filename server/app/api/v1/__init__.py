from fastapi import APIRouter
from . import auth, users, books, collections, borrows

# Gom V1
router = APIRouter()
router.include_router(auth.router)
router.include_router(users.router)
router.include_router(books.router)
router.include_router(collections.router)
router.include_router(borrows.router)
