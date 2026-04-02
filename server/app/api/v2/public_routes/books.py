from fastapi import APIRouter
from typing import List

router = APIRouter(prefix="/books", tags=["Books V2"])

@router.get("")
def get_books_v2():
    """Phiên bản V2 của API lấy sách (Đã được nâng cấp)"""
    return [{"message": "Xin chào! Bạn đang truy cập vào phiên bản Sách V2 mới nhất! Các API khác (auth, users) vẫn đang sử dụng đồ cũ của V1."}]
