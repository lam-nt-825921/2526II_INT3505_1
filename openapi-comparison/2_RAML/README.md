# Hướng dẫn phần Demo RAML

Tài liệu này giới thiệu tổng quan về **RAML (RESTful API Modeling Language)**. Điểm mạnh lớn nhất của định dạng này là khả năng kế thừa và mô-đun hóa cực kỳ chặt chẽ, tối đa hóa nguyên lý không lặp lại mã (DRY - Don't Repeat Yourself).

---

## 1. Phân tích Cấu trúc File RAML
Trái ngược với YAML của OpenAPI thiên về cấu trúc phẳng, RAML tổ chức file (`api.raml`) giống như một cấu trúc cây thư mục ngầm, rất gọn gàng. Các thành phần chính bao gồm:

### Cấu hình Siêu dữ liệu (Metadata)
- **`#%RAML 1.0`**: Dòng đầu tiên bắt buộc phải có để định danh phiên bản RAML parser (cũng giống `FORMAT: 1A` của API Blueprint).
- **`title` & `version`**: Khai báo tên dự án và phiên bản API.
- **`baseUri`**: URL gốc của Endpoint máy chủ.

### Hệ thống Kế thừa (Bản sắc của định dạng RAML)
RAML cung cấp các công cụ mạnh mẽ để ép buộc lập trình viên không gõ lại code dư thừa:
- **`types`**: Tương tự `components` của OpenAPI hay `Data Structures` của Blueprint, là nơi chứa định nghĩa các schema dữ liệu (VD: `Book`, `User`).
- **`traits`** (Vô cùng quan trọng): Một khái niệm cực kỳ đặc trưng của RAML. Nó đóng vai trò giống như một "hàm" hay "mixin" chứa các parameter hoặc headers dùng chung (ví dụ: bộ lọc `status` hay tham số phân trang `page/limit`). Bất cứ endpoint nào cần bộ tham số đó, chỉ việc gọi con trỏ `is: [ trait_name ]`.

### Kịch bản Endpoints (Mô hình Cây)
RAML gộp chung Path và HTTP Method thụt lề lồng vào nhau thay vì tách riêng:
- Bắt đầu bằng tên đường dẫn cấp 1: `/books:`
- Lùi vào trong là phương thức: `get:` hay `post:`
- Lùi tiếp vào trong là chi tiết luồng xử lý: `responses:` -> `200:` -> `body:` -> `type: Book[]`.

---

## 2. Cách Render Giao diện RAML ra HTML

Giống hệ sinh thái API Blueprint, RAML là định dạng thiết kế gốc nên cần một trình biên dịch (compiler) để chuyển hóa mớ chữ YAML thành giao diện UI Web chuyên nghiệp dễ đọc. Công cụ phổ biến nhất của cộng đồng là **raml2html**.

### Quy trình Render tài liệu tĩnh HTML:
Giả định máy tính của bạn đã có cài sẵn Node.js và công cụ `npx`. Mở terminal ngay tại thư mục `2_RAML` và chạy câu lệnh sau:
```bash
npx raml2html api.raml -o index.html
```
*(Nếu là lần chạy đầu tiên, NPM có thể hỏi bạn muốn tải package không, hãy bấm `y`).*

Có thể xem file [index.html](./index.html) đã được render sẵn.

---

## 3. Khởi chạy Server Backend Minh họa (Tùy chọn)

Nếu bạn muốn chạy thử phần mock server xử lý dữ liệu backend đang đứng đằng sau tài liệu (mã nguồn được viết bằng FastAPI trong file `main.py`):

**1. Cài đặt:**
```bash
pip install fastapi uvicorn pydantic
```

**2. Khởi chạy Server Backend:**
```bash
uvicorn main:app --reload
```
Máy chủ lưu trữ sẽ liên tục chạy ngầm ở **[http://localhost:8000](http://localhost:8000)**. Lưu ý: Việc chạy server này thuần túy chỉ chứng minh rằng Code server tương tác chuẩn xác theo như tài liệu API đã thiết kế ở trên. Mọi giao diện tài liệu của bạn hãy xem dựa theo file `index.html` của `raml2html` nhé!

---

## 4. Tự động sinh Python Code (Code Generation)

Giống như API Blueprint, hệ sinh thái code generator native cho RAML (như `ramlfications`) đa số đã lỗi thời hoặc chạy không thực sự ổn định với Python 3 hiện đại trên Windows. Tối ưu nhất để lấy code chất lượng cao là hướng tiếp cận 2 bước:

**Bước 1: Chuyển đổi file RAML sang OpenAPI**
Bạn có thể sử dụng các utility compiler từ Node.js như `oas-raml-converter`:
```bash
npx oas-raml-converter --from RAML --to OAS30 api.raml > openapi.yaml
```

**Bước 2: Sinh toàn bộ Project FastAPI Server**
Khi đã thu được file `openapi.yaml`, thay vì chỉ sinh models tĩnh, ta sử dụng `fastapi-code-generator` của hệ sinh thái Python để sinh hẳn một Server API chạy thật sự:
```bash
# Cài đặt công cụ bằng pip
pip install fastapi-code-generator

# Tiến hành sinh cấu trúc project vào thư mục api_app
fastapi-codegen --input openapi.yaml --output api_app
```
*(Quá trình này sẽ tự tạo folder `api_app` chứa sẵn `main.py` API Router và `models.py` Schema Data chuẩn hoá hoàn toàn để bạn có thể chạy test server).*
