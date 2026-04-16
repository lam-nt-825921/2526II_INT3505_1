from sqlalchemy import Column, Integer, String, Float
from .database import Base

class DBProduct(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    price = Column(Float)
    stock_quantity = Column(Integer)
