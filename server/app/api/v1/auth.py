from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, Token
from app.schemas.user import UserResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Đăng ký tài khoản mới"""
    return auth_service.register_user_v1(db, request)

@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Đăng nhập hệ thống (nhận Token)"""
    return auth_service.login_user_v1(db, request)
