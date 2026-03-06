from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app.schemas.product import ProductCreate, ProductResponse
from app.api.dependencies import get_db, get_current_user
from app.services import product_service
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def read_products(response: Response, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
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

@router.get("/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, response: Response, db: Session = Depends(get_db)):
    db_product = product_service.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Sản phẩm không tồn tại")
    response.headers["Cache-Control"] = "public, max-age=120"
    return db_product

@router.delete("/{product_id}")
def delete_product(
    product_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_product = product_service.delete_product(db, product_id=product_id, user_id=current_user.id)
    if db_product is None:
        raise HTTPException(status_code=403, detail="Sản phẩm không tồn tại hoặc bạn không có quyền xoá")
    return {"message": "Đã xóa sản phẩm thành công"}
