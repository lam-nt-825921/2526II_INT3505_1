from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Demo Library Management OpenAPI",
    description="Demo quản lý sách và người dùng theo chuẩn OpenAPI.",
    version="1.0.0"
)

class BookBase(BaseModel):
    title: str
    author: str
    status: str

class Book(BookBase):
    id: int

class UserBase(BaseModel):
    name: str
    email: str

class User(UserBase):
    id: int

books_db: List[Book] = [
    Book(id=1, title="Sapiens: Lược sử loài người", author="Yuval Noah Harari", status="available"),
    Book(id=2, title="1984", author="George Orwell", status="borrowed")
]

users_db: List[User] = [
    User(id=1, name="Alice", email="alice@example.com")
]

@app.get("/books", response_model=List[Book], summary="Lấy danh sách sách")
def get_books(status: Optional[str] = Query(None, description="Lọc theo trạng thái sách", enum=["available", "borrowed"])):
    """Trả về danh sách toàn bộ sách trong thư viện."""
    if status:
        return [b for b in books_db if b.status == status]
    return books_db

@app.post("/books", response_model=Book, status_code=201, summary="Thêm sách mới vào thư viện")
def create_book(book_in: BookBase):
    """Tạo một bản ghi sách mới và trả về sách vừa lưu."""
    new_id = max((b.id for b in books_db), default=0) + 1
    new_book = Book(id=new_id, **book_in.model_dump())
    books_db.append(new_book)
    return new_book

@app.get("/books/{id}", response_model=Book, summary="Xem chi tiết một sách cụ thể")
def get_book(id: int):
    """Tìm kiếm sách dựa theo đường dẫn ID cung cấp."""
    for b in books_db:
        if b.id == id:
            return b
    raise HTTPException(status_code=404, detail="Không tìm thấy sách")

@app.get("/users", response_model=List[User], summary="Lấy danh sách thành viên")
def get_users():
    """Trả về danh sách tất cả các user."""
    return users_db

@app.post("/users", response_model=User, status_code=201, summary="Thêm thành viên mới")
def create_user(user_in: UserBase):
    """Đăng ký user mới và trả về ID."""
    new_id = max((u.id for u in users_db), default=0) + 1
    new_user = User(id=new_id, **user_in.model_dump())
    users_db.append(new_user)
    return new_user

