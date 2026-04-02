from fastapi import APIRouter, Depends
from app.api.dependencies import get_token_payload

# Đọc các thư viện của V1 (Kế thừa)
from app.api.v1.public_routes import (
    auth as auth_v1, 
    users as users_v1, 
    books as books_v1_public, 
    collections as collections_v1_public
)
from app.api.v1.private_routes import router as private_v1_router

# Đọc các thư viện của V2 (Ghi đè)
from app.api.v2.public_routes import books as books_v2_public

router = APIRouter()

# ====================================================
# 1. Nhóm API PUBLIC (Không yêu cầu đăng nhập)
# ====================================================
public_router = APIRouter()

# Ưu tiên load V2 trước để bắt Route
public_router.include_router(books_v2_public.router)

# Load V1 bổ sung cho các Route V2 chưa làm
public_router.include_router(books_v1_public.router)
public_router.include_router(users_v1.router)
public_router.include_router(auth_v1.router)
public_router.include_router(collections_v1_public.router)

router.include_router(public_router)

# ====================================================
# 2. Nhóm API PRIVATE (Bảo toàn nguyên bản V1)
# ====================================================

# Gọi v1 private router vào (vốn dĩ đã tự ngậm cái thẻ Authentication ở chính cục router của nó rồi)
router.include_router(private_v1_router)
