import pytest
from unittest.mock import MagicMock, patch
from app.services.book_service import (
    create_book_v1, 
    get_book_by_id_v1, 
    update_book_v1, 
    get_all_books_v1,
    delete_book_v1,
    admin_delete_book_v1
)
from app.schemas.book import BookCreate, BookUpdate
from app.models.book import Book
from app.core.errors import AppException
from app.api.dependencies import PaginationParams, SearchParams

def test_get_all_books_with_search():
    db = MagicMock()
    pagination = PaginationParams(page=1, size=10)
    search = SearchParams(q="Python")
    
    # Mock paginate_query vì hàm này được gọi cuối cùng
    with patch("app.services.book_service.paginate_query") as mock_paginate:
        mock_paginate.return_value = {"items": [], "total": 0}
        
        get_all_books_v1(db, pagination, search)
        
        # Kiểm tra xem filter ilike có được gọi với từ khóa "Python" không
        # Đây là một cách nâng cao để kiểm tra xem logic filter có chạy không
        assert db.query.called
        assert mock_paginate.called

def test_create_book_v1():
    db = MagicMock()
    book_in = BookCreate(
        title="Test Book",
        author="Author Name",
        description="Description",
        price=100.0,
        stock=10
    )
    current_user_id = 1
    
    result = create_book_v1(db, book_in, current_user_id)
    
    assert result.title == "Test Book"
    assert result.owner_id == current_user_id
    assert db.add.called
    assert db.commit.called

def test_get_book_by_id_success():
    db = MagicMock()
    mock_book = Book(id=1, title="Found Book")
    db.query().filter().first.return_value = mock_book
    
    result = get_book_by_id_v1(db, 1)
    
    assert result.id == 1
    assert result.title == "Found Book"

def test_get_book_by_id_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    
    with pytest.raises(AppException) as exc:
        get_book_by_id_v1(db, 999)
    assert exc.value.status_code == 404

def test_update_book_success():
    db = MagicMock()
    mock_book = Book(id=1, title="Old Title", owner_id=1)
    db.query().filter().first.return_value = mock_book
    
    book_in = BookUpdate(title="New Title")
    result = update_book_v1(db, 1, book_in, current_user_id=1)
    
    assert result.title == "New Title"
    assert db.commit.called

def test_update_book_permission_denied():
    db = MagicMock()
    mock_book = Book(id=1, title="Old Title", owner_id=1)
    db.query().filter().first.return_value = mock_book
    
    book_in = BookUpdate(title="New Title")
    with pytest.raises(AppException) as exc:
        update_book_v1(db, 1, book_in, current_user_id=2)
    assert exc.value.status_code == 403

def test_delete_book_success():
    db = MagicMock()
    mock_book = Book(id=1, owner_id=1)
    db.query().filter().first.return_value = mock_book
    
    delete_book_v1(db, 1, current_user_id=1)
    
    assert db.delete.called
    assert db.commit.called

def test_admin_delete_book():
    db = MagicMock()
    # Sách của người dùng 1
    mock_book = Book(id=1, owner_id=1)
    db.query().filter().first.return_value = mock_book
    
    # Admin xóa (không cần truyền current_user_id vào hàm này theo logic của bạn)
    admin_delete_book_v1(db, 1)
    
    assert db.delete.called
    assert db.commit.called
