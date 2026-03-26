
## Hướng dẫn Đọc Tài liệu

Để hiểu rõ tư duy thiết kế và bối cảnh trước khi xem code, vui lòng đọc các tài liệu theo thứ tự sau:

1. **[CONTEXT.md](./CONTEXT.md):** Đọc đầu tiên. Nắm bắt bối cảnh nghiệp vụ (Domain Context) của hệ thống quản lý thư viện và các thực thể cốt lõi (Users, Books, Loans).
2. **[PLAN.md](./PLAN.md):** Đọc thứ hai. Hiểu phương pháp luận 4 bước để chuyển đổi từ nghiệp vụ thực tế sang thiết kế API.
3. **[RESOURCE_TREE.md](./RESOURCE_TREE.md):** Đọc thứ ba. Xem kết quả bản đồ các Endpoints (URIs) đã được thiết kế hoàn chỉnh.

## Hướng dẫn xem Code Demo

Trong khi kiến trúc tài nguyên được mô tả chi tiết ở các file Markdown, phần **Code Demo** tập trung vào việc cài đặt thực tế 3 chiến lược Phân trang (Pagination) thường gặp nhất. Riêng phần Data modeling thì được cài đặt ở serer/app chính vì ở đó đã cài database và phương thức giao tiếp với database là ORM nên sẽ tiện hơn.

**Mã nguồn Demo nằm tại thư mục:** `[./demo](./demo)`

Các ví dụ trong thư mục `./demo` sẽ mô phỏng cách truy vấn và trả về dữ liệu cho các kỹ thuật:
- **Offset/Limit Pagination** (Phổ biến, dễ cài đặt nhưng chậm với dữ liệu lớn).
- **Page-based Pagination** (Thân thiện với UI).
- **Cursor-based Pagination** (Hiệu năng cực cao, phù hợp cho Infinite Scroll).

*Lưu ý: Code demo sử dụng dữ liệu giả lập (mock data) để minh họa luồng xử lý (logic flow) thay vì kết nối với một database thực tế phức tạp.*