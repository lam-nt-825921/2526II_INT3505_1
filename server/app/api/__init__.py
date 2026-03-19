from fastapi import APIRouter
from .v1 import router as v1_router
from .v2 import router as v2_router

# Master Router cho toàn bộ ứng dụng
api_router = APIRouter(prefix="/api")

# Nhúng phiên bản v1 vào với tiền tố /v1 
api_router.include_router(v1_router, prefix="/v1")

# Nhúng phiên bản v2 vào với tiền tố /v2 
api_router.include_router(v2_router, prefix="/v2")
