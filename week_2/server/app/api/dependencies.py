from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User

# Khai báo loại xác thực là OAuth2 bằng Bearer Token
# Tham số tokenUrl báo cho Swagger UI biết URL nào dùng để LẤY token (chính là đường dẫn đăng nhập lát ta viết)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Dependency số 1: Xin cấp Session kết nối Database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency số 2: Lấy thông tin người dùng từ Token
def get_current_user(
    # Bắt FastAPI trích xuất chữ "Bearer <token>" từ Header ra, lấy cái <token> nhét vào đây
    token: str = Depends(oauth2_scheme), 
    # Bắt FastAPI mở kết nối DB luôn để lát tìm user
    db: Session = Depends(get_db)       
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Không thể xác thực danh tính",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.username == username).first()
    
    if user is None:
        raise credentials_exception
        
    return user
