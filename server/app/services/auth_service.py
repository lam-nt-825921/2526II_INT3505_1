from sqlalchemy.orm import Session
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.schemas.auth import RegisterRequest
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.errors import ErrorCode, AppException

def register_user_v1(db: Session, user_in: RegisterRequest):
    existing_user = db.query(User).filter(User.username == user_in.username).first()
    if existing_user:
        raise AppException(status_code=status.HTTP_400_BAD_REQUEST, error_code=ErrorCode.USER_ALREADY_EXISTS)
    
    existing_email = db.query(User).filter(User.email == user_in.email).first()
    if existing_email:
         raise AppException(status_code=status.HTTP_400_BAD_REQUEST, error_code=ErrorCode.USER_ALREADY_EXISTS)
    
    hashed_pwd = get_password_hash(user_in.password)
    new_user = User(username=user_in.username, email=user_in.email, name=user_in.name, phone=user_in.phone, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user_v1(db: Session, request: OAuth2PasswordRequestForm):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise AppException(status_code=status.HTTP_401_UNAUTHORIZED, error_code=ErrorCode.INVALID_CREDENTIALS, headers={"WWW-Authenticate": "Bearer"})
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
