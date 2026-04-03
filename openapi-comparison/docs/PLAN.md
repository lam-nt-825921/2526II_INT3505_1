## 🎼 Orchestration Plan: Tự động Sinh FastAPI Server từ OpenAPI YAML

### Bối cảnh (Context)
Ban đầu, quy trình đang sử dụng `datamodel-code-generator` - công cụ này rất mạnh nhưng **chỉ giới hạn ở mức sinh Data Models của Pydantic**, nó không hề tự động sinh ra các đoạn code route thực thi của máy chủ như `@app.get(...)` hay `@app.post(...)`. Để thật sự giải quyết được bài toán sinh ra "API chạy được", chúng ta cần đổi sang sử dụng một công cụ mạnh hơn của Python là `fastapi-code-generator`. 

Công cụ `fastapi-code-generator` có khả năng đọc nguyên bản file `openapi.yaml` của chúng ta và khởi tạo một project FastAPI server hoàn chỉnh (bao gồm thư mục, file `main.py` chạy uvicorn, và file `models.py`).

### Phase 1: Planning / Khảo sát (Hiện tại)
Tôi (dưới vai trò `project-planner`) đã thực hiện test thử phương pháp này và thành công. Lệnh `fastapi-codegen --input openapi.yaml --output api_app` thu được kết quả hoàn hảo, có đủ mã nguồn khởi chạy thay vì chỉ model chết.

### Phase 2: Implementation (Cập nhật hàng loạt)
Ngay khi bạn đồng ý, các "nhân sự" sẽ tiến hành làm việc song song để cập nhật Document & Demo:
1. **Frontend / Documentation Specialist (`frontend-specialist`)**: Sửa lại toàn bộ 3 file `README.md` của thư mục `1_APIBlueprint`, `2_RAML`, `3_TypeSpec`, đổi phần hướng dẫn tạo Code từ `datamodel-code-generator` (chỉ ra model) thành cấu trúc cài đặt module `fastapi-code-generator` sinh project FastAPI thực tế.
2. **Backend Specialist (`backend-specialist`)**: Sẽ chịu trách nhiệm chạy các command render API code thực tế bên trong thư mục demo của RAML và TypeSpec để làm bằng chứng (tạo ra thư mục `api_app` tại mỗi Spec).
3. **QA/Test Engineer (`test-engineer`)**: Kiểm định rằng tệp `main.py` được sinh ra không có lỗi cú pháp và khởi chạy được bằng lệnh uvicorn cơ bản.

---
Vui lòng xem và duyệt bản kế hoạch này để đi tiếp tới quá trình dàn xếp các chuyên viên (Phase 2).
