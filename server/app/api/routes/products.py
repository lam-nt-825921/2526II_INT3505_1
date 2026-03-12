from typing import List
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

from app.schemas.product import ProductCreate, ProductResponse
from app.schemas.review import ReviewCreate, ReviewResponse
from app.api.dependencies import get_db, get_current_user
from app.services import product_service, review_service
from app.models.user import User

from app.schemas.response import APIResponse, PaginatedResponse, PaginatedData

router = APIRouter()

@router.get("/", response_model=PaginatedResponse[ProductResponse])
def list_products(response: Response, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = product_service.get_products(db, skip=skip, limit=limit)
    response.headers["Cache-Control"] = "public, max-age=60"
    
    return {
        "success": True,
        "data": {
            "items": [ProductResponse.model_validate(p) for p in products],
            "total": len(products),
            "skip": skip,
            "limit": limit
        }
    }

@router.post("/", response_model=APIResponse[ProductResponse], status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = product_service.create_product(db=db, product=product_in, user_id=current_user.id)
    return {"success": True, "data": ProductResponse.model_validate(product)}

@router.get("/{id}", response_model=APIResponse[ProductResponse])
def get_product(id: int, response: Response, db: Session = Depends(get_db)):
    db_product = product_service.get_product(db, product_id=id)
    response.headers["Cache-Control"] = "public, max-age=120"
    return {"success": True, "data": ProductResponse.model_validate(db_product)}

@router.delete("/{id}", response_model=APIResponse[dict])
def delete_product(
    id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product_service.delete_product(db, product_id=id, user_id=current_user.id)
    return {"success": True, "data": {"message": "Đã xóa sản phẩm thành công"}}

# URL /proucts/{id}/reviews
@router.get("/{id}/reviews", response_model=PaginatedResponse[ReviewResponse])
def list_product_reviews(id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reviews = review_service.get_reviews_by_product(db, product_id=id, skip=skip, limit=limit)
    return {
        "success": True,
        "data": {
            "items": [ReviewResponse.model_validate(r) for r in reviews],
            "total": len(reviews),
            "skip": skip,
            "limit": limit
        }
    }

# URL /proucts/{id}/reviews
@router.post("/{id}/reviews", response_model=APIResponse[ReviewResponse], status_code=status.HTTP_201_CREATED)
def create_product_review(
    id: int,
    review_in: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    review = review_service.create_review(db=db, review=review_in, product_id=id, user_id=current_user.id)
    return {"success": True, "data": ReviewResponse.model_validate(review)}

# URL /proucts/{id}/reviews/{review_id}
@router.delete("/{id}/reviews/{review_id}", response_model=APIResponse[dict])
def delete_product_review(
    id: int,
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    review_service.delete_review(db, review_id=review_id, user_id=current_user.id)
    return {"success": True, "data": {"message": "Đã xóa đánh giá thành công"}}
