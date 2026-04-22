import pytest
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from jose import jwt
from app.core.config import settings

def test_password_hashing():
    password = "secret_password"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False

def test_create_access_token():
    data = {"sub": "user_id_123", "role": "admin"}
    token = create_access_token(data)
    
    # Giải mã token để kiểm tra dữ liệu bên trong
    decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    
    assert decoded_data["sub"] == data["sub"]
    assert decoded_data["role"] == data["role"]
    assert "exp" in decoded_data

def test_create_refresh_token():
    data = {"sub": "user_id_123"}
    token = create_refresh_token(data)
    
    decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    
    assert decoded_data["sub"] == data["sub"]
    assert decoded_data["type"] == "refresh"
    assert "exp" in decoded_data
