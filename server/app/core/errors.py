from enum import Enum
from fastapi import HTTPException

class ErrorCode(str, Enum):
    # Khối Lỗi Auth (1xxx)
    USER_ALREADY_EXISTS = "AUTH_1001"
    INVALID_CREDENTIALS = "AUTH_1002"
    
    # Khối Lỗi Product (2xxx)
    PRODUCT_NOT_FOUND = "PROD_2001"
    PRODUCT_DELETE_FORBIDDEN = "PROD_2002"
    
    # Khối Lỗi Review (3xxx)
    REVIEW_NOT_FOUND = "REV_3001"
    REVIEW_DELETE_FORBIDDEN = "REV_3002"

ERROR_DESCRIPTIONS = {
    ErrorCode.USER_ALREADY_EXISTS: "Tên đăng nhập đã tồn tại trong hệ thống.",
    ErrorCode.INVALID_CREDENTIALS: "Tài khoản hoặc mật khẩu không chính xác.",
    ErrorCode.PRODUCT_NOT_FOUND: "Sản phẩm không tồn tại.",
    ErrorCode.PRODUCT_DELETE_FORBIDDEN: "Bạn không có quyền xoá sản phẩm này.",
    ErrorCode.REVIEW_NOT_FOUND: "Đánh giá không tồn tại.",
    ErrorCode.REVIEW_DELETE_FORBIDDEN: "Bạn không có quyền xoá đánh giá này."
}

class AppException(HTTPException):
    def __init__(self, status_code: int, error_code: ErrorCode, headers: dict = None):
        super().__init__(status_code=status_code, detail=error_code.value, headers=headers)
