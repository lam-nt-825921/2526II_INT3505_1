from fastapi import APIRouter, Depends
from app.api.dependencies import get_token_payload
from . import books, collections, borrows

# Khóa cứng luồng private tại chính nội tại module để bảo tồn trạng thái bảo mật cao nhất
router = APIRouter(dependencies=[Depends(get_token_payload)])
router.include_router(books.router)
router.include_router(collections.router)
router.include_router(borrows.router)
