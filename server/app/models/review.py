from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)  # 1 to 5 stars
    content = Column(Text, nullable=True)
    
    # Quan hệ Nesting với Product
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    # Quan hệ với người đánh giá
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Đặt relationships (Tuỳ chọn cho việc query JOIN)
    # product = relationship("Product", back_populates="reviews")
    # user = relationship("User", back_populates="reviews")
