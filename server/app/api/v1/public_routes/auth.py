from fastapi import APIRouter, Depends, status, Response, Request
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import RegisterRequest, Token
from app.schemas.user import UserResponse
from app.services import auth_service
from app.core.errors import AppException, ErrorCode

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Đăng ký tài khoản mới"""
    return auth_service.register_user_v1(db, request)

@router.post("/login", response_model=Token)
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Đăng nhập hệ thống bằng Form Data (Trả Access Token qua JSON, Refresh qua Cookie)"""
    token_data = auth_service.login_user_v1(db, form_data)
    
    # Set the refresh token as an HttpOnly cookie
    response.set_cookie(
        key="refresh_token", 
        value=token_data.pop("refresh_token"), 
        httponly=True, 
        max_age=7 * 24 * 60 * 60, # 7 days
        samesite="lax", # secure=True should be used in production with HTTPS
    )
    return token_data

@router.post("/refresh", response_model=Token)
def refresh(request: Request, db: Session = Depends(get_db)):
    """Sử dụng Refresh Token chạy ngầm trong Cookie để lấy Access Token mới"""
    token = request.cookies.get("refresh_token")
    if not token:
        raise AppException(status_code=status.HTTP_401_UNAUTHORIZED, error_code=ErrorCode.INVALID_CREDENTIALS)
    
    return auth_service.refresh_token_v1(db, token)

@router.post("/logout")
def logout(response: Response):
    """Đăng xuất, xoá Refresh Cookie"""
    response.delete_cookie(key="refresh_token")
    return {"message": "Đăng xuất thành công"}
