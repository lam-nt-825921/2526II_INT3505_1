from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, PaginationParams, SearchParams
from app.schemas.book import BookResponse
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

@router.get("/{id}", response_model=BookResponse)
def get_book(id: int, db: Session = Depends(get_db)):
    """Xem chi tiết cuốn sách"""
    return book_service.get_book_by_id_v1(db, id)
