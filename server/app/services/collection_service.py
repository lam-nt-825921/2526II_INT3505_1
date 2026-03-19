from sqlalchemy.orm import Session
from fastapi import status
from app.models.collection import Collection
from app.schemas.collection import CollectionCreate, CollectionUpdate
from app.core.errors import ErrorCode, AppException

def get_all_collections_v1(db: Session):
    return db.query(Collection).all()

def create_collection_v1(db: Session, coll_in: CollectionCreate, current_user_id: int):
    new_coll = Collection(**coll_in.model_dump(), owner_id=current_user_id)
    db.add(new_coll)
    db.commit()
    db.refresh(new_coll)
    return new_coll

def get_collection_by_id_v1(db: Session, coll_id: int):
    coll = db.query(Collection).filter(Collection.id == coll_id).first()
    if not coll: raise AppException(status_code=status.HTTP_404_NOT_FOUND, error_code=ErrorCode.ITEM_NOT_FOUND)
    return coll

def update_collection_v1(db: Session, coll_id: int, coll_in: CollectionUpdate, current_user_id: int):
    coll = get_collection_by_id_v1(db, coll_id)
    if coll.owner_id != current_user_id: raise AppException(status_code=status.HTTP_403_FORBIDDEN, error_code=ErrorCode.PERMISSION_DENIED)
    
    for key, value in coll_in.model_dump(exclude_unset=True).items():
        setattr(coll, key, value)
    db.commit()
    db.refresh(coll)
    return coll

def delete_collection_v1(db: Session, coll_id: int, current_user_id: int):
    coll = get_collection_by_id_v1(db, coll_id)
    if coll.owner_id != current_user_id: raise AppException(status_code=status.HTTP_403_FORBIDDEN, error_code=ErrorCode.PERMISSION_DENIED)
    db.delete(coll)
    db.commit()
