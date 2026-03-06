### Kế hoạch cập nhật lên v3 stateless

## Hướng giải

- Thực hiện xây dựng server cung cấp API
- Thể hiện tính chất stateless bằng cách tạo tài nguyên User, yêu cầu người dùng xác nhận danh tính để quản lý các tài nguyên khác. (Như vậy hệ thống không cần biết lịch sử yêu cầu của người dùng, cứ mặc định mỗi yêu cầu đều phải gửi thông tin chứng minh danh tính)
- Xác thực danh tính bằng Jwt, người dùng gửi token qua Bearer Token trong header, server giải mã token để xác định danh tính người dùng

## Thiết kế API

**Kiến trúc API**
Để xây nên một server bài bản cần tạo cấu trúc logic, dễ bảo trì.

