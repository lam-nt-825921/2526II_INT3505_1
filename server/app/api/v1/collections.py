from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user
from app.schemas.collection import CollectionCreate, CollectionUpdate, CollectionResponse, CollectionDetailResponse
from app.models.user import User
from app.services import collection_service

router = APIRouter(prefix="/collections", tags=["Collections"])

@router.get("", response_model=List[CollectionResponse])
def get_collections(db: Session = Depends(get_db)):
    """Tìm kiếm và lấy danh sách bộ sưu tập"""
    return collection_service.get_all_collections_v1(db)

@router.post("", response_model=CollectionResponse, status_code=status.HTTP_201_CREATED)
def create_collection(collection: CollectionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Tạo bộ sưu tập sách mới"""
    return collection_service.create_collection_v1(db, collection, current_user.id)

@router.get("/{id}", response_model=CollectionDetailResponse)
def get_collection(id: int, db: Session = Depends(get_db)):
    """Xem chi tiết bộ sưu tập (bao gồm các sách bên trong)"""
    return collection_service.get_collection_by_id_v1(db, id)

@router.put("/{id}", response_model=CollectionResponse)
def update_collection(id: int, collection: CollectionUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Sửa thông tin bộ sưu tập (yêu cầu là chủ bộ sưu tập)"""
    return collection_service.update_collection_v1(db, id, collection, current_user.id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_collection(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Xóa bộ sưu tập (yêu cầu là chủ bộ sưu tập)"""
    collection_service.delete_collection_v1(db, id, current_user.id)
    return None
