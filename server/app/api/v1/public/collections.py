from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, PaginationParams, SearchParams
from app.schemas.collection import CollectionResponse, CollectionDetailResponse
from app.schemas.pagination import PageResponse
from app.services import collection_service

router = APIRouter(prefix="/collections", tags=["Collections"])

@router.get("", response_model=PageResponse[CollectionResponse])
def get_collections(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(),
    search: SearchParams = Depends()
):
    """Tìm kiếm và lấy danh sách bộ sưu tập"""
    return collection_service.get_all_collections_v1(db, pagination, search)

@router.get("/{id}", response_model=CollectionDetailResponse)
def get_collection(id: int, db: Session = Depends(get_db)):
    """Xem chi tiết bộ sưu tập (bao gồm các sách bên trong)"""
    return collection_service.get_collection_by_id_v1(db, id)
