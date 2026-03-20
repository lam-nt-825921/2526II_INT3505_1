# So sánh các Định dạng Mô tả API (API Description Formats)

## Giới thiệu
Thư mục này nhằm mục đích nghiên cứu, phân tích và so sánh các định dạng mô tả API phổ biến hiện nay, bao gồm: **OpenAPI**, **API Blueprint**, **RAML**, và **TypeSpec**. 

Để việc so sánh mang tính thực tiễn cao, dự án cung cấp một mô hình ứng dụng minh họa nhỏ (hệ thống quản lý thư viện). Ứng dụng này sẽ được tài liệu hóa bằng cả bốn định dạng kể trên, từ đó mang lại góc nhìn đối chiếu trực quan về cú pháp, khả năng mở rộng và mức độ hiệu quả của từng nền tảng.

## Tổng quan bài tập

### Phần 1: So sánh
- Hãy xem [INSTRUCTIONS.md](./INSTRUCTIONS.md) để hiểu rõ mục thế, phạm vi và phương pháp luận thiết lập các tiêu chí đánh giá.
- Phần trình bày kết quả so sánh cụ thể tại [SLIDE_CONTENT.md](./SLIDE_CONTENT.md).

### Phần 2: Demo
Có 4 thư mục tương ứng với demo của 4 loại định dạng mà bài tập so sánh, mỗi thư mục có hướng dẫn riêng tại file **README.md**.

#### Thống nhất về API demo
Do được tạo với mục đích demo nên API nhỏ và ít chức năng, hệ thống quản lý thư viện sẽ chỉ bao gồm **2 Thực thể (Entities)** với **5 Endpoints**. 

**1. Thực thể (Entities)**
- **Book (Sách)**: `id` (int), `title` (string), `author` (string), `status` (string: `"available"` hoặc `"borrowed"`).
- **User (Thành viên)**: `id` (int), `name` (string), `email` (string).

**2. Tiêu chuẩn Endpoints**
- `GET /books`: Phục vụ lấy danh sách sách (hỗ trợ thêm query param `?status=available`).
- `POST /books`: Thêm sách mới vào thư viện.
- `GET /books/{id}`: Xem chi tiết một sách cụ thể.
- `GET /users`: Lấy danh sách thành viên.
- `POST /users`: Thêm một thành viên mới.


#### Demo
Dưới đây là đường dẫn tới 4 demo:
- [Demo OpenAPI](./openapi-demo/README.md)
- [Demo API Blueprint](./api-blueprint-demo/README.md)
- [Demo RAML](./raml-demo/README.md)
- [Demo TypeSpec](./typespec-demo/README.md)
