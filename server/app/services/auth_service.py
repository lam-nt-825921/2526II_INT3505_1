from sqlalchemy.orm import Session
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.schemas.auth import RegisterRequest
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.core.errors import ErrorCode, AppException

def register_user_v1(db: Session, user_in: RegisterRequest):
    existing_user = db.query(User).filter(User.username == user_in.username).first()
    if existing_user:
        raise AppException(status_code=status.HTTP_400_BAD_REQUEST, error_code=ErrorCode.USER_ALREADY_EXISTS)
    
    existing_email = db.query(User).filter(User.email == user_in.email).first()
    if existing_email:
         raise AppException(status_code=status.HTTP_400_BAD_REQUEST, error_code=ErrorCode.USER_ALREADY_EXISTS)
    
    hashed_pwd = get_password_hash(user_in.password)
    # Gán role mặc định khi đăng ký là member
    new_user = User(username=user_in.username, email=user_in.email, name=user_in.name, phone=user_in.phone, hashed_password=hashed_pwd, role="member")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user_v1(db: Session, request: OAuth2PasswordRequestForm):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise AppException(status_code=status.HTTP_401_UNAUTHORIZED, error_code=ErrorCode.INVALID_CREDENTIALS, headers={"WWW-Authenticate": "Bearer"})
    
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    refresh_token = create_refresh_token(data={"sub": str(user.id), "role": user.role})
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "refresh_token": refresh_token
    }

def refresh_token_v1(db: Session, token: str):
    from app.core.config import settings
    from jose import jwt, JWTError
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub: str = payload.get("sub")
        token_type: str = payload.get("type", "")
        if sub is None or token_type != "refresh":
            raise AppException(status_code=status.HTTP_401_UNAUTHORIZED, error_code=ErrorCode.INVALID_CREDENTIALS, headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise AppException(status_code=status.HTTP_401_UNAUTHORIZED, error_code=ErrorCode.INVALID_CREDENTIALS, headers={"WWW-Authenticate": "Bearer"})
        
    user = db.query(User).filter(User.id == int(sub)).first()
    if not user:
        raise AppException(status_code=status.HTTP_401_UNAUTHORIZED, error_code=ErrorCode.INVALID_CREDENTIALS)
        
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}
