# Kế Hoạch Kiểm Thử API với Postman & Newman

Tài liệu này định nghĩa chi tiết các kịch bản kiểm thử dựa trên dữ liệu từ `seed_test.py` và cấu trúc lỗi trong `errors.py`.

## Cấu hình Môi trường (Environment Variables)
- `baseUrl`: `http://localhost:3000/api/v1`
- `admin_token`: Lưu tự động sau khi login admin.
- `user1_token`: Lưu tự động sau khi login user1.
- `others_book_id`: ID sách của `user2` (Lấy từ kết quả Lấy tất cả sách).
- `my_book_id`: ID sách do `user1` tạo ra.
- `non_existent_book_id`: ID sách không tồn tại (Tính bằng `others_book_id - 1`).

---

## 1. Nhóm API: Authentication (Công khai)

### 1.1 Đăng ký hợp lệ
- **Method:** `POST`
- **URL:** `{{baseUrl}}/public/auth/register`
- **Body (JSON):**
```json
{
    "username": "user1",
    "email": "user1@example.com",
    "password": "user123",
    "name": "User One",
    "phone": "0123456789"
}
```
- **Scripts (Tests):**
```javascript
pm.test("Status code is 200", () => pm.response.to.have.status(200));
```

### 1.2 Đăng ký thiếu trường dữ liệu
- **Method:** `POST`
- **Body (JSON):** `{"username": "fail"}`
- **Scripts (Tests):**
```javascript
pm.test("Lỗi 422 - Thiếu dữ liệu", () => pm.response.to.have.status(422));
```

### 1.3 Đăng ký sai định dạng email
- **Method:** `POST`
- **Body (JSON):** `{"username": "user_bad", "email": "sai-format", "password": "123", "name": "A", "phone": "1"}`
- **Scripts (Tests):**
```javascript
pm.test("Lỗi 422 - Email sai định dạng", () => pm.response.to.have.status(422));
```

### 1.4 Đăng ký tài khoản đã tồn tại
- **Method:** `POST`
- **Body (JSON):** Gửi lại dữ liệu của `user1` ở mục 1.1.
- **Scripts (Tests):**
```javascript
pm.test("Lỗi 400 - Tài khoản đã tồn tại", () => {
    pm.response.to.have.status(400);
    pm.expect(pm.response.json().detail).to.eql("AUTH_1001");
});
```

### 1.5 Đăng nhập thành công (Admin)
- **Method:** `POST`
- **URL:** `{{baseUrl}}/public/auth/login`
- **Body (form-data):** `username: admin`, `password: admin123`
- **Scripts (Tests):**
```javascript
pm.test("Lấy token Admin thành công", () => {
    pm.response.to.have.status(200);
    pm.environment.set("admin_token", pm.response.json().access_token);
});
```

### 1.6 Đăng nhập thành công (User 1)
- **Method:** `POST`
- **Body (form-data):** `username: user1`, `password: user123`
- **Scripts (Tests):**
```javascript
pm.test("Lấy token User 1 thành công", () => {
    pm.response.to.have.status(200);
    pm.environment.set("user1_token", pm.response.json().access_token);
});
```

### 1.7 Đăng nhập sai tài khoản/mật khẩu
- **Method:** `POST`
- **Body (form-data):** `username: user1`, `password: wrongpass`
- **Scripts (Tests):**
```javascript
pm.test("Lỗi 401 - Sai thông tin", () => {
    pm.response.to.have.status(401);
    pm.expect(pm.response.json().detail).to.eql("AUTH_1002");
});
```

### 1.8 Đăng nhập với dữ liệu trống
- **Method:** `POST`
- **Body (form-data):** (Để trống fields)
- **Scripts (Tests):**
```javascript
pm.test("Lỗi 422 - Dữ liệu trống", () => pm.response.to.have.status(422));
```

---

## 2. Nhóm API: Books (Công khai & Riêng tư)

### 2.1 Lấy tất cả sách
- **Method:** `GET`
- **URL:** `{{baseUrl}}/public/books`
- **Scripts (Tests):**
```javascript
pm.test("Lấy danh sách thành công", () => {
    pm.response.to.have.status(200);
    var firstBook = pm.response.json().items[0];
    pm.environment.set("others_book_id", firstBook.id);
    pm.environment.set("non_existent_book_id", firstBook.id - 1);
});
```

### 2.2 Lấy sách theo bộ lọc
- **Method:** `GET`
- **URL:** `{{baseUrl}}/public/books?q=User 2`
- **Scripts (Tests):**
```javascript
pm.test("Filter thành công", () => pm.response.to.have.status(200));
```

### 2.3 Xem chi tiết sách
- **Method:** `GET`
- **URL:** `{{baseUrl}}/public/books/{{others_book_id}}`
- **Scripts (Tests):**
```javascript
pm.test("Xem chi tiết thành công", () => pm.response.to.have.status(200));
```

### 2.4 Xem chi tiết sách không tồn tại
- **Method:** `GET`
- **URL:** `{{baseUrl}}/public/books/{{non_existent_book_id}}`
- **Scripts (Tests):**
```javascript
pm.test("Lỗi 404 - Không tìm thấy", () => {
    pm.response.to.have.status(404);
    pm.expect(pm.response.json().detail).to.eql("ERR_4004");
});
```

### 2.5 Tạo sách mới nhưng thiếu token
- **Method:** `POST`
- **URL:** `{{baseUrl}}/private/books`
- **Scripts (Tests):**
```javascript
pm.test("Lỗi 401 - Thiếu token", () => pm.response.to.have.status(401));
```

### 2.6 Tạo sách mới nhưng sai token
- **Method:** `POST`
- **Header:** `Authorization: Bearer sai_token`
- **Scripts (Tests):**
```javascript
pm.test("Lỗi 401 - Sai token", () => pm.response.to.have.status(401));
```

### 2.7 Tạo sách mới thành công
- **Method:** `POST`
- **Header:** `Authorization: Bearer {{user1_token}}`
- **Body (JSON):**
```json
{
    "title": "Sách của User 1",
    "author": "User 1",
    "price": 100,
    "stock": 10
}
```
- **Scripts (Tests):**
```javascript
pm.test("Tạo sách thành công", () => {
    pm.response.to.have.status(201);
    pm.environment.set("my_book_id", pm.response.json().id);
});
```

### 2.8 Tạo sách với dữ liệu không hợp lệ
- **Method:** `POST`
- **Body (JSON):** `{"title": "", "price": -10}`
- **Scripts (Tests):**
```javascript
pm.test("Lỗi 422 - Data không hợp lệ", () => pm.response.to.have.status(422));
```

### 2.9 Cập nhật sách của bản thân
- **Method:** `PUT`
- **URL:** `{{baseUrl}}/private/books/{{my_book_id}}`
- **Header:** `Authorization: Bearer {{user1_token}}`
- **Body (JSON):** `{"title": "Tiêu đề đã sửa"}`
- **Scripts (Tests):**
```javascript
pm.test("Cập nhật thành công", () => pm.response.to.have.status(200));
```

### 2.10 Cập nhật sách của người khác
- **Method:** `PUT`
- **URL:** `{{baseUrl}}/private/books/{{others_book_id}}`
- **Header:** `Authorization: Bearer {{user1_token}}`
- **Body (JSON):** `{"title": "Hacker cố sửa"}`
- **Scripts (Tests):**
```javascript
pm.test("Lỗi 403 - Sai quyền", () => {
    pm.response.to.have.status(403);
    pm.expect(pm.response.json().detail).to.eql("ERR_4003");
});
```

### 2.11 Admin xóa sách
- **Method:** `DELETE`
- **URL:** `{{baseUrl}}/private/books/admin/force-delete/{{others_book_id}}`
- **Header:** `Authorization: Bearer {{admin_token}}`
- **Scripts (Tests):**
```javascript
pm.test("Admin xóa thành công", () => pm.response.to.have.status(204));
```
