from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from typing import Optional, Union, List
from datetime import datetime

app = FastAPI(title="API Consistency Violations Demo")

users_db = [{"id": 1, "name": "Alice", "email": "alice@example.com", "created_at": "2023-10-27"}]
orders_db = [{"id": 101, "item": "Laptop", "price": 1000, "is_active": True}]
reviews_db = [{"id": 1, "product_id": 101, "user_id": 1, "rating": 5, "content": "Tuyệt vời"}]

# 1. Vi phạm quy ước đặt tên (Naming Inconsistency)
# Hỗn hợp Case & Trộn lẫn Số ít và Số nhiều
@app.get("/user_profile")
def get_user_profile():
    return users_db[0]

@app.get("/v1/userAddress")
def get_user_address():
    return {"address": "123 Main St"}

# Dùng từ đồng nghĩa (user vs client) cho cùng 1 resource
@app.put("/client/{id}")
def update_client(id: int, name: str):
    users_db[0]["name"] = name
    return {"msg": f"Updated client {id}"}

# 2. Vi phạm cấu trúc Dữ liệu (Payload Inconsistency)
# Endpoint A trả về Envelope, Boolean true/false, Date ISO
@app.get("/orders")
def get_orders():
    return {
        "data": orders_db,
        "total": len(orders_db)
    }

# Endpoint B trả về trực tiếp Array, Boolean 1/0, Date Unix (Giả lập chung data orders)
@app.get("/latest_purchases") 
def get_latest_purchases():
    return [
         {"id": 101, "item": "Laptop", "price": 1000, "is_active": 1, "purchase_date": 1698381200}
    ]

# 3. Vi phạm mã lỗi và phản hồi (Status Code Inconsistency)
@app.get("/users/{id}")
def get_user(id: int, response: Response):
    if id != 1:
        # Lỗi 200 nhưng nội dung là Error
        # Cấu trúc lỗi 1
        return {"success": False, "error": "User not found"}
        
    return users_db[0]

@app.get("/orders/{id}")
def get_order(id: int, response: Response):
    if id != 101:
        # Dùng sai mã lỗi (400 thay vì 404 cho Not Found)
        # Cấu trúc lỗi 2
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"errors": [{"code": 404, "msg": "Order does not exist"}]}
        
    return orders_db[0]


# 4. Vi phạm phương thức HTTP (Method Inconsistency)
# Dùng GET để xóa dữ liệu
@app.get("/users/delete")
def delete_user_via_get(id: int):
    return {"message": f"Deleted user {id}"}

# Dùng POST lấy dữ liệu
@app.post("/users/get_all")
def get_all_users_via_post():
    return users_db

# 5. Vi phạm Nesting & Relationships (Nesting Inconsistency)
# Nesting quá sâu (Deep Nesting)
@app.get("/users/{user_id}/orders/{order_id}/products/{product_id}/reviews")
def get_deeply_nested_reviews(user_id: int, order_id: int, product_id: int):
    """
    Lỗi: Định tuyến /users/.../orders/.../products/.../reviews có cấu trúc quá lồng ghép (trên 2 cấp).
    Hậu quả: URL dài dòng, khó tái sử dụng, URL phụ thuộc quá nhiều vào ID trung gian (tight coupling).
    Đúng ra: Chỉ nên /products/{product_id}/reviews.
    """
    return reviews_db

# Query parameter thay vì đường dẫn cho resource con (Path vs Query)
@app.get("/get_reviews")
def get_reviews_by_query(product_id: int):
    """
    Lỗi: Dùng danh từ chung /get_reviews và truyền id qua Query thay vì dùng Nested Path.
    Hậu quả: Phá vỡ sự nhất quán của việc thiết kế resource phân cấp (Product chứa Reviews).
    Đúng ra: Dùng /products/{product_id}/reviews.
    """
    return [r for r in reviews_db if r["product_id"] == product_id]

# Đảo ngược quan hệ phi logic
@app.get("/reviews/{review_id}/product/{product_id}/user")
def get_user_from_review_and_product(review_id: int, product_id: int):
    """
    Lỗi: Lẫn lộn bậc quan hệ, đi ngược từ Review lên Product rồi vòng sang User trong cùng một URL.
    Hậu quả: Phá vỡ cấu trúc và ngữ nghĩa của REST (Hierarchy).
    """
    return users_db[0]

