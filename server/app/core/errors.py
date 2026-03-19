from enum import Enum
from fastapi import HTTPException

class ErrorCode(str, Enum):
    # Khối Lỗi Auth (1xxx)
    USER_ALREADY_EXISTS = "AUTH_1001"
    INVALID_CREDENTIALS = "AUTH_1002"
    
    # Khối Lỗi Căn Bản (4xxx)
    ITEM_NOT_FOUND = "ERR_4004"
    PERMISSION_DENIED = "ERR_4003"
    VALIDATION_ERROR = "ERR_4022"

ERROR_DESCRIPTIONS = {
    ErrorCode.USER_ALREADY_EXISTS: "Tên đăng nhập hoặc email đã tồn tại trong hệ thống.",
    ErrorCode.INVALID_CREDENTIALS: "Tài khoản hoặc mật khẩu không chính xác.",
    ErrorCode.ITEM_NOT_FOUND: "Tài nguyên không tìm thấy (Sách, Bộ sưu tập, Đơn mượn...).",
    ErrorCode.PERMISSION_DENIED: "Chỉ chủ sở hữu (Owner) mới có quyền thực hiện hành động này.",
    ErrorCode.VALIDATION_ERROR: "Dữ liệu đầu vào không hợp lệ hoặc thiếu tham số."
}

class AppException(HTTPException):
    def __init__(self, status_code: int, error_code: ErrorCode, headers: dict = None):
        super().__init__(status_code=status_code, detail=error_code.value, headers=headers)
