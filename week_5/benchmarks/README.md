# Phân trang Cơ sở dữ liệu: Offset vs Cursor ⏱️

Thư mục này chứa bộ công cụ mô phỏng và **Benchmark (Đo đạc tốc độ)** để làm rõ lý do tại sao các hệ thống lớn (Facebook, Twitter) lại nói KHÔNG với phân trang Offset/Limit truyền thống ở các thiết kế API hiện đại.

## 🛠 Cách vận hành Demo (Dành cho Giảng Vấn/Sinh viên)

Với tư cách là người thuyết minh, bạn chỉ cần thực thi 3 bước sau:

### Bước 1: Khởi tạo Database giả lập
Kịch bản cần sinh ra 100,000 bản ghi để làm nổi bật sự khác biệt về tốc độ quét vòng lặp của Database.
```bash
python seed.py
```
*(Lệnh này sẽ tự động khởi dựng file `benchmark.db` nội bộ bằng chuẩn SQLite qua Raw Query trong tích tắc).*

### Bước 2: Kích hoạt API Server
Chạy máy chủ Backend mô phỏng tương tác truy vấn CSDL:
```bash
uvicorn api:app --port 8001
```

### Bước 3: Đo lường tốc độ (Benchmark)
Mở một tab Terminal mới và nã đạn vào Server để xem thời gian xử lý:
```bash
python benchmark.py
```

---

## 🧠 Phân tích kết quả (Kịch bản Giải thích)

Sau khi chạy `benchmark.py`, bảng kết quả Markdown sẽ hiện ra. Hãy bám vào đó để phân tích kiến trúc cho khán giả:

### 1. Chiến thuật - Không Phân Trang (`/books/no-page`)
Truy vấn trực tiếp Database để load `100,000` dòng. 
* **Nhược điểm:** Server mất nhiều trăm ms lãng phí CPU chỉ để Parse mảng data, chưa kể tốn hàng chục MB RAM/Network. 
* **Hậu quả:** Dễ gây sập Backend do OOM (Out Of Memory) hoặc thắt cổ chai đường truyền (Bandwidth Bottleneck) của client. 

### 2. Chiến thuật - Offset/Limit (`/books/offset`)
Khi người dùng cuộn tới cuối trang sâu, ví dụ lấy bản ghi mốc thứ `95,000`. Lệnh `OFFSET 95000 LIMIT 20` bắt ép Database phải **chạy đếm scan và vứt bỏ** toàn bộ `95,000` bản ghi trước đó để lọc ra được 20 dòng cuối.
* **Hậu quả:** Thời gian `Query Time` tỉ lệ thuận tuyến tính $\mathcal{O}(N)$ với độ sâu của trang hiện tại. Trang càng sâu -> Trải nghiệm người dùng càng chậm dần. Lãng phí số lượt Disk I/O khổng lồ vô ích.

### 3. Chiến thuật - Cursor Pagination (`/books/cursor`)
Cũng lấy dữ liệu mốc đó nhưng API đặt câu hỏi khác đi CSDL: *"Lấy cho tôi 20 bản ghi có Primary Key `id` lớn hơn cột mốc trên màn hình hiện tại (id > 95000)"*. 
* **Ưu điểm:** Nhờ bản chất cột `id` đã được đánh chỉ mục **B-Tree Index**, Database rẽ thẳng nhánh BTree đến vị trí node `95000` mất một lượng thời gian cố định cực nhỏ, tiệm cận $\mathcal{O}(1)$ hay chính xác hơn là $\mathcal{O}(\log n)$, hoàn toàn không cần quét bảng đếm từng dòng rác.
* **Kết quả Benchmark:** Tốc độ Cursor Pagination **nhanh gấp > 25 lần** Offset và luôn duy trì được tốc độ chớp nhoáng dẫu DB có nặng hàng tỷ Dữ Liệu!
