from fastapi import APIRouter
from app.api.v1 import users, auth, collections, borrows # Dùng lại hàng V1
from app.api.v2 import books # Dùng hàng cao cấp V2

router = APIRouter()

# 1. Mắc lưới V2 trước (Ưu tiên tóm request thay đổi)
router.include_router(books.router)

# 2. Rải lưới V1 bên dưới (Fallback/Rollback cho những request không bị đổi)
router.include_router(users.router)
router.include_router(auth.router)
router.include_router(collections.router)
router.include_router(borrows.router)
