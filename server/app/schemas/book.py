from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    price: float = Field(0.0, ge=0)
    stock: int = Field(0, ge=0)

class BookCreate(BookBase):
    collection_id: Optional[int] = None

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    collection_id: Optional[int] = None

class BookResponse(BookBase):
    id: int
    owner_id: int
    collection_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
