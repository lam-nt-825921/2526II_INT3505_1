from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from app.core.errors import AppException, ErrorCode, ERROR_DESCRIPTIONS

async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "detail": exc.detail,  # Thêm lại để khớp với Postman Test
            "error": {
                "code": exc.detail,
                "message": ERROR_DESCRIPTIONS.get(exc.detail, "Lỗi không xác định")
            }
        },
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "detail": exc.detail,  # Thêm lại để khớp với Postman Test
            "error": {
                "code": "HTTP_ERROR",
                "message": exc.detail
            }
        },
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "detail": "VALIDATION_ERROR", # Thêm để đồng nhất
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Dữ liệu đầu vào không hợp lệ",
                "details": jsonable_encoder(exc.errors())
            }
        },
    )

async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "detail": "INTERNAL_SERVER_ERROR",
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Đã có lỗi ngoại lệ xảy ra trên hệ thống."
            }
        },
    )
