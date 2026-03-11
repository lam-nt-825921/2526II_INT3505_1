from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    owner_id: Optional[int] = None

    class Config:
        from_attributes = True
