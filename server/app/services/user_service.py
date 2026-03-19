from sqlalchemy.orm import Session
from fastapi import status
from app.models.user import User
from app.core.errors import ErrorCode, AppException

def get_user_by_id_v1(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise AppException(status_code=status.HTTP_404_NOT_FOUND, error_code=ErrorCode.ITEM_NOT_FOUND)
    return user
