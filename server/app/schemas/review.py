from pydantic import BaseModel, Field
from typing import Optional

class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Số sao đánh giá từ 1 đến 5")
    content: Optional[str] = Field(None, description="Nội dung đánh giá")

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    product_id: int
    user_id: int

    class Config:
        from_attributes = True
