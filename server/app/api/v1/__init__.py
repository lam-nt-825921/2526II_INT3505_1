from fastapi import APIRouter, Depends
from app.api.dependencies import get_token_payload
from .public import router as public_router
from .private import router as private_router

router = APIRouter()

# 1. Public Routes (No authentication required globally)
router.include_router(public_router)

# 2. Private Routes (Authentication đã được cấu hình cứng ngầm bên trong private_router)
router.include_router(private_router)
