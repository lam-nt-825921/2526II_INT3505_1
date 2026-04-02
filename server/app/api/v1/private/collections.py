from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user_id
from app.schemas.collection import CollectionCreate, CollectionUpdate, CollectionResponse
from app.services import collection_service

router = APIRouter(prefix="/collections", tags=["Collections"])

@router.post("", response_model=CollectionResponse, status_code=status.HTTP_201_CREATED)
def create_collection(collection: CollectionCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Tạo bộ sưu tập sách mới"""
    return collection_service.create_collection_v1(db, collection, current_user_id)

@router.put("/{id}", response_model=CollectionResponse)
def update_collection(id: int, collection: CollectionUpdate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Sửa thông tin bộ sưu tập (yêu cầu là chủ bộ sưu tập)"""
    return collection_service.update_collection_v1(db, id, collection, current_user_id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_collection(id: int, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Xóa bộ sưu tập (yêu cầu là chủ bộ sưu tập)"""
    collection_service.delete_collection_v1(db, id, current_user_id)
    return None
