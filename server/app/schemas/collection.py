from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .book import BookResponse

class CollectionBase(BaseModel):
    title: str
    description: Optional[str] = None

class CollectionCreate(CollectionBase):
    pass

class CollectionUpdate(CollectionBase):
    title: Optional[str] = None
    description: Optional[str] = None

class CollectionResponse(CollectionBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CollectionDetailResponse(CollectionResponse):
    books: List[BookResponse] = []
