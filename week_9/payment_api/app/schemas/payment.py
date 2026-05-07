from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    full_name: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class AccountBase(BaseModel):
    account_number: str
    balance: float

class AccountResponse(AccountBase):
    id: int
    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    transaction_type: str
    amount: float
    description: str
    created_at: datetime

class TransactionResponse(TransactionBase):
    id: int
    class Config:
        from_attributes = True

# V1 Withdrawal Request - amount is String
class WithdrawalRequestV1(BaseModel):
    account_number: str
    amount: str  # Breaking change in V2 will be float
    description: Optional[str] = "Withdrawal"

# V2 Withdrawal Request - amount is Float
class WithdrawalRequestV2(BaseModel):
    account_number: str
    amount: float
    description: Optional[str] = "Withdrawal"

class LoginRequest(BaseModel):
    username: str
    password: str
