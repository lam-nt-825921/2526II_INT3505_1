from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    role = Column(String, default="member")
    created_at = Column(DateTime, default=datetime.utcnow)

    books = relationship("Book", back_populates="owner")
    collections = relationship("Collection", back_populates="owner")
    borrowed_records = relationship("BorrowRecord", foreign_keys="[BorrowRecord.borrower_id]", back_populates="borrower")
    owned_records = relationship("BorrowRecord", foreign_keys="[BorrowRecord.owner_id]", back_populates="owner")