from fastapi import APIRouter
from app.api.v1 import users, auth, collections, borrows
from app.api.v1 import books as books_v1                
from app.api.v2 import books as books_v2                

router = APIRouter()

router.include_router(books_v2.router)

router.include_router(books_v1.router)

router.include_router(users.router)
router.include_router(auth.router)
router.include_router(collections.router)
router.include_router(borrows.router)
