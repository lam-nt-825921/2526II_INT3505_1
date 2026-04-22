import pytest
from unittest.mock import MagicMock
from app.services.auth_service import register_user_v1, login_user_v1
from app.schemas.auth import RegisterRequest
from app.models.user import User
from app.core.errors import AppException
from fastapi.security import OAuth2PasswordRequestForm

def test_register_user_success():
    # Mock DB Session
    db = MagicMock()
    # Giả lập không tìm thấy user trùng tên/email
    db.query().filter().first.return_value = None
    
    user_in = RegisterRequest(
        username="testuser",
        email="test@example.com",
        password="password123",
        name="Test User",
        phone="0123456789"
    )
    
    result = register_user_v1(db, user_in)
    
    assert result.username == "testuser"
    assert db.add.called
    assert db.commit.called

def test_register_user_already_exists():
    db = MagicMock()
    # Giả lập đã tồn tại user
    db.query().filter().first.return_value = User(username="testuser")
    
    user_in = RegisterRequest(
        username="testuser",
        email="test@example.com",
        password="password123",
        name="Test User",
        phone="0123456789"
    )
    
    with pytest.raises(AppException) as exc:
        register_user_v1(db, user_in)
    
    assert exc.value.status_code == 400

def test_login_user_invalid_credentials():
    db = MagicMock()
    # Giả lập không tìm thấy user
    db.query().filter().first.return_value = None
    
    request = MagicMock(spec=OAuth2PasswordRequestForm)
    request.username = "wronguser"
    request.password = "wrongpass"
    
    with pytest.raises(AppException) as exc:
        login_user_v1(db, request)
    
    assert exc.value.status_code == 401
