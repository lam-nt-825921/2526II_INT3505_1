Case study: Thiết kế chiến lược nâng cấp từ v1 sang v2 cho một API thanh toán
Viết thông báo deprecation cho developers


API đơn giản chỉ có các endpoint sau: 1 cái để rút tiền ra khỏi tài khoản, 1 cái nữa để xem lịch sử giao dịch, 1 cái để xem thông tin tài khoản (tên chủ sở hữu, số tài khoản, số dư), 1 endpoint đăng nhập, 1 endpoint đăng ký

API được viết bằng FastAPI, LiteSQL, ALchema

API được nâng cấp version là rút tiền ra khỏi tài khoản, break changes là sửa amount từ kiểu String thành Double/Float. 

Quy trình sẽ như sau: 
Viết hoàn thiện API v1 tại week_9/
Viết kế hoạch mirgrate plan tại week_9/PLAN.md
Thực hiện lần lượt theo kế hoạch đến khi xong, mỗi lần xong một bước sẽ ghi lại vào nhật ký ở week_9/ đồng thời chụp ảnh demo.


Lưu ý: kế hoạch phải có phần thông báo với đối tác(người dùng enpoint) bằng header và phần kế hoạch triển khai gồm các bước cơ bản như sau:
expand database để không ảnh hưởng v1
tạo route và controller cho v2
sửa logic ở service để dùng kiểu dữ liệu mới
code phiên dịch ở controller v1 để dùng được logic mới
cập nhật response của v1 để trả về header chuẩn mực (vẫn cập nhật ở controller v1)


kế hoạch là sẽ đóng hoàn toàn v1 vào: Wed, 31 Dec 2026;