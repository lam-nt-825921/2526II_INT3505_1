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
uvicorn server_app.main:app --port 8000 --reload
```

Mở trình duyệt, truy cập `http://localhost:8000/docs` để kiểm tra.

## Bước 4: Chuyển đổi thành System Live (Kết nối hệ cơ sở NoSQL - MongoDB)

Để hệ thống tự sinh có thể lưu trữ dữ liệu thật trên Cloud, ta sẽ xây dựng tầng Data Access Layer giao tiếp trực tiếp với MongoDB.

**4.1. Cài đặt thư viện giao tiếp:**
```bash
# Cài thư viện Mongo và thư viện đọc file ẩn (.env)
pip install pymongo python-dotenv
```

**4.2. Khai báo biến môi trường bảo mật (`.env`):**
Tạo file `.env` ở tại thư mục gốc `week_7` chứa thông tin nhạy cảm (Không bao giờ Push lên Git):
```env
MONGO_URL=mongodb+srv://<username>:<password>@cluster0.abcde.mongodb.net/?retryWrites=true&w=majority
```
*(Bạn hãy thay đổi nội dung trên bằng Connection String thật của cluster Atlas)*

**4.3. Thiết lập Engine Connect (`database.py`):**
Tạo file `server_app/database.py` làm nhiệm vụ lấy chuỗi bảo mật từ file `.env` và gọi kết nối tới Atlas.
```python
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv() # Nạp cấu hình từ .env
MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise ValueError("Lỗi: Chưa cấu hình MONGO_URL trong file .env")

client = MongoClient(MONGO_URL)
cols = client.shop_db

def get_db():
    try:
        yield cols
    finally:
        pass
```

**4.4. Cài đặt các Logic CRUD (`product_repo.py`):**
Tạo file `server_app/product_repo.py` gọi thẳng vào collection chứa Products để tận dụng tốc độ của NoSQL.
```python
from pymongo.database import Database
from pymongo import ReturnDocument
from .models import ProductCreate

def get_products(db: Database, name: str = None, min_price: float = None, max_price: float = None):
    # Thực thi Query
    cursor = db.products.find({})
    results = []
    for doc in cursor:
        doc["id"] = doc.get("_id_int", 0)
        results.append(doc)
    return results

def create_product(db: Database, product: ProductCreate):
    # Logic cấp phát ID tự động mô phỏng
    last_p = db.products.find_one(sort=[("_id_int", -1)])
    new_id = (last_p["_id_int"] + 1) if last_p and "_id_int" in last_p else 1
    
    doc = product.model_dump()
    doc["_id_int"] = new_id
    db.products.insert_one(doc)
    
    doc["id"] = new_id
    return doc
```
*(Trong Source code đính kèm chứa đầy đủ các hàm get_by_id, update, delete gốc tương ứng)*.

**4.6. Nhúng Data vào Mã Tự Sinh (`main.py`):**
Mở file trung tâm `server_app/main.py`. Ta sẽ Import Collection Dependency và tiêm vào Endpoints thay thế cho chữ `pass`.

*Hành động 1: Cập nhật Import ở phần đầu file*
```python
from fastapi import Depends, HTTPException, status
from pymongo.database import Database
from .database import get_db
from . import product_repo
```
*(Không dùng Lệnh Metadata Create All vì NoSQL sẽ tự động khởi tạo Collection khi có dữ liệu được nhét vào).* 

*Hành động 2: Thay thế `pass` tại các Endpoints*
```python
@app.post('/products', response_model=Product, status_code=status.HTTP_201_CREATED, tags=['Products'])
def create_product(body: ProductCreate, db: Database = Depends(get_db)) -> Product:
    return product_repo.create_product(db, body)

@app.get('/products', response_model=List[Product], tags=['Products'])
def get_products(
    name: str = None, min_price: float = None, max_price: float = None, db: Database = Depends(get_db)
) -> List[Product]:
    return product_repo.get_products(db, name, min_price, max_price)
```

**4.7. Khởi chạy và Kiểm chứng:**
Bật Server lên:
```bash
uvicorn server_app.main:app --port 8000 --reload
```
Lên Swagger (`http://localhost:8000/docs`), gọi thử lệnh `POST /products`. Bạn hãy truy cập vào Atlas Mongo giao diện nền web, dữ liệu Document rực rỡ JSON sẽ nằm sẵn chờ đón bạn! Kiến trúc Backend hoàn hảo!