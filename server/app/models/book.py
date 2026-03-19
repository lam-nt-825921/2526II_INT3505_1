from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    description = Column(Text, nullable=True)
    quantity = Column(Integer, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    collection_id = Column(Integer, ForeignKey("collections.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="books")
    collection = relationship("Collection", back_populates="books")
    borrow_records = relationship("BorrowRecord", back_populates="book")
