from fastapi import Depends, HTTPException, status, Query
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User

from fastapi.security import OAuth2PasswordBearer, SecurityScopes

# Khai báo loại xác thực là OAuth2 bằng Bearer Token
# Tham số tokenUrl báo cho Swagger UI biết URL nào dùng để LẤY token
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    scopes={
        "admin": "Quyền quản trị viên hệ thống (full access)",
        "member": "Quyền hội viên độc giả",
    }
)

# Dependency số 1: Xin cấp Session kết nối Database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency số 2: Lấy thông tin người dùng từ Token và Check Scopes
def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)       
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Không thể xác thực danh tính",
        headers={"WWW-Authenticate": authenticate_value},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        
        # Lấy file role (ví dụ: payload chứa "scopes": ["admin"]) hoặc custom role
        token_scopes = payload.get("scopes", [])
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
        
    # Check if the user has the required scopes
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tài khoản không có đủ quyền/scope để thực hiện hành động này",
            )
            
    return user

class PaginationParams:
    def __init__(
        self,
        page: int = Query(1, ge=1, description="Trang hiện hành (mặc định là 1)"),
        size: int = Query(20, ge=1, le=100, description="Kích thước trang (mặc định là 20)")
    ):
        self.page = page
        self.size = size

class SearchParams:
    def __init__(
        self,
        q: Optional[str] = Query(None, description="Từ khóa tìm kiếm chung (tùy chọn)")
    ):
        self.q = q
