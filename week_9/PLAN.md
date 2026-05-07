# Kế hoạch nâng cấp Payment API từ v1 lên v2

## 1. Tổng quan
- **Mục tiêu**: Nâng cấp hệ thống thanh toán để xử lý dữ liệu chính xác hơn.
- **Thay đổi quan trọng (Breaking Change)**: Chuyển đổi kiểu dữ liệu của trường `amount` trong endpoint rút tiền từ **String** sang **Double/Float**.
- **Thời hạn đóng hoàn toàn v1 (Sunset Date)**: **Thứ Tư, 31/12/2026**.

---

## 2. Chiến lược thông báo và Deprecation
Để đảm bảo đối tác có đủ thời gian chuyển đổi, hệ thống sẽ áp dụng các cơ chế thông báo sau:

### 2.1. Thông báo qua HTTP Headers (tại v1)
Kể từ khi v2 ra mắt, tất cả các phản hồi từ v1 sẽ bao gồm các header chuẩn mực:
- `Deprecation`: `@true` (Thông báo endpoint đã lỗi thời).
- `Sunset`: `Wed, 31 Dec 2026 23:59:59 GMT` (Thời điểm đóng API).
- `Link`: `<https://api.example.com/docs/migration-v1-v2>; rel="deprecation"` (Link hướng dẫn migrate).
- `Warning`: `299 - "The v1 API is deprecated and will be removed on 2026-12-31. Please migrate to v2."`

### 2.2. Tài liệu & Email
- Gửi thông báo chính thức cho các đối tác tích hợp.
- Cập nhật tài liệu API với nhãn **[DEPRECATED]** cho các endpoint v1.

---

## 3. Lộ trình triển khai (Implementation Roadmap)

### Bước 1: Mở rộng Database (Expand)
- **Mục tiêu**: Đảm bảo DB hỗ trợ cả hai phiên bản mà không làm hỏng dữ liệu cũ.
- **Hành động**: Kiểm tra lại schema hiện tại. Vì SQLite/SQLAlchemy đã dùng kiểu `Float` ở model, bước này chủ yếu là kiểm tra tính nhất quán và đảm bảo không có ràng buộc (constraints) nào ở mức DB bắt buộc phải là String.

### Bước 2: Tạo Route và Controller cho v2
- **Hành động**: 
    - Tạo thư mục `app/api/v2/`.
    - Định nghĩa `WithdrawalRequestV2` trong schemas với `amount: float`.
    - Tạo các endpoint v2 mới.

### Bước 3: Sửa logic ở Service để dùng kiểu dữ liệu mới
- **Hành động**: 
    - Cập nhật `payment_service.py` để ưu tiên xử lý `float`.
    - Tạo hàm `withdraw_v2` nhận trực tiếp `amount` kiểu float.

### Bước 4: Code "Phiên dịch" (Adapter) tại Controller v1
- **Hành động**: 
    - Giữ nguyên `WithdrawalRequestV1` (amount: str).
    - Tại controller v1, thực hiện ép kiểu từ `str` sang `float` trước khi gọi logic ở Service mới.
    - Đảm bảo v1 vẫn hoạt động bình thường với dữ liệu cũ nhưng sử dụng "lõi" logic của v2.

### Bước 5: Cập nhật Response Headers cho v1
- **Hành động**: Thêm các header Deprecation/Sunset (đã nêu ở mục 2.1) vào middleware hoặc trực tiếp tại router v1.

---

## 4. Nhật ký thực hiện (Implementation Log)

| Ngày | Bước | Nội dung công việc | Kết quả | Ảnh demo |
| :--- | :--- | :--- | :--- | :--- |
| 07/05/2026 | Khởi tạo | Hoàn thành API v1 và Kế hoạch nâng cấp | Đã sẵn sàng | [N/A] |
| 07/05/2026 | 2 | Tạo Route/Schema và Controller cho v2 | Hoàn thành | [Demo v2] |
| 07/05/2026 | 3 | Sửa logic ở Service hỗ trợ v2 | Hoàn thành | [Demo logic] |
| 07/05/2026 | 4 | Code Adapter cho v1 (Sử dụng logic v2) | Hoàn thành | [Demo Adapter] |
| 07/05/2026 | 5 | Cập nhật Deprecation Headers cho v1 | Hoàn thành | [Minh chứng Header] |

---
*Ghi chú: Mỗi bước hoàn thành sẽ được cập nhật vào nhật ký này kèm theo minh chứng.*
