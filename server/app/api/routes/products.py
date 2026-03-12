from typing import List
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

from app.schemas.product import ProductCreate, ProductResponse
from app.api.dependencies import get_db, get_current_user
from app.services import product_service
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def list_products(response: Response, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = product_service.get_products(db, skip=skip, limit=limit)
    response.headers["Cache-Control"] = "public, max-age=60"
    return products

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return product_service.create_product(db=db, product=product_in, user_id=current_user.id)

@router.get("/{id}", response_model=ProductResponse)
def get_product(id: int, response: Response, db: Session = Depends(get_db)):
    db_product = product_service.get_product(db, product_id=id)
    response.headers["Cache-Control"] = "public, max-age=120"
    return db_product

@router.delete("/{id}")
def delete_product(
    id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product_service.delete_product(db, product_id=id, user_id=current_user.id)
    return {"message": "Đã xóa sản phẩm thành công"}
