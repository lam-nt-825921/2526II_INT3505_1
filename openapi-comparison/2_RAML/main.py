from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Library Management - RAML Demo",
    description="Ứng dụng phục vụ demo cho chuẩn tài liệu RAML (RESTful API Modeling Language).",
    version="1.0.0"
)

# === Models ===
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

# === Dữ liệu giả định (Mock DB) ===
books_db: List[Book] = [
    Book(id=1, title="Sapiens", author="Yuval Noah Harari", status="available"),
    Book(id=2, title="1984", author="George Orwell", status="borrowed")
]

users_db: List[User] = [
    User(id=1, name="Alice", email="alice@example.com")
]

# === Endpoints ===
@app.get("/books", response_model=List[Book])
def get_books(status: Optional[str] = Query(None)):
    if status:
        return [b for b in books_db if b.status == status]
    return books_db

@app.post("/books", response_model=Book, status_code=201)
def create_book(book_in: BookBase):
    new_id = max((b.id for b in books_db), default=0) + 1
    new_book = Book(id=new_id, **book_in.model_dump())
    books_db.append(new_book)
    return new_book

@app.get("/books/{id}", response_model=Book)
def get_book(id: int):
    for b in books_db:
        if b.id == id:
            return b
    raise HTTPException(status_code=404, detail="Không tìm thấy sách")

@app.get("/users", response_model=List[User])
def get_users():
    return users_db

@app.post("/users", response_model=User, status_code=201)
def create_user(user_in: UserBase):
    new_id = max((u.id for u in users_db), default=0) + 1
    new_user = User(id=new_id, **user_in.model_dump())
    users_db.append(new_user)
    return new_user
