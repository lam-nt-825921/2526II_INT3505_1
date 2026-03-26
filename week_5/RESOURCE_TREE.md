# RESOURCE_TREE.md: Thiết kế Cây Tài nguyên API (API Resource Tree)

Dựa trên phương pháp tại `PLAN.md`, dưới đây là thiết kế các endpoints cho hệ thống quản lý thư viện.

## 1. Resource: Books (`/books`)
Đại diện cho danh mục sách trong thư viện.

- `GET /books`
  - **Mô tả:** Lấy danh sách sách. Hỗ trợ tìm kiếm và phân trang.
  - **Query Params (Demo Pagination):** - Offset/Limit: `?offset=0&limit=20`
    - Page-based: `?page=1&size=20`
    - Cursor-based: `?cursor=last_id_here&limit=20`
  - **Query Params (Search):** `?q=tên_sách` hoặc `?author=tên_tác_giả`
- `GET /books/{bookId}`
  - **Mô tả:** Lấy chi tiết một cuốn sách.
- `POST /books`
  - **Mô tả:** Thêm sách mới vào thư viện (Dành cho Admin/Thủ thư).
- `PUT /books/{bookId}`
  - **Mô tả:** Cập nhật toàn bộ thông tin sách.
- `DELETE /books/{bookId}`
  - **Mô tả:** Xóa sách (hoặc đánh dấu ngưng sử dụng).

## 2. Resource: Users (`/users`)
Đại diện cho độc giả/thành viên.

- `GET /users`
  - **Mô tả:** Lấy danh sách thành viên (Hỗ trợ phân trang tương tự `/books`).
- `GET /users/{userId}`
  - **Mô tả:** Lấy thông tin chi tiết của một độc giả.
- `POST /users`
  - **Mô tả:** Đăng ký thành viên mới.

## 3. Resource: Loans (`/loans`)
Đại diện cho các giao dịch mượn/trả sách.

- `GET /loans`
  - **Mô tả:** Lấy toàn bộ lịch sử mượn sách của thư viện (Dành cho Admin). Hỗ trợ phân trang.
  - **Query Params (Filter):** `?status=active` (đang mượn) hoặc `?status=returned` (đã trả).
- `GET /loans/{loanId}`
  - **Mô tả:** Lấy chi tiết một phiếu mượn.
- `POST /loans`
  - **Mô tả:** Mượn sách (Tạo mới một giao dịch mượn). 
  - **Payload:** `{ "userId": "123", "bookId": "456" }`
- `PATCH /loans/{loanId}`
  - **Mô tả:** Trả sách (Cập nhật trạng thái phiếu mượn).
  - **Payload:** `{ "status": "returned", "returnedAt": "2026-03-26T10:00:00Z" }`

## 4. Sub-Resources (Mối quan hệ)
- `GET /users/{userId}/loans`
  - **Mô tả:** Lấy danh sách các sách đã/đang mượn của MỘT độc giả cụ thể. Hỗ trợ phân trang để xử lý trường hợp một người mượn rất nhiều lần trong năm.