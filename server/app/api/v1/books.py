from fastapi import APIRouter, Depends, status, Query, Security
from typing import List, Optional
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user, PaginationParams, SearchParams
from app.schemas.book import BookCreate, BookUpdate, BookResponse
from app.schemas.pagination import PageResponse
from app.models.user import User
from app.services import book_service

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("", response_model=PageResponse[BookResponse])
def get_books(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(),
    search: SearchParams = Depends()
):
    """Tìm kiếm và lấy danh sách sách"""
    return book_service.get_all_books_v1(db, pagination, search)

@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Đăng sách mới"""
    return book_service.create_book_v1(db, book, current_user.id)

@router.get("/{id}", response_model=BookResponse)
def get_book(id: int, db: Session = Depends(get_db)):
    """Xem chi tiết cuốn sách"""
    return book_service.get_book_by_id_v1(db, id)

@router.put("/{id}", response_model=BookResponse)
def update_book(id: int, book: BookUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Sửa thông tin sách (yêu cầu quyền Chủ sách)"""
    return book_service.update_book_v1(db, id, book, current_user.id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Xóa sách (yêu cầu quyền Chủ sách)"""
    book_service.delete_book_v1(db, id, current_user.id)
    return None

@router.delete("/admin/force-delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_force_delete_book(id: int, db: Session = Depends(get_db), current_user: User = Security(get_current_user, scopes=["admin"])):
    """Xóa sách bất kỳ không cần hỏi (Chỉ dành cho Admin)"""
    book_service.admin_delete_book_v1(db, id)
    return None
