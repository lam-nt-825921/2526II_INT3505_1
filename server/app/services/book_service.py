from sqlalchemy.orm import Session
from fastapi import status
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate
from app.core.errors import ErrorCode, AppException

def get_all_books_v1(db: Session):
    return db.query(Book).all()

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
