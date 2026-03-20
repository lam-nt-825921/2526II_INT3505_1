# Hướng dẫn phần Demo OpenAPI

Tài liệu này đóng vai trò dẫn dắt bạn đi sâu vào cách cấu trúc, khởi tạo và trải nghiệm thực tế với định dạng **OpenAPI** — thông qua dự án quản lý thư viện mô phỏng (gồm 2 entities: *Book* & *User*).

---

## 1. Tìm hiểu Cấu trúc File OpenAPI
Một file đặc tả OpenAPI (như `openapi.yaml` hoặc `openapi.json`) thực chất là một sơ đồ ánh xạ trực tiếp các Endpoints và Data Models của hệ thống thành một khối dữ liệu có cấu trúc rành mạch. Dưới đây là các định danh cốt lõi giúp bạn đối chiếu qua lại giữa file và hệ thống thật:

### Các trường cốt lõi (Mô tả API Thực tế)
- **`paths`**: Là gốc rễ định nghĩa các Endpoints (ví dụ: `/books`, `/users`). Bên trong mỗi path sẽ được chia ra thành từng phương thức HTTP cụ thể (`get`, `post`, `put`, `delete`).
- **`parameters`**: Nằm bên trong cấu hình của từng phương thức HTTP, dùng để khai báo các biến mà server kỳ vọng nhận được. Nó có thể là **Path Parameters** (như `{id}`) hoặc **Query Parameters** (như `?status=available`).
- **`requestBody` & `responses`**: Mô tả chặt chẽ cấu trúc JSON của thân gửi lên (Payload) và dữ liệu chuẩn bị trả về. Khu vực `responses` luôn được phân cấp theo các mã HTTP Status Code rõ ràng (200, 201, 404...).
- **`components` & `schemas`**: Đây là linh hồn tạo nên tính **Modularity** (Tái sử dụng). Thay vì viết lại từng dòng khai báo thuộc tính dữ liệu ở nhiều API khác nhau, ta định nghĩa gom tụ mô hình `Book` vào mục `components/schemas`. Sau đó, bất cứ điểm nào cần cấu trúc `Book`, ta chỉ việc kế thừa qua con trỏ `$ref: '#/components/schemas/Book'`.

### Các trường siêu dữ liệu phục vụ Document (Metadata)
- **`openapi`**: Xác định phiên bản chuẩn kỹ thuật (Specification Version) đang được áp dụng (VD: `3.0.3` hoặc `3.1.0`).
- **`info`**: Chứa toàn bộ thông tin hiển thị định danh của hệ thống, bao gồm tựa đề (title), phiên bản app (version) và lời giới thiệu/mô tả.
- **`servers`**: Cung cấp danh sách các base URL có sẵn để thử nghiệm thực tế (chẳng hạn url cho môi trường Local, url Staging...).
- **`security` / `securitySchemes`**: *(Demo tuy chưa có Auth, nhưng đây là cấu trúc cực kỳ trọng điểm)*. Dùng để đăng ký các chuẩn phân quyền tổng quát áp dụng xuyên suốt API (VD: JWT Bearer Token, API Key, hay OAuth2).

---

## 2. Các phương pháp khởi tạo file OpenAPI

Dựa theo cách tiếp cận hiện đại, dự án này giới thiệu cho bạn 2 trường phái tạo ra file thiết kế:

### P.1: Phương pháp "Design-First" (Viết thủ công bằng tay)
- **Cách thức**: Bạn mở trình Text Editor và thận trọng gõ từng dòng định cấu trúc `openapi.yaml` dựa theo thiết kế hệ thống, sau đó code theo thiết kế đó hoặc dùng tools để sinh khung code.
- **Điểm mạnh**: Bộ khung file yaml này đóng vai trò như bản **Hợp đồng API (API Contract)**. Team Frontend Mobile/Web có thể bắt tay ghép nối giao diện vào Mock Server được sinh ra từ file này mà không cần chờ Backend code xong.

### P.2: Phương pháp "Code-First" (Dùng tools sinh tự động cực mạnh)
- **Cách thức**: Ở phương pháp này, bạn viết mã nguồn server (như file `main.py` dùng **FastAPI**), sau đó sử dụng các công cụ để tự động trích xuất hệ thống API đó ngược ra thành document.
- **Thực hành nhấn mạnh khả năng hỗ trợ**: OpenAPI quá uy tín và tiêu chuẩn đến mức các framework đều nỗ lực hỗ trợ tận răng. Hãy kiểm tra script chạy ngầm `generate_openapi.py`. Chạy file script này, hệ thống sẽ **phân tích (parse) cú pháp Python thực tế** và tự động nhả ra (dump) các file `openapi.json` hay `.yaml` hoàn hảo 100% về mặt format OpenAPI. Bạn không bao giờ phải lo việc "Tài liệu và Code bị lệch đồng bộ"!

---

## 3. Khởi chạy & Trình chiếu Swagger UI

**Bước 1: Cài đặt thư viện vận hành môi trường**
Mở terminal và đảm bảo rằng bạn đã cài đặt FastAPI và trình chạy server Uvicorn (cộng thêm `pyyaml` nếu muốn test script tạo yaml hồi nãy):
```bash
pip install fastapi uvicorn pydantic pyyaml
```

**Bước 2: Dựng Server mô phỏng**
Đứng tại khu vực thư mục `/0_OpenAPI/`, chạy lệnh sau để chạy máy chủ:
```bash
uvicorn main:app --reload
```
Hệ thống lúc này sẽ khởi chạy Backend của mô phỏng quản lý Thư viện tại cổng `8000`.

**Bước 3: Mở trình duyệt và vào Swagger UI gốc**
Truy cập thông qua trình duyệt tại đường dẫn:  **[http://localhost:8000/docs](http://localhost:8000/docs)**

Giao diện **Swagger UI** tự tích hợp trong FastAPI sẽ hiển thị:
1. Xem cấu trúc Models `Book` và `User` được Render trực quan.
2. Bấm thẳng nút **"Try it out"** ở bất kỳ endpoint nào (`GET /books`, `POST /users`...) để test API tương tác chạy thật nộp dữ liệu vào Local server.
