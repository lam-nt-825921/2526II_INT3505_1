from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import status
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate
from app.core.errors import ErrorCode, AppException
from app.api.dependencies import PaginationParams, SearchParams
from app.utils.pagination import paginate_query

def get_all_books_v1(db: Session, pagination: PaginationParams, search: SearchParams):
    query = db.query(Book)
    
    if search.q:
        query = query.filter(
            or_(
                Book.title.ilike(f"%{search.q}%"),
                Book.author.ilike(f"%{search.q}%")
            )
        )
    
    return paginate_query(query, pagination)

def create_book_v1(db: Session, book_in: BookCreate, current_user_id: int):
    new_book = Book(**book_in.model_dump(), owner_id=current_user_id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def get_book_by_id_v1(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book: raise AppException(status_code=status.HTTP_404_NOT_FOUND, error_code=ErrorCode.ITEM_NOT_FOUND)
    return book

def update_book_v1(db: Session, book_id: int, book_in: BookUpdate, current_user_id: int):
    book = get_book_by_id_v1(db, book_id)
    if book.owner_id != current_user_id: raise AppException(status_code=status.HTTP_403_FORBIDDEN, error_code=ErrorCode.PERMISSION_DENIED)
    
    for key, value in book_in.model_dump(exclude_unset=True).items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

def delete_book_v1(db: Session, book_id: int, current_user_id: int):
    book = get_book_by_id_v1(db, book_id)
    if book.owner_id != current_user_id: raise AppException(status_code=status.HTTP_403_FORBIDDEN, error_code=ErrorCode.PERMISSION_DENIED)
    db.delete(book)
    db.commit()

def admin_delete_book_v1(db: Session, book_id: int):
    book = get_book_by_id_v1(db, book_id)
    # Bỏ qua check owner_id vì dùng cho Admin
    db.delete(book)
    db.commit()
