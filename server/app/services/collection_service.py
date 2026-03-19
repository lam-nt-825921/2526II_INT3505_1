from sqlalchemy.orm import Session
from fastapi import status
from app.models.collection import Collection
from app.schemas.collection import CollectionCreate, CollectionUpdate
from app.core.errors import ErrorCode, AppException

def get_all_collections_v1(db: Session):
    return db.query(Collection).all()

def create_collection_v1(db: Session, coll_in: CollectionCreate, current_user_id: int):
    new_coll = Collection(
        title=coll_in.title,
        description=coll_in.description,
        owner_id=current_user_id
    )
    db.add(new_coll)
    db.commit()
    db.refresh(new_coll)
    return new_coll

def get_collection_by_id_v1(db: Session, coll_id: int):
    coll = db.query(Collection).filter(Collection.id == coll_id).first()
    if not coll:
        raise AppException(status_code=status.HTTP_404_NOT_FOUND, error_code=ErrorCode.ITEM_NOT_FOUND, message="Không tìm thấy Collection")
    return coll

def update_collection_v1(db: Session, coll_id: int, coll_in: CollectionUpdate, current_user_id: int):
    coll = get_collection_by_id_v1(db, coll_id)
    if coll.owner_id != current_user_id:
        raise AppException(status_code=status.HTTP_403_FORBIDDEN, error_code=ErrorCode.PERMISSION_DENIED, message="Không có quyền thao tác")
    
    if coll_in.title is not None: coll.title = coll_in.title
    if coll_in.description is not None: coll.description = coll_in.description
    
    db.commit()
    db.refresh(coll)
    return coll

def delete_collection_v1(db: Session, coll_id: int, current_user_id: int):
    coll = get_collection_by_id_v1(db, coll_id)
    if coll.owner_id != current_user_id:
        raise AppException(status_code=status.HTTP_403_FORBIDDEN, error_code=ErrorCode.PERMISSION_DENIED, message="Không có quyền thao tác")
    db.delete(coll)
    db.commit()
