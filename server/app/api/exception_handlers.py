from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.errors import AppException, ErrorCode, ERROR_DESCRIPTIONS

async def app_exception_handler(request: Request, exc: AppException):
    # Trả về format chuẩn thống nhất cho tất cả mã lỗi Custom của hệ thống
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": exc.detail,
                "message": ERROR_DESCRIPTIONS.get(exc.detail, "Lỗi không xác định")
            }
        },
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Mapping lỗi validation mặc định của FastAPI (422) thành cấu trúc APIResponse thống nhất
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Dữ liệu đầu vào không hợp lệ",
                "details": exc.errors() # Optional: Có thể ẩn đi nếu muốn giấu chi tiết trả về
            }
        },
    )

async def global_exception_handler(request: Request, exc: Exception):
    # Mapping mọi Exception chưa được lường trước (Lỗi Internal Server 500)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Đã có lỗi ngoại lệ xảy ra trên hệ thống."
            }
        },
    )
