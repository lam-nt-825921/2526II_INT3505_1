### Kế hoạch tạo swagger cho các enpoint, đảm bảo chuẩn OpenAPI

- Viết sơ lược kiến thức vào README.md
- Tạo kế hoạch sửa đổi server theo chuẩn OpenAPI, kế hoạch bao gồm:
    + Xác định rõ lại API là gì -> định nghĩa ra các entity
    + Xác định các enpoint phiên bản này cần có (coi như đây là version 1.0.0)
    + Xác định cách xác thực, phân quyền
    + Tiến hành sửa enpoint và model theo đúng kế hoạch
    + Tạo file swagger.yaml theo đúng chuẩn OpenAPI
    + Tạo tài liệu tự động bằng Swagger UI
    + Xác định kết quả bằng cách render swagger ui

---

### 1. Xác định rõ lại API là gì và định nghĩa các entity

**Mô tả API:**
API quản lý thư viện sách trực tuyến. Người dùng đăng nhập để tương tác với hệ thống. Có 2 vai trò (người dùng nào cũng có cả 2 vai trò, phân ra ở đây chỉ để rõ ràng mục đích của enpoint thôi):
- **Chủ sách**: Đăng tải (tạo), chỉnh sửa, xóa sách của mình; tạo các bộ sưu tập/tuyển tập sách.
- **Người đọc**: Tìm kiếm sách, xem chi tiết thông tin và đặt lịch mượn sách.
*Lưu ý: Sách tự động được quản lý hiển thị theo số lượng tồn kho (sẽ báo ẩn nếu hết số lượng. Nếu không khai báo, số lượng mặc định là vô hạn).*

**Các thực thể (Entities) cốt lõi:**
1. `User`: Lưu thông tin tài khoản đăng nhập và định danh vai trò (Chủ sách / Người đọc).
2. `Book`: Thông tin chi tiết của sách, số lượng tồn kho định mức, có tham chiếu đến người đăng (Chủ sách).
3. `Collection`: Bộ sưu tập/tuyển tập gồm nhiều sách (do Chủ sách tạo ra), có thể mượn theo bộ.
4. `BorrowRecord`: Đơn đặt lịch mượn sách (lưu giữ thông tin: Người đọc, Sách báo mượn và trạng thái duyệt đơn).

**Chi tiết các trường (Fields) và Kiểu dữ liệu:**

1. **User**
   - `id` (Integer): Khóa chính.
   - `username` (String): Tài khoản đăng nhập (unique).
   - `password` (String): Mật khẩu (đã được băm/mã hóa).
   - `name` (String): Tên người dùng.
   - `email` (String): Email người dùng.
   - `phone` (String): Số điện thoại người dùng.
   - `created_at` (DateTime): Thời gian tạo tài khoản.

2. **Book**
   - `id` (Integer): Khóa chính.
   - `title` (String): Tiêu đề sách.
   - `author` (String): Tác giả cuốn sách.
   - `description` (Text): Thông tin chi tiết mô tả sách.
   - `quantity` (Integer, Nullable): Số lượng tồn kho (nếu `null` => vô hạn).
   - `owner_id` (Integer): Tham chiếu `User.id` (chủ sở hữu sách).
   - `collection_id` (Integer, Nullable): Tham chiếu `Collection.id`. (Một sách có thể thuộc về 1 bộ sưu tập).
   - `created_at` (DateTime): Ngày đăng sách.

3. **Collection**
   - `id` (Integer): Khóa chính.
   - `title` (String): Tên bộ sưu tập.
   - `description` (Text, Nullable): Mô tả ngắn về bộ sưu tập.
   - `owner_id` (Integer): Tham chiếu `User.id` (Chủ sở hữu, quy định mọi sách trong bộ sưu tập này phải khớp `owner_id` với nó).
   - `created_at` (DateTime): Ngày tạo bộ sưu tập.

4. **BorrowRecord**
   - `id` (Integer): Khóa chính.
   - `book_id` (Integer, Nullable): Tham chiếu `Book.id` được mượn. 
   - `collection_id` (Integer, Nullable): Tham chiếu `Collection.id` nếu người mượn yêu cầu mượn cả bộ. (Chỉ 1 trong 2 trường `book_id` hoặc `collection_id` có giá trị).
   - `borrower_id` (Integer): Tham chiếu `User.id` của người đọc.
   - `owner_id` (Integer): Tham chiếu `User.id` của chủ sách/chủ bộ sưu tập (người sở hữu tài sản bị mượn). Giúp tối ưu hóa truy vấn xem ai đang đặt lịch với mình.
   - `status` (String): Trạng thái lịch (`pending` - chờ chủ sách duyệt, `approved` - đã duyệt, `rejected` - từ chối, `returned` - đã trả, `expired` - lịch hết hạn).
   - `additional_info` (Text, Nullable): Thông tin bổ sung, lời nhắn hoặc trao đổi cách thức lấy/trả sách.
   - `created_at` (DateTime): Thời gian gửi yêu cầu mượn.

---

### 2. Xác định các Endpoint (Version 1.0.0)


**A. Xác thực (Authentication)**
- `POST /api/v1/auth/register`: Đăng ký tài khoản.
- `POST /api/v1/auth/login`: Đăng nhập (trả về token).

**B. Người dùng (Users)**
- `GET /api/v1/users/{id}`: Xem thông tin công khai của người dùng (Tên, Email, SĐT).

**C. Sách (Books)**
- `GET /api/v1/books`: Tìm kiếm và lấy danh sách sách.
- `POST /api/v1/books`: Thêm (đăng) sách mới.
- `GET /api/v1/books/{id}`: Xem thông tin chi tiết một cuốn sách.
- `PUT /api/v1/books/{id}`: Chọn sửa sách (yêu cầu phải là chủ sách).
- `DELETE /api/v1/books/{id}`: Xóa sách (yêu cầu phải là chủ sách).

**D. Bộ sưu tập (Collections)**
- `GET /api/v1/collections`: Tìm kiếm và lấy danh sách bộ sưu tập.
- `POST /api/v1/collections`: Tạo bộ sưu tập sách mới.
- `GET /api/v1/collections/{id}`: Xem chi tiết bộ sưu tập (bao gồm các sách bên trong).
- `PUT /api/v1/collections/{id}`: Sửa thông tin bộ sưu tập (yêu cầu là chủ bộ sưu tập).
- `DELETE /api/v1/collections/{id}`: Xóa bộ sưu tập (yêu cầu là chủ bộ sưu tập).

**E. Đặt lịch mượn (Borrow Records)**
- `POST /api/v1/borrows`: Tạo đơn mượn (truyền `book_id` hoặc `collection_id`).
- `GET /api/v1/borrows`: Lấy danh sách lịch mượn tài khoản đang tham gia (đơn đi mượn hoặc đơn người khác mượn sách của mình).
- `GET /api/v1/borrows/{id}`: Xem chi tiết một lịch mượn cụ thể.
- `PATCH /api/v1/borrows/{id}/status`: Cập nhật trạng thái duyệt/từ chối hoặc trả sách (dành cho chủ sách).

---

### 3. Xác định cách xác thực và phân quyền

Ở phiên bản hiện tại (v1.0.0), hệ thống bảo mật sẽ được thiết kế theo cơ chế như sau:

**A. Xác thực (Authentication)**
- Quản lý đăng nhập bằng **Bearer Token JWT**.
- Sau khi người dùng gọi API đăng nhập thành công, server sẽ sinh ra và trả về một chuỗi JWT.
- Khi người dùng gửi request đến các API được bảo vệ, client phải đính kèm chuỗi này vào giao thức HTTP Header (ví dụ: `Authorization: Bearer <chuỗi_token>`). Nếu token hợp lệ (chưa hết hạn và được ký đúng), cho phép truy cập.

**B. Phân quyền (Authorization)**
Hệ thống sử dụng cơ chế bảo mật theo tài nguyên. Có 2 mức phân quyền chính:
- **Quyền Cơ bản (Requires Login)**: Chỉ cần có JWT hợp lệ được gửi lên là có thể thao tác (Ví dụ: Thêm sách, tạo bộ sưu tập, tìm kiếm danh sách sách, xem thông tin sinh viên, đặt lịch mượn). 
- **Quyền Sở hữu (`isOwner`)**: Được áp dụng trên các endpoint quan trọng để chống truy cập trái phép. Nó áp dụng cho các hành động thay đổi/xóa tài nguyên (VD: Sửa/xóa sách, cập nhật thông tin bộ sưu tập, phê duyệt lịch mượn sách). Hệ thống sẽ kiểm tra xem `user_id` (được giải mã từ Token) có khớp với `owner_id` của đối tượng đang thao tác hay không. Nếu kiểm tra thất bại, server sẽ chặn request với mã lỗi `403 Forbidden`.


