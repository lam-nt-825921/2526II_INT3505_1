import pytest
from unittest.mock import MagicMock
from app.services.borrow_service import create_borrow_v1, get_borrow_by_id_v1, update_borrow_status_v1
from app.schemas.borrow_record import BorrowRecordCreate, BorrowRecordUpdateStatus, BorrowStatus
from app.models.borrow_record import BorrowRecord
from app.models.book import Book
from app.core.errors import AppException

def test_create_borrow_book_success():
    db = MagicMock()
    # Giả lập tìm thấy sách
    mock_book = Book(id=10, owner_id=20)
    db.query().filter().first.return_value = mock_book
    
    borrow_in = BorrowRecordCreate(book_id=10, additional_info="Muốn mượn đọc thử")
    current_user_id = 1 # Người mượn là ID 1
    
    result = create_borrow_v1(db, borrow_in, current_user_id)
    
    assert result.book_id == 10
    assert result.borrower_id == 1
    assert result.owner_id == 20 # Phải lấy đúng owner từ sách
    assert result.status == "pending"
    assert db.add.called

def test_create_borrow_no_ids():
    db = MagicMock()
    # Gửi request không có book_id cũng không có collection_id
    borrow_in = BorrowRecordCreate(book_id=None, collection_id=None)
    
    with pytest.raises(AppException) as exc:
        create_borrow_v1(db, borrow_in, current_user_id=1)
    assert exc.value.status_code == 400

def test_get_borrow_permission_denied():
    db = MagicMock()
    # Bản ghi mượn giữa người 10 và người 20
    mock_record = BorrowRecord(id=1, borrower_id=10, owner_id=20)
    db.query().filter().first.return_value = mock_record
    
    # Người dùng ID 30 (người lạ) cố gắng xem
    with pytest.raises(AppException) as exc:
        get_borrow_by_id_v1(db, 1, current_user_id=30)
    assert exc.value.status_code == 403

def test_update_status_only_owner_can_approve():
    db = MagicMock()
    # Người mượn: 10, Chủ sách: 20
    mock_record = BorrowRecord(id=1, borrower_id=10, owner_id=20, status="pending")
    db.query().filter().first.return_value = mock_record
    
    status_in = BorrowRecordUpdateStatus(status=BorrowStatus.APPROVED)
    
    # Case 1: Người mượn (ID 10) cố tự duyệt cho mình -> Phải lỗi 403
    with pytest.raises(AppException) as exc:
        update_borrow_status_v1(db, 1, status_in, current_user_id=10)
    assert exc.value.status_code == 403
    
    # Case 2: Chủ sách (ID 20) duyệt -> Thành công
    result = update_borrow_status_v1(db, 1, status_in, current_user_id=20)
    assert result.status == "approved"
    assert db.commit.called
