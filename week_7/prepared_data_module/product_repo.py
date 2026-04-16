from sqlalchemy.orm import Session
from . import db_models
from .models import ProductCreate

def get_products(db: Session, name: str = None, min_price: float = None, max_price: float = None):
    query = db.query(db_models.DBProduct)
    if name:
        query = query.filter(db_models.DBProduct.name.contains(name))
    if min_price is not None:
        query = query.filter(db_models.DBProduct.price >= min_price)
    if max_price is not None:
        query = query.filter(db_models.DBProduct.price <= max_price)
    return query.all()

def create_product(db: Session, product: ProductCreate):
    # Sử dụng model_dump() thay cho dict() trong Pydantic V2
    db_product = db_models.DBProduct(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product_by_id(db: Session, product_id: int):
    return db.query(db_models.DBProduct).filter(db_models.DBProduct.id == product_id).first()

def update_product(db: Session, product_id: int, product_update: ProductCreate):
    db_product = get_product_by_id(db, product_id)
    if db_product:
        for key, value in product_update.model_dump().items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product_by_id(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False
