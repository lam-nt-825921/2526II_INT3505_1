# CONTEXT.md: Bối cảnh thiết kế API

## 1. Giới thiệu
Dự án tuần này là một API Demo được thiết kế nhằm minh họa các nguyên tắc thiết kế Web API hiện đại liên quan đến Data modeling và Pagination:
1. **Data Modeling & Resource Design:** Xây dựng cây tài nguyên (Resource Tree) phản ánh đúng ngữ nghĩa của miền nghiệp vụ (Domain).
2. **Pagination Strategies:** Cài đặt và so sánh các chiến lược phân trang (Offset/Limit, Page-based, Cursor-based) trên các endpoint tìm kiếm và lấy danh sách.

## 2. Bối cảnh Nghiệp vụ (Domain Context)
Hệ thống xoay quanh nghiệp vụ **Quản lý Thư viện cơ bản**. 
Các hành động chính bao gồm: 
* Thư viện quản lý danh mục sách.
* Độc giả đăng ký thành viên.
* Độc giả thực hiện mượn sách và trả sách.

## 3. Các Thực thể Cốt lõi (Core Domain Models)
Thay vì ánh xạ 1-1 toàn bộ các bảng trong cơ sở dữ liệu (Database-centric), API Resource Model được thiết kế hướng tới người dùng (Consumer-centric) dựa trên 3 thực thể (Resources) cốt lõi sau:

* **`Users` (Độc giả/Thành viên):** Đại diện cho những người sử dụng dịch vụ của thư viện. Dữ liệu tập trung vào thông tin định danh và trạng thái thẻ thành viên.
* **`Books` (Sách):** Đại diện cho các đầu sách vật lý có thể mượn được. Chứa các thông tin metadata (tiêu đề, tác giả) và trạng thái sẵn sàng (có sẵn hay đang được mượn).
* **`Loans` (Phiếu mượn/Giao dịch mượn):** Bản cam kết cho hành động một Độc giả (`User`) mượn một cuốn Sách (`Book`) ghi lại thời gian mượn/trả trạng thái mượn, và các thông tin liên quan khác. 

