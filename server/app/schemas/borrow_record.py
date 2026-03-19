from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class BorrowStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    RETURNED = "returned"
    EXPIRED = "expired"

class BorrowRecordCreate(BaseModel):
    book_id: Optional[int] = None
    collection_id: Optional[int] = None
    additional_info: Optional[str] = None

class BorrowRecordUpdateStatus(BaseModel):
    status: BorrowStatus

class BorrowRecordResponse(BaseModel):
    id: int
    book_id: Optional[int]
    collection_id: Optional[int]
    borrower_id: int
    owner_id: int
    status: BorrowStatus
    additional_info: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
