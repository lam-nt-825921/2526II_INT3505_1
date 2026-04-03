# Hướng dẫn phần Demo TypeSpec

Tài liệu này đánh giá **TypeSpec** - ngôn ngữ thiết kế API hiện đại nhất do công ty Microsoft đứng sau phát triển. Điểm "Ăn tiền" nhất của TypeSpec là nó mang lại cảm giác cực kỳ thân thuộc cho mọi lập trình viên nhờ vay mượn hệ thống cú pháp siêu mạnh của **TypeScript / C#**.

---

## 1. Phân tích Cấu trúc File TypeSpec
Nếu bạn là dân hệ Code, chỉ cần lướt qua file `main.tsp` là tự động hiểu liền hệ thống đang thiết kế gì mà không cần học bất cứ luật lệ nào mới:

### Khai báo Module & Siêu dữ liệu
- TypeSpec hỗ trợ module hóa hoàn hảo qua từ khóa `import` thư viện và `using` ở đầu file. Tính modularity của nó là đỉnh cao nhất trong 4 công cụ khảo sát.
- Định nghĩa Metadata API qua các Decorator (hậu tố `@`): như `@service`, `@server`. Mọi thứ đều được gói trong một `namespace` riêng.

### Hệ thống Data Models
- Sử dụng cú pháp `model` và `enum` y hệt như interface của Typescript.
- Định dạng kiểu dữ liệu tĩnh nghiêm ngặt (`int32`, `string`).

### Khai báo Endpoints "như viết Code"
Thay vì bóp lồi lõm mớ YAML hay chèn lồng Header phức tạp, TypeSpec sử dụng khái niệm `interface`:
- Bạn có thể dùng decorator `@route("/books")` đặt trên đầu của `interface Books` để thiết lập URL chung.
- Ở các hàm nội bộ bên trong, khai báo hành động bằng các Decorator Method: `@get list(@query status?: BookStatus): Book[]`. Ý nghĩa lập trình API thể hiện cực kỳ trơn tru, mạch lạc.

---

## 2. Cách Biên dịch (Compile) TypeSpec

Khác với RAML hay API Blueprint biến tài liệu thành giao diện trực tiếp, triết lý thiết kế của Microsoft biến **TypeSpec thành một trạm phát điện cốt lõi**. TypeSpec sẽ được "Compile" biên dịch xuất ngược ra định dạng trung gian tiêu chuẩn **OpenAPI v3** (yaml). 

Cú pháp viết thì cực sướng của TypeSpec + Giao diện UI đồ sộ Swagger của hệ sinh thái OpenAPI = Sự kết hợp hoàn hảo!

### Bước 1: Cài đặt công cụ môi trường Node.js
Trong Project minh họa thư mục `3_TypeSpec`, tôi đã viết sẵn `package.json` và `tspconfig.yaml`. Bạn chỉ việc tải module xuống chuẩn bị để TypeSpec chạy:
```bash
npm install
```

### Bước 2: Build sang tệp OpenAPI YAML tiêu chuẩn
Hệ thống compiler mạnh mẽ nhất của TypeSpec sẽ tiến hành build file:
```bash
npx tsp compile main.tsp
```
Sau ~1 giây, TypeSpec sẽ check tĩnh lỗi của toàn bộ dự án, và sinh ra một folder mới có tên là **`tsp-output`**. Bên trong thư mục đó chính là lõi file `openapi.yaml` đạt chuẩn cấu trúc OpenAPI cao nhất do chính Microsoft đóng dấu. 

Giờ đây bạn có thể thoải mái quăng file OpenAPI yaml đó vào trong Swagger UI hoặc đưa vào các tool Gen-Code để tiếp tục workflow như ở thư mục OpenAI bài 1!

---

## 3. Tự động sinh Python Code (Code Generation)

Vì TypeSpec được thiết kế theo tư duy hiện đại, tính mở rộng là vô tận. Nó sở hữu hệ thống các **Emitter** (Bộ xuất code) riêng biệt do Microsoft hoặc cộng đồng tạo ra, cho phép gen Python Code Client Native cực kỳ sạch.

**Bước 1: Cài đặt Plugin Python Emitter**
Tải plugin dành riêng cho Python vào nội hàm dự án thông qua Node.js:
```bash
npm install @typespec/http-client-python --save-dev
```

**Bước 2: Cập nhật cấu hình `tspconfig.yaml`**
Mở file `tspconfig.yaml` ra và thêm đuôi bộ build cho Python vào khối `emit` để trình compiler biết mục đích của chúng ta:
```yaml
emit:
  - "@typespec/openapi3"
  - "@typespec/http-client-python"
```

**Bước 3: Thu hoạch Code**
Chạy quy trình Build dự án lần nữa:
```bash
npx tsp compile main.tsp
```
Trình biên dịch sẽ tự động bắt đầu quá trình và sinh ra một Client SDK chuẩn Python trong thư mục hệ thống con `tsp-output`.

Bộ code này cực kỳ chuyên nghiệp và cũng là chuẩn giao tiếp mà các dev nội bộ Azure SDK đang sử dụng!. Dĩ nhiên, nếu dự định của bạn là sinh nhánh **Server** (FastAPI) thay vì nhánh **Client**, bạn không cần tải plugin `http-client-python`. 

Hãy linh hoạt lấy đúng file trung gian OpenAPI `openapi.yaml` (sinh ra ở thư mục `tsp-output`) và chạy phối hợp với công cụ `fastapi-code-generator` của hệ sinh thái Python:
```bash
# Cài đặt bằng pip
pip install fastapi-code-generator

# Chạy lệnh xuất file lấy source là file trong thẻ output:
fastapi-codegen --input tsp-output/openapi.yaml --output api_app
```
*(Sau lệnh này bạn sẽ thu được thẳng thư mục `api_app` có sẵn API `main.py` chạy uvicorn ngay lập tức!)*

---

## 4. Khởi chạy Server Backend mới sinh (Tùy chọn)

Python FastAPI Backend Mockup luôn là bảo chứng mạnh mẽ của dự án! Hãy xem code vừa được TypeSpec/OpenAPI Generate ra từ API Schema chạy mượt mà thế nào:

**Cài đặt framework & Khởi chạy:**
```bash
pip install fastapi uvicorn pydantic

cd api_app
uvicorn main:app --reload
```
Máy chủ lưu trữ sẽ chạy tại cổng [http://localhost:8000](http://localhost:8000/docs).
