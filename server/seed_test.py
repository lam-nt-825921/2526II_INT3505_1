import sys
import os

# Thêm thư mục hiện tại vào sys.path để có thể import app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import engine, SessionLocal, Base
from app.models.user import User
from app.models.book import Book
from app.core.security import get_password_hash

def seed_test_data():
    from app.core.config import settings
    print(f"--- Khởi tạo dữ liệu Test vào DB: {settings.SQLALCHEMY_DATABASE_URL} ---")
    
    # 1. Xóa và tạo lại toàn bộ bảng để đảm bảo Clean Slate
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 2. Tạo tài khoản Admin
        admin_user = User(
            username="admin",
            email="admin@library.com",
            name="System Admin",
            hashed_password=get_password_hash("admin123"),
            role="admin",
            phone="0000000000"
        )
        db.add(admin_user)
        
        # 3. Tạo tài khoản User2
        user2 = User(
            username="user2",
            email="user2@example.com",
            name="User Two",
            hashed_password=get_password_hash("user123"),
            role="member",
            phone="0987654321"
        )
        db.add(user2)
        db.flush() # Để lấy được ID của user2
        
        # 4. Tạo 1 cuốn sách duy nhất thuộc về User2
        book_of_user2 = Book(
            title="Sách của User 2",
            author="Tác giả ẩn danh",
            description="Cuốn sách này dùng để test lỗi 403 khi User 1 cố tình sửa",
            price=150000.0,
            stock=5,
            owner_id=user2.id
        )
        db.add(book_of_user2)
        
        db.commit()
        print("✅ Đã tạo tài khoản: 'admin' (pass: admin123)")
        print("✅ Đã tạo tài khoản: 'user2' (pass: user123)")
        print(f"✅ Đã tạo 1 cuốn sách thuộc về User2 (ID: {book_of_user2.id})")
        print("--- Hoàn tất ---")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_test_data()
