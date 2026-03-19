# Tài liệu hóa API & OpenAPI (Tóm lược)

## 1. Mục đích của Tài liệu hóa API
- **Tối ưu DX (Developer Experience)**: Dễ học, dễ tích hợp và cài đặt, dễ debug.
- **Giảm chi phí giao tiếp**: Nguồn tham khảo duy nhất cho toàn bộ team (tham số, mã lỗi lặp lại).
- **Thúc đẩy sự tiếp nhận (Adoption)**: Kênh giới thiệu, marketing hiệu quả cho Public API.
- **Quản lý vòng đời dự án**: Dễ dàng theo dõi, quản trị phiên bản (versioning).

## 2. Bản chất OpenAPI (OAS)
- Là đặc tả chuẩn kỹ thuật cho RESTful API, định dạng bằng JSON/YAML, độc lập với ngôn ngữ lập trình.
- Đóng vai trò là "Bản hợp đồng" giao kết rõ ràng giữa Client và Server.
- Máy móc và con người đều có thể đọc/hiểu để phân tích, render UI (như Swagger) hoặc tự động sinh code.

## 3. Cấu trúc cốt lõi của của một file OpenAPI chuẩn
Một tài liệu API chuẩn cần xác định đủ các điểm sau:
- **Siêu dữ liệu (`openapi`, `info`, `servers`)**: Chứa phiên bản OpenAPI, thông tin API và URL đích.
- **Định tuyến (`paths` & `operations`)**: Các Endpoints (VD: `/books`) và HTTP methods (GET, POST, PUT, DELETE).
- **Tham số đầu vào (`parameters`)**: Định nghĩa cấu trúc dữ liệu truyền lên. Có 4 vị trí truyền: `in: path`, `query`, `header`, `cookie`.
- **Thành phần Dùng chung (`components`)**: Nơi khai báo tập trung các mô hình dự liệu, tham số chung, cấu trúc xác thực... để tái sử dụng ở nhiều endpoint khác bằng cách trỏ `$ref`.
- **Mô hình Dữ liệu (`schemas`)**: Định nghĩa chi tiết cấu trúc JSON Schema cho Object (có các trường `type`, `properties`, `required`).