# 1. So sánh JWT và OAuth 2.0 & Ý nghĩa của Bearer Token

Trong phát triển Web API, chúng ta cần cơ chế xác thực rốt ráo vì HTTP mặc định là vô trạng thái (Stateless). **Bearer Token** là "chìa khóa" phổ biến nhất, giúp server nhận diện Client mà không cần phải gọi Database để xác thực thông tin user name/password trong từng request.

## 1.1 Bearer Token là gì?

**Bearer Token** dịch nôm na là "Token của người mang/chứa nó". 
Giống như việc bạn cầm một tấm vé xem phim: nhân viên rạp không cần biết TÊN bạn là gì, chỉ cần bạn CÓ CẦM vé (bearer) hợp lệ, họ sẽ cho bạn vào.

Trong HTTP Request, Bearer Token được gửi trong Header:
```http
Authorization: Bearer <token_string_ở_đây>
```

> [!WARNING]
> Vì đặc tính "Ai cầm nó thì là chủ nhân", nếu token bị lộ (Leakage), kẻ gian hoàn toàn có thể giả mạo danh tính của bạn. Do đó, Bearer Token LUÔN LUÔN phải được gửi qua đường truyền mã hóa chuẩn **HTTPS**.

---

## 1.2 Json Web Token (JWT)

**JWT (JSON Web Token)** là một định dạng cụ thể, mã hóa thành chuỗi (để dùng làm Bearer token).

**Đặc điểm:** Tự chứa dữ liệu (Self-contained). Nó lưu sẵn thông tin của User (như ID, Role). Khi gửi JWT lên, Server giải mã nó và biết ngay ông A thuộc Role B mà **KHÔNG CẦN CHỌC VÀO DATABASE**.

### Cấu trúc JWT (3 phần)
Một JWT gồm 3 phần cách nhau bằng dấu chấm `.`: `Header.Payload.Signature`

1. **Header:** Chứa thuật toán mã hóa (VD: HS256).
2. **Payload:** Chứa claims (dữ liệu thật sự như `user_id`, `role`, `nbf`, `exp` - hạn dùng).
3. **Signature:** Chữ ký số dùng để **chống giả mạo**. Nếu kẻ thù sửa Payload, chữ ký sẽ không khớp! (Server sinh chữ ký bằng `SECRET_KEY`).

> [!CAUTION]
> JWT có thể được giải mã (Base64 decode) để đọc Payload. Đừng bao giờ lưu Data nhạy cảm (Password, mã số thẻ) trong Payload. Hãy xem file `demo_1_jwt_anatomy.py` để hình dung.

---

## 1.3 OAuth 2.0 là gì?

Nhiều người lầm tưởng JWT và OAuth 2.0 là 2 đối thủ cạnh tranh, kiểu "Dùng JWT hay dùng OAuth?". Thực tế, chúng **không cùng đẳng cấp**.
- **JWT** là ĐỊNH DẠNG một cái "Thẻ chứng minh" (Token format).
- **OAuth 2.0** là MỘT QUY TRÌNH (Framework/Protocol) hướng dẫn CÁCH CẤP/CHIA SẺ CÁI THẺ ĐÓ cho bên thứ 3 an toàn.

**Ví dụ bài toán thư viện:**
Bạn (`User`) sử dụng website A.
Website A yêu cầu lấy danh sách sách đã mượn của bạn từ ứng dụng Thư Viện (`Server`).
- Nếu dùng cơ chế mật khẩu, Trang A sẽ đòi bạn gõ Mật khẩu Thư viện của bạn. Cực kì nguy hiểm!
- **Giải pháp OAuth 2.0:** Bạn đăng nhập thẳng ở màn hình của Thư Viện, sau đó Thư viện sẽ cấp một cái **Access Token** (thường format chính là JWT) cho trang A. Trang A cầm thẻ JWT đó để đọc sách của bạn thay mặt bạn!

---

## 1.4 Bảng so sánh dễ hiểu

| Tiêu chí | JWT | OAuth 2.0 |
| :--- | :--- | :--- |
| **Bản chất** | Một định dạng chuỗi token mang theo dữ liệu (Format). | Một quy trình ủy quyền (Protocol/Framework). |
| **Vai trò** | Là "tấm vé" (Vé vào cửa chứa thông tin). | Là quy trình "xin/phát vé/ủy quyền". |
| **Mục đích** | Truyền tải thông tin an toàn giữa các bên (Authentication). | Cấp quyền cho app bên thứ 3 truy cập tài nguyên (Authorisation). |
| **Độ phức tạp** | Rất dễ triển khai: Client login -> Server trả JWT. | Phức tạp (Cần Authorization Server, Client ID, Secret, callback...). |
| **Khả năng ứng dụng**| Dùng làm Access Token bên trong quá trình OAuth 2.0. | Xây dựng tính năng "Login with Google", "Login with Facebook". |

---

## 1.5 Kết luận

Trong API `Server` của chúng ta, các endpoint như gọi phiếu mượn `/loans/` không cần uỷ quyền cho bên thứ 3. Do đó, ta **chỉ cần áp dụng JWT (Authentication) cơ bản**, không cần cài toàn bộ flow OAuth 2.0 phức tạp. Tuy nhiên, theo quy ước của FastAPI, cơ chế nhận Token từ form login sẽ sử dụng scheme `OAuth2PasswordBearer` (Một nhánh flow nhỏ nhất của OAuth2 nhằm sinh token và gán cho Bearer).
