from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas.user import UserPublic
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/{id}", response_model=UserPublic)
def get_user_public_info(id: int, db: Session = Depends(get_db)):
    """Xem thông tin công khai của người dùng"""
    return user_service.get_user_by_id_v1(db, id)
