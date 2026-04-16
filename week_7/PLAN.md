# Kế hoạch Triển khai Backend RESTful API với OpenAPI & Swagger Codegen (Tuần 7)

## 1. Công cụ & Kiến trúc
- **Ngôn ngữ & Framework:** Python - FastAPI
- **Công cụ sinh code tự động (Codegen):** `fastapi-code-generator` (Công cụ chuẩn Python, tương thích 100% Windows và không yêu cầu Java).
- **Mức độ tự động hoá (High Automation):** Code đẻ ra một HTTP Server Project hoàn chỉnh (bao gồm `main.py`, thư mục `routers/`, và `models.py` theo quy chuẩn Pydantic). Không cần gõ lại cấu trúc hệ thống.
- **Tích hợp Database (SQLite):** Sau khi Project tự phân tách các Endpoints, chúng ta sử dụng cơ chế Plug & Play: chỉ việc gọi các hàm truy xuất CSDL nhúng vào thẳng file Router do máy tạo ra.
- **Authentication:** Thiết lập Public Access API (Mức độ Demo).

## 2. Thiết kế Cấu trúc (Tài liệu OpenAPI Spec)

### 2.1. Model Schema `Product`
Trường dữ liệu tinh gọn tập trung vào CRUD cốt lõi:
- `id` (integer) - Khóa chính
- `name` (string) - Tên sản phẩm
- `price` (number/float) - Giá bán
- `stock_quantity` (integer) - Số lượng trong kho

### 2.2. Tài nguyên API (Resource Tree)
| Phương thức | Đường dẫn (URI) | Chức năng (Tags: Product) | Input Parameters |
|:---:|---|---|---|
| `GET` | `/products` | Lấy danh sách sản phẩm | **Query:** `name` (tìm gần đúng), `min_price`, `max_price` |
| `POST` | `/products` | Tạo mới sản phẩm | **Body:** schema Product (bỏ `id`) |
| `GET` | `/products/{productId}` | Lấy chi tiết thông tin SP | **Path:** `productId` |
| `PUT` | `/products/{productId}` | Cập nhật thông tin SP | **Path:** `productId`, **Body:** Product |
| `DELETE` | `/products/{productId}` | Xóa sản phẩm khỏi CSDL | **Path:** `productId` |

### 2.3. Thiết kế Data Module (Architecture Plug-and-Play)
Để thuận tiện cho thao tác Demo rảnh tay và thể hiện Clean Architecture, ta chuẩn bị sẵn các file thao tác DB:
- `database.py`: Chứa thiết lập Connection Engine và Session DB (SQLite).
- `product_repo.py`: Chứa các hàm Logic truy xuất dữ liệu (Thêm, sửa, xóa).
- **Nguyên lý Plug & Play:** Quá trình sinh code tạo ra một bộ Router rỗng. Lập trình viên chỉ cần rút ruột Data Module (đã code sẵn) copy vào code tự gen, tiến hành Import hàm vào Router tương ứng. Code tự sinh hoàn toàn không bị vỡ kiến trúc và Server lập tức đọc được CSDL thực tế.

## 3. Lộ trình Thực hành tuần 7 (Roadmap)
Khi đi vào /create, chúng ta sẽ lần lượt thi hành:

- [ ] **Phase 1:** Thiết kế nội dung file đặc tả `swagger.yaml` mô tả chính xác API Tree nói trên bằng chuẩn OpenAPI v3.
- [ ] **Phase 2:** Sử dụng Engine Auto-codegen để dịch yaml sang source code cấu trúc thư mục FastAPI mới.
- [ ] **Phase 3:** Thiết lập kết nối SQLite, tiêm mã truy vấn (SQL) vào các function Router Service mà GenTool vừa tạo ra.
- [ ] **Phase 4:** Tiến hành test thử endpoint và Hoàn thiện tài liệu `README.md` (hướng dẫn tải package và chạy server bằng uvicorn).
