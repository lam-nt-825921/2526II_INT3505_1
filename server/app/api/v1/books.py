from fastapi import APIRouter, Depends, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user_id, PaginationParams, SearchParams, RoleChecker
from app.schemas.book import BookCreate, BookUpdate, BookResponse
from app.schemas.pagination import PageResponse
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
def create_book(book: BookCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Đăng sách mới"""
    return book_service.create_book_v1(db, book, current_user_id)

@router.get("/{id}", response_model=BookResponse)
def get_book(id: int, db: Session = Depends(get_db)):
    """Xem chi tiết cuốn sách"""
    return book_service.get_book_by_id_v1(db, id)

@router.put("/{id}", response_model=BookResponse)
def update_book(id: int, book: BookUpdate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Sửa thông tin sách (yêu cầu quyền Chủ sách)"""
    return book_service.update_book_v1(db, id, book, current_user_id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id: int, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Xóa sách (yêu cầu quyền Chủ sách)"""
    book_service.delete_book_v1(db, id, current_user_id)
    return None

@router.delete("/admin/force-delete/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(RoleChecker(["admin"]))])
def admin_force_delete_book(id: int, db: Session = Depends(get_db)):
    """Xóa sách bất kỳ không cần hỏi (Chỉ dành cho Admin)"""
    book_service.admin_delete_book_v1(db, id)
    return None
