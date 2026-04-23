# Hướng dẫn Load Test & Tìm Break Point (Week 8)

Tài liệu này hướng dẫn cách thực hiện load test cho Library API ngay trên máy cấu hình yếu để tìm ra giới hạn của hệ thống.

---

## 1. Chuẩn bị (Preparation)

### Bước 1: Khởi tạo dữ liệu Test
Do Database đang rỗng, bạn cần chạy script seed để tạo tài khoản `admin` và một số dữ liệu mẫu:
```bash
cd server
python seed_test.py
```

### Bước 2: Cài đặt công cụ
1. **Cài đặt Locust** (Dùng để chạy kịch bản Python):
   ```bash
   pip install locust requests
   ```

2. **Cài đặt `hey`** (Dùng để tìm Break Point - Cực kỳ quan trọng):
   - **Cách 1 (Nhanh nhất):**
     1. Tải trực tiếp file này: [hey_windows_amd64](https://storage.googleapis.com/hey-releases/hey_windows_amd64)
     2. Sau khi tải về, bạn sẽ có một file tên là `hey_windows_amd64`.
     3. Bạn hãy **đổi tên nó thành `hey.exe`**.
     4. Copy file `hey.exe` này vào thư mục dự án (ngang hàng với file `locustfile.py`).
     5. Mở Terminal tại thư mục đó và gõ `.\hey.exe` để kiểm tra.

---

## 2. Chạy Server ở chế độ tối ưu (Optimized Server)
Khi test tải, chúng ta cần tắt bớt log để Server tập trung xử lý request:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 3000 --no-access-log
```

---

## 3. Thực hiện Load Test với Locust (Scenario Testing)

Locust giúp giả lập luồng người dùng thực tế (Login -> Xem sách -> Profile).

1. Mở một terminal mới tại thư mục gốc dự án và chạy:
   ```bash
   locust -f locustfile.py --host http://localhost:3000
   ```
2. Truy cập: `http://localhost:8089` trên trình duyệt.
3. **Thông số đề xuất cho máy yếu:**
   - **Number of users:** 200
   - **Spawn rate:** 5 (tăng dần 5 user mỗi giây)
4. **Quan sát:**
   - **RPS (Requests Per Second):** Tốc độ xử lý của hệ thống.
   - **Response Time:** Nếu đường màu vàng tăng vọt lên trên 1000ms, server bắt đầu quá tải.

---

## 4. Tìm Break Point cực nhanh (Tự động hóa)

Để không phải copy token thủ công, hãy sử dụng script tổng hợp sau. Script này sẽ: **Tự động Login -> Lấy Token -> Gọi lệnh `hey` (hoặc `ab`)**.

```bash
python server/stress_test.py
```

*Lưu ý: Nếu máy bạn chưa có `hey`, script sẽ cố gắng dùng `ab` (có sẵn trong XAMPP). Nếu không có cả hai, bạn nên cài `hey` để có kết quả đo chính xác nhất.*

---

## 5. Cách đọc kết quả (Interpreting Results)

- **Thành công:** Hầu hết Request trả về code 200.
- **Break Point (Điểm gãy):** 
    - Khi bạn tăng User nhưng **RPS không tăng thêm** mà **Latency (độ trễ) tăng vọt**.
    - Server bắt đầu trả về lỗi `500 Internal Server Error` hoặc `Connection Refused`.
    - CPU của máy chạy Server đạt 100%.

**Lưu ý:** Với SQLite, nếu bạn test các API có Ghi dữ liệu (POST/PUT), điểm gãy sẽ đến sớm hơn rất nhiều do cơ chế khóa (locking) của SQLite.
