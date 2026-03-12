from sqlalchemy.orm import Session
from fastapi import status
from app.models.product import Product
from app.schemas.product import ProductCreate
from app.core.errors import ErrorCode, AppException

def create_product(db: Session, product: ProductCreate, user_id: int):
    db_product = Product(**product.model_dump(), owner_id=user_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, skip: int = 0, limit: int = 100):
    # Lấy danh sách sản phẩm (Bất kỳ ai cũng xem được)
    return db.query(Product).offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
    # Lấy chi tiết 1 sản phẩm
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise AppException(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ErrorCode.PRODUCT_NOT_FOUND,
        )
    return db_product

def delete_product(db: Session, product_id: int, user_id: int):
    # Kiểm tra xem sản phẩm có tồn tại không
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise AppException(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ErrorCode.PRODUCT_NOT_FOUND,
        )
    
    # Kiểm tra quyền
    if db_product.owner_id != user_id:
        raise AppException(
            status_code=status.HTTP_403_FORBIDDEN,
            error_code=ErrorCode.PRODUCT_DELETE_FORBIDDEN,
        )
        
    db.delete(db_product)
    db.commit()
    return db_product
