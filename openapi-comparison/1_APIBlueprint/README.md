# Hướng dẫn phần Demo API Blueprint

Tài liệu này giới thiệu tổng quan về cách viết và đọc hiểu thiết kế **API Blueprint**. Điểm mạnh nhất của định dạng này là sự hỗ trợ ngữ pháp MSON (Markdown Syntax for Object Notation), giúp file thiết kế tài liệu trông như một văn bản Markdown rất dễ đọc.

---

## 1. Phân tích Cấu trúc File API Blueprint
Khác với tính chất phẳng và hơi lặp lại của OpenAPI JSON/YAML, file API Blueprint (thường có đuôi `.apib`) tuân thủ cấu trúc dựa trên ngữ cảnh (Heading của Markdown). Một file cơ bản gồm các thành phần sau:

### Các Headers Siêu dữ liệu (Metadata)
- **`FORMAT: 1A`**: Dòng hiển thị đầu tiên, mang tính bắt buộc để khai báo phiên bản parser của API Blueprint.
- **`HOST: url`**: (Tùy chọn) Xác định Base URL của hệ thống (Ví dụ: `http://localhost:8000`).

### Khối Cấu trúc Endpoints (Resource Groups)
API Blueprint tổ chức API theo từng khối (Group) - Tài nguyên (Resource) - Hành động (Action):
- **`# Group [Tên]`**: Định nghĩa một nhóm các API có liên quan. Ưu điểm là phân luồng tài liệu rất tốt.
- **`## [Tên_Resource] [/path]`**: Tên của tài nguyên cụ thể và đường dẫn URL. Có thể kẹp thêm param (Ví dụ: `## Books Collection [/books{?status}]`).
- **`### [Tên_Hành_Động] [HTTP_METHOD]`**: Định nghĩa trực tiếp loại request. VD: `### Tạo mới Sách [POST]`. Bên trong hành động này sẽ chứa vỏ bọc dữ liệu:
  - **`+ Parameters`**: Chứa tham số truy xuất (nếu có).
  - **`+ Request`**: Gói chuẩn bị dữ liệu gửi đi của Client (Payload).
  - **`+ Response [Status_Code]`**: Gói nhận phản hồi từ Server (VD: `+ Response 201 (application/json)`).

### Khu vực Định nghĩa Mô hình (Data Structures)
Để tăng tính Modularity (Tái sử dụng/Tránh lặp code), các file Blueprint có một khu vực khai báo gọi là **Data Structures** (tính năng tương tự `components/schemas` bên OpenAPI):
- Cú pháp khai báo cực kỳ gọn gàng với bullet points: `## [Tên_Model] (object)`
- Thuộc tính bên trong không cần ngoặc kép như JSON, chỉ cần dấu cộng: `+ current_status: available (string, required)`
- Khi gọi lại model này vào `+ Response` hay `+ Request`, ta chỉ cần gõ `+ Attributes ([Tên_Model])`. 

---

## 2. Cách Render Trình chiếu Giao diện API Blueprint

Mặc dù file `api.apib` đọc trực tiếp bằng trình gõ văn bản rất đơn giản, nhưng điểm "ăn tiền" của hệ sinh thái Blueprint là nó cung cấp các công cụ biến mã nguồn markdown đó thành một giao diện web HTML vô cùng chuyên nghiệp - chia layout theo phong cách 2-3 cột giống như tài liệu của Stripe.

Dưới đây là phương pháp xem tài liệu dễ nhất bằng công cụ **Snowboard** (Một trong những compiler mã nguồn mở tốt nhất hiện nay):

### Cách 1: Khởi chạy bằng Node.js / npx (Tối ưu cho MacOS / Linux)
Nếu máy bạn là MacOS hoặc đã cài sẵn bộ Build Tools C++, công cụ `npx snowboard` rất tuyệt vời:
```bash
# Xem live server web trên cổng 8088
npx snowboard http api.apib 

# Hoặc xuất ra file HTML tĩnh để đem đi chia sẻ offline
npx snowboard html api.apib -o index.html
```
*(⚠️ **Điểm yếu hệ sinh thái trên Windows**: Vì parser của API Blueprint sử dụng thư viện lõi viết bằng C++, khi chạy `npx` từ Windows máy sẽ cố gắng yêu cầu cài đặt VS Studio C++ và Python (node-gyp rebuild). Điều này hay gây ra lỗi cài đặt crash liên tục. Hãy dùng Cách 2 bên dưới).*

### Cách 2: Preview qua nền tảng Cloud Apiary
Copy toàn bộ text từ file `api.apib` và dán thẳng vào nền tảng editor chính thống [Apiary.io](https://app.apiary.io/).

---

## 3. Tự động sinh Python Code (Code Generation)

Vì API Blueprint thiếu hệ sinh thái sinh code Python native ổn định trên Windows, quy trình tốt nhất là thông qua cầu nối OpenAPI:

**Bước 1: Chuyển đổi API Blueprint sang OpenAPI v3**
Bạn có thể sử dụng công cụ `apib2swagger` qua môi trường Node.js. Cần nhớ thêm `-y` và cờ `--open-api-3` để output ra định dạng đúng nhé:
```bash

npx apib2swagger -i api.apib -o openapi.yaml -y --open-api-3

```

**Bước 2: Sinh toàn bộ Project FastAPI Server**
Sau khi đã có file `openapi.yaml`, chúng ta sẽ sử dụng công cụ `fastapi-code-generator` (được xây dựng dựa trên sức mạnh lõi của datamodel-codegen) để sinh ra hẳn một API có khả năng chạy ngay:
```bash
# Cài đặt công cụ bằng pip
pip install fastapi-code-generator

# Sinh ra project FastAPI vào thư mục api_app
fastapi-codegen --input openapi.yaml --output api_app
```
*(Lệnh này sẽ tự động khởi tạo thư mục `api_app` đính kèm file `main.py` chứa toàn bộ Router và `models.py` chứa Data Schema. Hãy chạy file main đó để có API Server thực thụ!)*

---

## 4. Khởi chạy Server Backend mới sinh (Tùy chọn)

Sau khi công cụ Code Generator tự động sinh ra module API, bạn có thể chạy thử mã nguồn (người thật, việc thật) để chứng minh tính chuẩn xác so với document của Blueprint.

**1. Cài đặt framework chạy Server:**
```bash
pip install fastapi uvicorn pydantic
```

**2. Kích hoạt Backend gốc:**
```bash
uvicorn api_app.main:app --reload
```
Server sẽ kích hoạt ở cổng **[http://localhost:8000](http://localhost:8000)**. Các API Endpoint như `GET /books` hay `POST /users` đã sẵn sàng ứng chiến!
*(Lưu ý: Công cụ sinh code sẽ xuất file `main.py` với cấu trúc relative package `from .models`, do đó chúng ta phải đứng từ ngoài gọi vào bằng `api_app.main` chứ không `cd` vào trong).*
