# PLAN.md: Thiết kế Tài nguyên (Resource Design Methodology)

Tài liệu này trình bày các bước chuẩn hóa mà chúng tôi đã áp dụng để chuyển đổi từ Bối cảnh nghiệp vụ (Domain Context) sang Cây tài nguyên API (API Resource Tree), dựa trên các nguyên tắc của James Higginbotham.

## Bước 1: Xác định các Thực thể Miền (Identify Domain Entities)
Thay vì nhìn vào database schema, chúng ta nhìn vào các danh từ chính trong nghiệp vụ thư viện:
- **Độc giả (Reader/User):** Người mượn sách.
- **Sách (Book):** Tài sản được cho mượn.
- **Lượt mượn (Loan/Borrowing):** Giao dịch xảy ra giữa Độc giả và Sách.
=> Từ đây, ta trích xuất được 3 tài nguyên gốc (Root Resources): `/users`, `/books`, `/loans`.

## Bước 2: Phân định Ranh giới và Mối quan hệ (Define Boundaries & Relationships)
Xác định cách các tài nguyên tương tác với nhau để quyết định cấu trúc URI (độc lập hay lồng nhau):
- Sách và Độc giả tồn tại độc lập.
- Một Lượt mượn (`Loan`) bắt buộc phải gắn với 1 `User` và 1 `Book`.
- Quản trị viên cần xem toàn bộ lịch sử mượn (`/loans`), nhưng Độc giả cũng cần xem lịch sử mượn của riêng họ (`/users/{id}/loans`).

## Bước 3: Áp dụng quy tắc Định tuyến Nông (Shallow Routing)
Để tránh URI quá dài và khó bảo trì (Anti-pattern: `/users/{userId}/loans/{loanId}/books/{bookId}`), ta giới hạn độ sâu của URI tối đa ở cấp 2.
- Truy xuất danh sách mượn của người dùng cụ thể: Dùng `/users/{userId}/loans`.
<!-- Cá nhân muốn dùng me/loans hơn nhưng để demo nên để như trên (TT ^ TT) -->
- Tương tác với một giao dịch cụ thể: Truy cập trực tiếp qua `/loans/{loanId}`.

## Bước 4: Ánh xạ Hành động sang HTTP Methods
Sử dụng danh từ cho Endpoint và để HTTP Methods (GET, POST, PUT, PATCH, DELETE) làm nhiệm vụ thể hiện hành động.
- Không dùng: `POST /borrowBook` hoặc `POST /returnBook`.
- Sử dụng: `POST /loans` (Tạo phiếu mượn) và `PATCH /loans/{id}` (Cập nhật trạng thái thành "đã trả").