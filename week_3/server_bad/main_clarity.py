from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List

app = FastAPI(title="API Clarity Violations Demo")

users_db = [{"id": 1, "name": "Alice", "email": "alice@example.com", "created_at": "2023-10-27"}]
orders_db = [{"id": 101, "item": "Laptop", "price": 1000, "is_active": True}]

# 1. Vi phạm Ubiquitous Language (Ngôn ngữ chung)
# Thay vì dùng tên nghiệp vụ (ví dụ: Orders, Users), lại dùng tên kỹ thuật của Database
@app.get("/fetch_orders_db_records")
def get_records():
    return orders_db

# 2. Vi phạm Cognitive Load (Tải nhận thức) - Sử dụng từ viết tắt khó hiểu
@app.get("/u_actv_chk/{u_id}")
def check_user_status(u_id: int):
    for user in users_db:
        if user["id"] == u_id:
            return {"status": "Found"}
    return {"status": "Not Found"}

# 3. Rò rỉ chi tiết triển khai (Leaking Implementation Details)
# Lộ tên công nghệ (Python/List) và cấu trúc xử lý bên trong
@app.get("/get_python_list_of_users")
def list_users():
    return users_db

# 4. Vi phạm Intent-Based Naming (Đặt tên không dựa trên ý định)
# Thay vì đặt tên theo kết quả muốn đạt được, lại đặt tên theo hành động kỹ thuật chung chung
@app.post("/execute_data_op_v1")
def execute_operation(op_type: str = Query(..., description="1 for create, 2 for update")):
    return {"msg": f"Operation {op_type} executed"}

# 5. Dữ liệu trả về thiếu rõ ràng (Ambiguous Response Fields)
# Sử dụng các phím (keys) không có ý nghĩa hoặc quá ngắn
class BadResponse(BaseModel):
    id: int
    a: str   # Tên món hàng? Ghi chú?
    b: int   # Giá tiền? Trạng thái? Số lượng?

@app.get("/order_details/{id}", response_model=BadResponse)
def get_order(id: int):
    """
    Các trường 'a', 'b' trong JSON không có ý nghĩa nghiệp vụ. 
    Người dùng phải 'đoán' dữ liệu (a là tên item, b là giá).
    """
    for order in orders_db:
        if order["id"] == id:
            return {"id": id, "a": order["item"], "b": order["price"]}
    return {"id": id, "a": "Unknown", "b": 0}

# 6. Trộn lẫn các mối quan tâm (Mixing Concerns)
@app.get("/get_user_and_latest_order_and_system_status")
def get_everything():
    """
    Một endpoint cố gắng làm quá nhiều việc không liên quan, 
    khiến 'Clarity' về mục đích của tài nguyên bị phá vỡ hoàn toàn.
    """
    return {
        "user": users_db[0]["name"] if users_db else None, 
        "order": orders_db[0]["item"] if orders_db else None, 
        "system": "OK"
    }
