from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=True)
    collection_id = Column(Integer, ForeignKey("collections.id"), nullable=True)
    borrower_id = Column(Integer, ForeignKey("users.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending")  # pending, approved, rejected, returned, expired
    additional_info = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    book = relationship("Book", back_populates="borrow_records")
    collection = relationship("Collection", back_populates="borrow_records")
    borrower = relationship("User", foreign_keys=[borrower_id], back_populates="borrowed_records")
    owner = relationship("User", foreign_keys=[owner_id], back_populates="owned_records")
