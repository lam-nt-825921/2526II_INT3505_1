from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate

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
    return db.query(Product).filter(Product.id == product_id).first()

def delete_product(db: Session, product_id: int, user_id: int):
    # Chặn quyền: Chỉ trả về sản phẩm nếu do chính người đó tạo
    db_product = db.query(Product).filter(Product.id == product_id, Product.owner_id == user_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product
