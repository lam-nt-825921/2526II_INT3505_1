from pydantic import BaseModel, EmailStr
from datetime import datetime

# Schema yêu cầu đăng ký
class RegisterRequest(BaseModel):
    username: str
    password: str
    name: str
    email: EmailStr
    phone: str

# Schema yêu cầu đăng nhập (nếu dùng JSON body thay vì Form Data)
class LoginRequest(BaseModel):
    username: str
    password: str

# Schema trả về Token
class Token(BaseModel):
    access_token: str
    token_type: str
