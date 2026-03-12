from sqlalchemy.orm import Session
from fastapi import status

from app.models.user import User
from app.schemas.auth import UserCreate
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.errors import ErrorCode, AppException

def register_user(db: Session, user_in: UserCreate):

    existing_user = db.query(User).filter(User.username == user_in.username).first()
    if existing_user:
        raise AppException(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=ErrorCode.USER_ALREADY_EXISTS,
        )
    
    hashed_pwd = get_password_hash(user_in.password)
    
    new_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_pwd
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
def authenticate_user(db: Session, username: str, password_in: str):

    user = db.query(User).filter(User.username == username).first()
    
    if not user or not verify_password(password_in, user.hashed_password):

        raise AppException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=ErrorCode.INVALID_CREDENTIALS,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = create_access_token(
        data={"sub": user.username}
    )
    
    return access_token_expires
