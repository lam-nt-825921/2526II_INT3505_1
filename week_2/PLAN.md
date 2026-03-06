### Kế hoạch cập nhật lên v4 cacheable

## Hướng giải

- Cập nhật API GET /products để có thể cache
- Cập nhật API GET /products/{id} để có thể cache
- Cache bằng cách chèn thêm headers vào response

## Thiết kế API

**Kiến trúc server**
Để xây nên một server bài bản cần tạo cấu trúc logic, dễ bảo trì.

server/
├── app/
│   ├── __init__.py
│   ├── main.py                 # File khởi chạy ứng dụng FastAPI (app object)
│   ├── core/                   # Cấu hình cốt lõi dùng chung
│   │   ├── config.py           # Load biến môi trường (Settings)
│   │   └── security.py         # Hàm băm mật khẩu, hàm tạo/giải mã JWT
│   ├── api/                    # Định nghĩa các Controller / Endpoints (Routes)
│   │   ├── dependencies.py     # Chứa Dependency Injection (ví dụ: get_current_user, get_db)
│   │   └── routes/
│   │       ├── auth.py         # Chứa router /login, /register
│   │       └── products.py     # Chứa router /products (GET, POST,...)
│   ├── models/                 # Chứa các class biểu diễn bảng Database
│   │   ├── user.py
│   │   └── product.py
│   ├── schemas/                # Chứa các Pydantic models (Validate request/response, Typing)
│   │   ├── auth.py             # VD: Token, UserCreate, UserLogin
│   │   └── product.py          # VD: ProductResponse, ProductCreate
│   ├── services/               # Chứa Business Logic (xử lý logic nghiệp vụ)
│   │   ├── auth_service.py     # Xử lý gọi DB để xác thực user
│   │   └── product_service.py  # Xử lý lấy, tính toán thông tin sản phẩm
│   └── db/                     # Quản lý kết nối Database
│       └── session.py          # Kết nối với SQLAlchemy
├── .env