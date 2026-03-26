# Demo Các Chiến Thuật Phân Trang (Pagination Strategies)

Demo này sử dụng FastAPI để minh họa 3 chiến thuật phân trang khác nhau. Dựa trên `RESOURCE_TREE.md`, endpoint lấy danh sách sách là `GET /books`.Mỗi chiến thuật phân trang được tác ra thành một file chạy (FastAPI app) độc lập.

Các file định nghĩa cấu trúc Response (kiểu trả về) vẫn được đặt riêng biệt ở thư mục `schemas`.

## Cấu trúc thư mục

```
week_5/demo/
├── offset_limit_demo.py     # Demo chạy FastAPI cho phân trang dạng Offset/Limit
├── page_based_demo.py       # Demo chạy FastAPI cho phân trang dạng Page-based
├── cursor_based_demo.py     # Demo chạy FastAPI cho phân trang dạng Cursor-based
├── models.py                # Định nghĩa data model (thực thể Books chung)
├── schemas/                 # Chứa các file định nghĩa kiểu trả về của Response
│   ├── offset_limit.py      # Định nghĩa Response của Offset/Limit
│   ├── page_based.py        # Định nghĩa Response của Page-based
│   └── cursor_based.py      # Định nghĩa Response của Cursor-based
└── README.md                # Tài liệu hướng dẫn này
```

## Giải thích chi tiết các Chiến thuật (Strategy)

### 1. Offset / Limit Pagination
**File khởi chạy:** `offset_limit_demo.py`
**File định nghĩa model response:** `schemas/offset_limit.py`
**API Definition:** `GET /books?offset=0&limit=20`

* **Cách hoạt động:** Bỏ qua `offset` số lượng bản ghi và lấy `limit` bản ghi tiếp theo.
* **Mô hình Dữ liệu Trả về:** Gồm `items` (danh sách bản ghi), `total` (tổng số lượng record), `offset` và `limit` hiện tại.
* **Ưu điểm:** Dễ hiểu và dễ dàng map với SQL `OFFSET / LIMIT`.
* **Nhược điểm:** Hiệu suất giảm nghiêm trọng khi `offset` lớn do DB vẫn phải đọc qua các record bị bỏ qua. Bị sai lệch dữ liệu nếu có thao tác thêm/xóa xảy ra giữa các lần gọi trang.

### 2. Page-based Pagination (Page / Size)
**File khởi chạy:** `page_based_demo.py`
**File định nghĩa model response:** `schemas/page_based.py`
**API Definition:** `GET /books?page=1&size=20`

* **Cách hoạt động:** Chỉ định trang thứ `page`, mỗi trang có kích thước `size`. Bản chất thường chuyển đổi thành `offset` ngầm bên dưới (`offset = (page - 1) * size`).
* **Mô hình Dữ liệu Trả về:** Gồm `items`, `total`, `page`, `size` và `total_pages` (tổng số trang).
* **Ưu điểm:** Phù hợp với giao diện người dùng hiển thị số trang (1, 2, 3...). 
* **Nhược điểm:** Chung nhược điểm về hiệu suất và sai lệch như Offset/Limit.

### 3. Cursor-based Pagination (Next Token)
**File khởi chạy:** `cursor_based_demo.py`
**File định nghĩa model response:** `schemas/cursor_based.py`
**API Definition:** `GET /books?cursor=10&limit=20`

* **Cách hoạt động:** Dựa vào một giá trị duy nhất và tuần tự (như `id` hoặc `timestamp`) của phần tử cuối cùng để truy vấn phần tử tiếp theo (VD: `WHERE id > cursor LIMIT ...`).
* **Mô hình Dữ liệu Trả về:** Gồm `items`, `next_cursor` (con trỏ gọi cho trang sau) và `has_next` (còn trang tiếp theo không). Không nhất thiết phải có `total`.
* **Ưu điểm:** Rất nhanh ngay cả khi phân cấp hàng triệu dòng do tận dụng trực tiếp index Database. Không bị mất mát/trùng lặp dữ liệu trong quá trình thay đổi `insert/delete`.
* **Nhược điểm:** Không thể nhảy trực tiếp (jump) đến một trang cụ thể nào đó giữa chừng. Chỉ lấy được trang tiếp theo hoặc trang trước. Phải tồn tại một trường có thể sắp xếp và có tính duy nhất (Unique Sortable Column).


