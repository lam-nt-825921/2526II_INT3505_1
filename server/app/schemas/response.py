from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel
from app.core.errors import ErrorCode

T = TypeVar('T')

class ErrorDetail(BaseModel):
    code: ErrorCode
    message: str

class APIResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[ErrorDetail] = None

class PaginatedData(BaseModel, Generic[T]):
    items: list[T]
    total: int
    skip: int
    limit: int

class PaginatedResponse(APIResponse[PaginatedData[T]]):
    pass
