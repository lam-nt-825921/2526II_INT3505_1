from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel

T = TypeVar("T")

class CursorBasedResponse(BaseModel, Generic[T]):
    items: List[T]
    next_cursor: Optional[int] = None
    has_next: bool
