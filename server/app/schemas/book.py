from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    quantity: Optional[int] = None

class BookCreate(BookBase):
    collection_id: Optional[int] = None

class BookUpdate(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    collection_id: Optional[int] = None

class BookResponse(BookBase):
    id: int
    owner_id: int
    collection_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
