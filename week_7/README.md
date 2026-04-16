# Hướng dẫn Chạy Tự Động Hóa Backend Cơ Bản - Tuần 7

Tài liệu này dùng để lưu lại các dòng lệnh bắt buộc trong quá trình sinh code tự động (Codegen), với tiêu chí: Thuần Python, Tốc độ cao và Tương thích 100% hệ điều hành Windows.

## Bước 1: Cài đặt Bộ Công Cụ
Mở Terminal, chạy lệnh cài đặt thư viện chuyên dụng cho Python:

```bash
# Thư viện sinh code tự động
pip install fastapi-code-generator

# Cài đặt sẵn FastAPI và Uvicorn để lát nữa chạy Web Server
pip install fastapi uvicorn pydantic
```

## Bước 2: Kích hoạt Auto-Generate Code
Đảm bảo Terminal đang trỏ vào thư mục `week_7` (nơi có chứa file thiết kế `openapi.yaml`). Chạy lệnh:

```bash
fastapi-codegen --input openapi.yaml --output ./server_app
```

## Bước 3: Chạy thử Server (API rỗng)
Để hệ thống tự động nối kết (Resolve Imports) các file tự sinh mà không bị lỗi đứt gãy, bạn **phải ĐỨNG Ở NGOÀI** (tại thư mục `week_7`) và chạy trực tiếp nó dưới dạng Package Module:

```bash
uvicorn server_app.main:app --port 8080 --reload
```

Mở trình duyệt, truy cập `http://localhost:8080/docs` để kiểm tra.

## Bước 4: Chuyển đổi thành System Live (Kết nối Database SQLite)

Để hệ thống tự sinh có thể lưu trữ dữ liệu thật, ta cần viết bổ sung tầng Data Access theo mô hình Clean Architecture.

**4.1. Cài đặt thư viện ORM:**
```bash
pip install sqlalchemy
```

**4.2. Khởi tạo Engine Database (`database.py`):**
Tạo file `server_app/database.py` để làm nhiệm vụ kết nối với tệp SQLite cục bộ.
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite_demo.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**4.3. Khai báo Bảng CSDL (`db_models.py`):**
Tạo file `server_app/db_models.py`. Đây là nơi ánh xạ Schema OpenAPI thành Bảng (Table) thực.
```python
from sqlalchemy import Column, Integer, String, Float
from .database import Base

class DBProduct(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    price = Column(Float)
    stock_quantity = Column(Integer)
```

**4.4. Cài đặt các Logic CRUD (`product_repo.py`):**
Tạo file `server_app/product_repo.py`. File này đóng gói các kỹ thuật truy xuất dữ liệu (Kéo, Thêm, Sửa, Xoá) gọi bằng ngôn ngữ Python.
*(Chi tiết các hàm CRUD được đóng gói thành các function riêng biệt để tái sử dụng)*.

**4.5. Nhúng Data vào Mã Tự Sinh (`main.py`):**
Mở file trung tâm `server_app/main.py`. Ta khai báo Import và thay thế các hàm rỗng (chứa `pass`) bằng dữ liệu thật (Cơ chế Dependency Injection).

*Hành động 1: Gọi lệnh khởi tạo DB ở đầu file*
```python
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import db_models, product_repo

# Đúc cấu trúc bảng vào tệp SQLite
db_models.Base.metadata.create_all(bind=engine)
```

*Hành động 2: Thay thế `pass` tại các Endpoints bằng Hàm Repo*
```python
@app.post('/products', response_model=Product, status_code=status.HTTP_201_CREATED, tags=['Products'])
def create_product(body: ProductCreate, db: Session = Depends(get_db)) -> Product:
    return product_repo.create_product(db, body)

@app.get('/products', response_model=List[Product], tags=['Products'])
def get_products(
    name: str = None, min_price: float = None, max_price: float = None, db: Session = Depends(get_db)
) -> List[Product]:
    return product_repo.get_products(db, name, min_price, max_price)
```

**4.6. Khởi chạy và Kiểm chứng:**
Bật Server:
```bash
uvicorn server_app.main:app --port 8080 --reload
```
Lên Swagger (`http://localhost:8080/docs`), gọi thử lệnh `POST /products`. Bạn sẽ thấy một file `sqlite_demo.db` xuất hiện.