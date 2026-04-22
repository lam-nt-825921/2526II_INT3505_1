from fastapi import APIRouter
from app.api.v1 import (
    auth as auth_v1, 
    users as users_v1, 
    books as books_v1, 
    collections as collections_v1,
    borrows as borrows_v1
)

# Đọc các thư viện của V2 (Ghi đè)
from app.api.v2.public_routes import books as books_v2_public

router = APIRouter()

# ====================================================
# 1. Nhóm API PUBLIC & PRIVATE (V2 kế thừa V1)
# ====================================================

# Ưu tiên load V2 trước
router.include_router(books_v2_public.router)

# Load các router V1 (Đã bao gồm cả public và private logic bên trong)
router.include_router(books_v1.router)
router.include_router(users_v1.router)
router.include_router(auth_v1.router)
router.include_router(collections_v1.router)
router.include_router(borrows_v1.router)
