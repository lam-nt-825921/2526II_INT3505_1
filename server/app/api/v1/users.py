from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user_id
from app.schemas.user import UserResponse
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def get_me(db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Lấy thông tin cá nhân (yêu cầu Login)"""
    return user_service.get_user_by_id_v1(db, current_user_id)

@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    """Xem thông tin công khai của người dùng bất kỳ"""
    return user_service.get_user_by_id_v1(db, id)
