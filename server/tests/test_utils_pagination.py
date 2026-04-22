import pytest
from unittest.mock import MagicMock
from app.utils.pagination import paginate_query
from app.api.dependencies import PaginationParams

def test_paginate_query_basic():
    # 1. Tạo Mock cho SQLAlchemy Query
    mock_query = MagicMock()
    
    # Giả lập hành vi của query.count() trả về 100 bản ghi
    mock_query.count.return_value = 100
    
    # Giả lập query.offset().limit().all() trả về list 10 item giả
    mock_items = [MagicMock() for _ in range(10)]
    mock_query.offset.return_value.limit.return_value.all.return_value = mock_items
    
    # 2. Tạo params phân trang (Trang 2, mỗi trang 10 cái)
    pagination = PaginationParams(page=2, size=10)
    
    # 3. Chạy hàm cần test
    result = paginate_query(mock_query, pagination)
    
    # 4. Kiểm tra (Assert)
    assert result["total"] == 100
    assert result["page"] == 2
    assert result["size"] == 10
    assert result["total_pages"] == 10
    assert len(result["items"]) == 10
    
    # Kiểm tra xem offset có được tính đúng không (Trang 2, size 10 => offset = 10)
    mock_query.offset.assert_called_with(10)

def test_paginate_query_empty():
    mock_query = MagicMock()
    mock_query.count.return_value = 0
    mock_query.offset.return_value.limit.return_value.all.return_value = []
    
    pagination = PaginationParams(page=1, size=20)
    result = paginate_query(mock_query, pagination)
    
    assert result["total"] == 0
    assert result["total_pages"] == 0
    assert result["items"] == []
