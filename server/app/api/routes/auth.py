from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.services import auth_service
from app.schemas.auth import UserCreate, Token
from app.api.dependencies import get_db

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    user_in: UserCreate, 
    db: Session = Depends(get_db)
):
    auth_service.register_user(db, user_in)
    return {"message": "Đăng ký thành công"}

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    access_token = auth_service.authenticate_user(db, form_data.username, form_data.password)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
