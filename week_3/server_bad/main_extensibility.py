from fastapi import FastAPI, HTTPException, Request

app = FastAPI(title="API Design Bad Practices: Extensibility")

users_db = [{"id": 1, "name": "Alice", "email": "alice@example.com", "status": "active"}]
products_db = [{"id": 101, "name": "Laptop", "price": 1000, "stock": 5}]

# Vi phạm extensibility
# Làm hỏng ứng dụng khách hàng khi hệ thống tiến hóa.

# 1. Thiếu Versioning ngay từ đầu (No Versioning)
# Không có không gian tên phiên bản (ví dụ: /v1/) trong URL.
# Khi có thay đổi đột phá (breaking change), không có cách nào định tuyến client cũ 
# và client mới tới hai logic khác nhau, buộc phải ghi đè trực tiếp lên endpoint hiện tại 
# và làm sập các ứng dụng khách.
@app.get("/users/{id}")
def get_user(id: int):
    # Trước đây có thể trả về thông tin user chi tiết, sau này muốn rút gọn hoặc thay đổi 
    # cấu trúc tại endpoint này sẽ ngay lập tức làm hỏng các client cũ do thiếu versioning.
    return users_db[0]


# 2. Thay đổi cấu trúc dữ liệu làm hỏng Client (Breaking Structural Change)
# Giả sử trước đây trả về trường "name". Nay Sếp yêu cầu tách ra "first_name" và "last_name".
# Lỗi: Xóa trường "name" cũ. Các App đang dùng `user.name` sẽ bị lỗi 'undefined'.
# Đúng ra: Phải giữ trường 'name' (additive change) để tương thích ngược 
# và thêm 2 trường mới, hoặc tạo một endpoint ở /v2/.
@app.get("/v1/profile-updated-bad")
def get_profile_breaking():
    """
    Cấu trúc cũ từng trả về:
    {
        "id": 1,
        "name": "Alice", # Client cũ đang phụ thuộc vào trường "name" này
        "email": "alice@example.com"
    }
    """
    return {
        "id": 1,
        "first_name": "Alice", # BAD: Đột ngột xóa trường 'name' và thay thế
        "last_name": "Smith",
        "email": "alice@example.com"
    }


# 3. Thay đổi kiểu dữ liệu (Data Type Change)
# Lỗi: Trước đây "price" là số (1000). Nay đổi thành object để thêm đơn vị tiền tệ.
# Hậu quả: Client cũ đang thực hiện phép tính (ví dụ: price * 1.1) sẽ bị crash vì 
# không thể thực hiện phép toán trên một Object.
@app.get("/products/{id}")
def get_product_breaking(id: int):
    """
    Dữ liệu cũ từng trả về:
    {
        "id": 101,
        "name": "Laptop",
        "price": 1000 # Kiểu Số nguyên (Integer)
    }
    """
    return {
        "id": 101,
        "name": "Laptop",
        "price": {"amount": 1000, "currency": "USD"} # BAD: Đổi kiểu dữ liệu sang Object
    }


# 4. Vi phạm Luật Postel (Strict Validation)
# Lỗi: Client gửi thêm một trường mới (ví dụ: 'note') mà Server chưa biết.
# Thay vì bỏ qua (ignore) các trường không xác định, Server lại trả về báo lỗi HTTP 400. 
# Điều này ngăn cản Client nâng cấp, gửi thêm payload chuẩn bị cho tương lai trước Server.
@app.post("/orders/strict")
async def create_order_strict(request: Request):
    data = await request.json()
    allowed_fields = {"product_id", "quantity"}
    
    # Kiểm tra cực đoan: Nếu có bất kỳ trường lạ nào là báo lỗi ngay
    for key in data.keys():
        if key not in allowed_fields:
            raise HTTPException(status_code=400, detail=f"Trường {key} không hợp lệ!")
    
    return {"status": "Created"}
