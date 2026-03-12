from sqlalchemy.orm import Session
from fastapi import status
from app.models.review import Review
from app.schemas.review import ReviewCreate
from app.core.errors import ErrorCode, AppException
from app.services import product_service

def create_review(db: Session, review: ReviewCreate, product_id: int, user_id: int):
    # Đảm bảo product tồn tại trước khi cho phép review
    product_service.get_product(db, product_id)
    
    db_review = Review(
        **review.model_dump(), 
        product_id=product_id, 
        user_id=user_id
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_reviews_by_product(db: Session, product_id: int, skip: int = 0, limit: int = 100):
    # Đảm bảo product tồn tại
    product_service.get_product(db, product_id)
    
    return db.query(Review).filter(Review.product_id == product_id).offset(skip).limit(limit).all()

def delete_review(db: Session, review_id: int, user_id: int):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise AppException(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ErrorCode.REVIEW_NOT_FOUND,
        )
    
    if db_review.user_id != user_id:
        raise AppException(
            status_code=status.HTTP_403_FORBIDDEN,
            error_code=ErrorCode.REVIEW_DELETE_FORBIDDEN,
        )
        
    db.delete(db_review)
    db.commit()
    return db_review
