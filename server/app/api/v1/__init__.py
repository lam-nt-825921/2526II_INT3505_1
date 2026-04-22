from fastapi import APIRouter
from .auth import router as auth_router
from .books import router as books_router
from .collections import router as collections_router
from .users import router as users_router
from .borrows import router as borrows_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(books_router)
router.include_router(collections_router)
router.include_router(users_router)
router.include_router(borrows_router)
