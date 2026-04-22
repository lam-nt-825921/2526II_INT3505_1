from fastapi import Depends, HTTPException, status, Query
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User

# Khai báo loại xác thực
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)

# Dependency số 1: Xin cấp Session kết nối Database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency số 2: Xác thực Token 
def get_token_payload(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            print("DEBUG: Token payload has no 'sub'")
            raise HTTPException(status_code=401, detail="Token không hợp lệ")
        return payload
    except JWTError as e:
        print(f"DEBUG: JWT Decode Error: {e}")
        raise HTTPException(status_code=401, detail=f"Xác thực thất bại: {str(e)}")

# Dependency số 3: Kiểm tra quyền
class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, payload: dict = Depends(get_token_payload)):
        role = payload.get("role")
        if role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tài khoản không đủ quyền (Role) để thực thi",
            )
        return payload  # Trả về payload cho các dependency phía sau nếu cần

# Dependency số 4: Truy xuất user theo JWT
def get_current_user_id(payload: dict = Depends(get_token_payload)) -> int:
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản này có Token quá cũ, không hợp lệ",
        )
    return int(sub)

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
