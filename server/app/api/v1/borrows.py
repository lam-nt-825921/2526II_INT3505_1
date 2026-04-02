from fastapi import APIRouter, Depends, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user_id, PaginationParams
from app.schemas.borrow_record import BorrowRecordCreate, BorrowRecordUpdateStatus, BorrowRecordResponse
from app.schemas.pagination import PageResponse
from app.services import borrow_service

router = APIRouter(prefix="/borrows", tags=["Borrow Records"])

@router.post("", response_model=BorrowRecordResponse, status_code=status.HTTP_201_CREATED)
def create_borrow(borrow: BorrowRecordCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Tạo đơn mượn (truyền book_id hoặc collection_id)"""
    return borrow_service.create_borrow_v1(db, borrow, current_user_id)

@router.get("", response_model=PageResponse[BorrowRecordResponse])
def get_borrows(
    db: Session = Depends(get_db), 
    current_user_id: int = Depends(get_current_user_id),
    pagination: PaginationParams = Depends()
):
    """Lấy danh sách lịch mượn tài khoản đang tham gia (đơn đi mượn hoặc đơn người khác mượn sách của mình)"""
    return borrow_service.get_user_borrows_v1(db, current_user_id, pagination)

@router.get("/{id}", response_model=BorrowRecordResponse)
def get_borrow(id: int, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Xem chi tiết một lịch mượn cụ thể"""
    return borrow_service.get_borrow_by_id_v1(db, id, current_user_id)

@router.patch("/{id}/status", response_model=BorrowRecordResponse)
def update_borrow_status(id: int, status_update: BorrowRecordUpdateStatus, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Cập nhật trạng thái duyệt/từ chối hoặc trả sách (dành cho chủ sách/người mượn)"""
    return borrow_service.update_borrow_status_v1(db, id, status_update, current_user_id)
