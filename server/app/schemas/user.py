from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    email: EmailStr
    phone: str
    role: str = "member"
    created_at: datetime

    class Config:
        from_attributes = True

class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str

    class Config:
        from_attributes = True
