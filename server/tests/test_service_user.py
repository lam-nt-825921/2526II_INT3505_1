import pytest
from unittest.mock import MagicMock
from app.services.user_service import get_user_by_id_v1
from app.models.user import User
from app.core.errors import AppException

def test_get_user_by_id_success():
    db = MagicMock()
    mock_user = User(id=1, username="testuser")
    db.query().filter().first.return_value = mock_user
    
    result = get_user_by_id_v1(db, 1)
    
    assert result.id == 1
    assert result.username == "testuser"

def test_get_user_by_id_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    
    with pytest.raises(AppException) as exc:
        get_user_by_id_v1(db, 999)
    assert exc.value.status_code == 404
