from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user_id, PaginationParams
from app.schemas.borrow_record import BorrowRecordCreate, BorrowRecordUpdateStatus, BorrowRecordResponse
from app.schemas.pagination import PageResponse
from app.services import borrow_service

router = APIRouter(prefix="/borrows", tags=["Borrows"])

@router.post("", response_model=BorrowRecordResponse, status_code=status.HTTP_201_CREATED)
def create_borrow(
    borrow: BorrowRecordCreate, 
    db: Session = Depends(get_db), 
    current_user_id: int = Depends(get_current_user_id)
):
    """Gửi yêu cầu mượn sách/bộ sưu tập"""
    return borrow_service.create_borrow_v1(db, borrow, current_user_id)

@router.get("", response_model=PageResponse[BorrowRecordResponse])
def get_my_borrows(
    db: Session = Depends(get_db), 
    current_user_id: int = Depends(get_current_user_id),
    pagination: PaginationParams = Depends()
):
    """Xem danh sách các đơn mượn liên quan đến mình (người mượn hoặc chủ sách)"""
    return borrow_service.get_user_borrows_v1(db, current_user_id, pagination)

@router.get("/{id}", response_model=BorrowRecordResponse)
def get_borrow_detail(
    id: int, 
    db: Session = Depends(get_db), 
    current_user_id: int = Depends(get_current_user_id)
):
    """Xem chi tiết một đơn mượn (chỉ dành cho người liên quan)"""
    return borrow_service.get_borrow_by_id_v1(db, id, current_user_id)

@router.patch("/{id}/status", response_model=BorrowRecordResponse)
def update_borrow_status(
    id: int, 
    status_update: BorrowRecordUpdateStatus, 
    db: Session = Depends(get_db), 
    current_user_id: int = Depends(get_current_user_id)
):
    """Cập nhật trạng thái đơn mượn (Chỉ dành cho chủ sách - Owner)"""
    return borrow_service.update_borrow_status_v1(db, id, status_update, current_user_id)
