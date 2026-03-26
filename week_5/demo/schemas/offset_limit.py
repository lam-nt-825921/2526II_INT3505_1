from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")

class OffsetLimitResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    offset: int
    limit: int
