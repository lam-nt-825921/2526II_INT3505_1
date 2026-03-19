from sqlalchemy.orm import Session
from fastapi import status
from app.models.borrow_record import BorrowRecord
from app.models.book import Book
from app.models.collection import Collection
from app.schemas.borrow_record import BorrowRecordCreate, BorrowRecordUpdateStatus
from app.core.errors import ErrorCode, AppException

def create_borrow_v1(db: Session, borrow_in: BorrowRecordCreate, current_user_id: int):
    if not borrow_in.book_id and not borrow_in.collection_id:
        raise AppException(status_code=status.HTTP_400_BAD_REQUEST, error_code=ErrorCode.VALIDATION_ERROR)

    owner_id = None
    if borrow_in.book_id:
        book = db.query(Book).filter(Book.id == borrow_in.book_id).first()
        if not book: raise AppException(status_code=status.HTTP_404_NOT_FOUND, error_code=ErrorCode.ITEM_NOT_FOUND)
        owner_id = book.owner_id
    elif borrow_in.collection_id:
        coll = db.query(Collection).filter(Collection.id == borrow_in.collection_id).first()
        if not coll: raise AppException(status_code=status.HTTP_404_NOT_FOUND, error_code=ErrorCode.ITEM_NOT_FOUND)
        owner_id = coll.owner_id

    new_record = BorrowRecord(
        book_id=borrow_in.book_id,
        collection_id=borrow_in.collection_id,
        borrower_id=current_user_id,
        owner_id=owner_id,
        status="pending",
        additional_info=borrow_in.additional_info
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

def get_user_borrows_v1(db: Session, current_user_id: int):
    return db.query(BorrowRecord).filter(
        (BorrowRecord.borrower_id == current_user_id) | (BorrowRecord.owner_id == current_user_id)
    ).all()

def get_borrow_by_id_v1(db: Session, borrow_id: int, current_user_id: int):
    record = db.query(BorrowRecord).filter(BorrowRecord.id == borrow_id).first()
    if not record: raise AppException(status_code=status.HTTP_404_NOT_FOUND, error_code=ErrorCode.ITEM_NOT_FOUND)
    if record.borrower_id != current_user_id and record.owner_id != current_user_id:
        raise AppException(status_code=status.HTTP_403_FORBIDDEN, error_code=ErrorCode.PERMISSION_DENIED)
    return record

def update_borrow_status_v1(db: Session, borrow_id: int, status_update: BorrowRecordUpdateStatus, current_user_id: int):
    record = db.query(BorrowRecord).filter(BorrowRecord.id == borrow_id).first()
    if not record: raise AppException(status_code=status.HTTP_404_NOT_FOUND, error_code=ErrorCode.ITEM_NOT_FOUND)
    if record.owner_id != current_user_id: raise AppException(status_code=status.HTTP_403_FORBIDDEN, error_code=ErrorCode.PERMISSION_DENIED)
    
    record.status = status_update.status.value
    db.commit()
    db.refresh(record)
    return record
