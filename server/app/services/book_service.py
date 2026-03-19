from sqlalchemy.orm import Session
from fastapi import status
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate
from app.core.errors import ErrorCode, AppException

def get_all_books_v1(db: Session):
    return db.query(Book).all()

def create_book_v1(db: Session, book_in: BookCreate, current_user_id: int):
    new_book = Book(
        title=book_in.title,
        author=book_in.author,
        description=book_in.description,
        quantity=book_in.quantity,
        collection_id=book_in.collection_id,
        owner_id=current_user_id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def get_book_by_id_v1(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise AppException(status_code=status.HTTP_404_NOT_FOUND, error_code=ErrorCode.ITEM_NOT_FOUND, message="Sách không tồn tại")
    return book

def update_book_v1(db: Session, book_id: int, book_in: BookUpdate, current_user_id: int):
    book = get_book_by_id_v1(db, book_id)
    if book.owner_id != current_user_id:
        raise AppException(status_code=status.HTTP_403_FORBIDDEN, error_code=ErrorCode.PERMISSION_DENIED, message="Bạn không có quyền sửa sách này")
    
    if book_in.title is not None: book.title = book_in.title
    if book_in.author is not None: book.author = book_in.author
    if book_in.description is not None: book.description = book_in.description
    if book_in.quantity is not None: book.quantity = book_in.quantity
    if book_in.collection_id is not None: book.collection_id = book_in.collection_id
    
    db.commit()
    db.refresh(book)
    return book

def delete_book_v1(db: Session, book_id: int, current_user_id: int):
    book = get_book_by_id_v1(db, book_id)
    if book.owner_id != current_user_id:
        raise AppException(status_code=status.HTTP_403_FORBIDDEN, error_code=ErrorCode.PERMISSION_DENIED, message="Bạn không có quyền xoá sách này")
    db.delete(book)
    db.commit()
