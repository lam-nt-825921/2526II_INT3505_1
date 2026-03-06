from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

class ProductUpdate(BaseModel):
    quantity: int | None = None
    price: int | None = None
    name: str | None = None

app = FastAPI()

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.txt")

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_db(db):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Lỗi lưu file: {e}")

@app.get("/")
def home():
    return {"message": "Chào mừng bạn đến với API của tôi!"}

@app.get("/product/{product_id}")
def get_product(product_id: str):
    db = load_db()
    if product_id in db:
        product_data = db[product_id].copy()
        # HATEOAS: Cung cấp URI cho Client biết thao tác tiếp theo
        product_data["buy_link"] = f"/product/{product_id}/buy"
        return {"status": "success", "data": product_data}
    return {"status": "error", "message": "Không tìm thấy sản phẩm"}

@app.post("/product/{product_id}/buy")
def buy_product(product_id: str):
    db = load_db()
    if product_id not in db:
        return {"status": "error", "message": "Không tìm thấy sản phẩm"}
        
    product = db[product_id]
    if product.get("quantity", 0) <= 0:
        return {"status": "error", "message": "Sản phẩm đã hết hàng!"}
        
    # Giảm số lượng
    product["quantity"] -= 1
    save_db(db)
    
    return {
        "status": "success", 
        "message": f"Mua thành công {product['name']}! Số lượng còn lại: {product['quantity']}"
    }

@app.patch("/product/{product_id}")
def update_product(product_id: str, payload: ProductUpdate):
    db = load_db()
    if product_id not in db:
        return {"status": "error", "message": "Không tìm thấy sản phẩm"}
        
    product = db[product_id]
    
    # Cập nhật các trường được gửi lên trong payload
    if payload.quantity is not None:
        product["quantity"] = payload.quantity
    if payload.price is not None:
        product["price"] = payload.price
    if payload.name is not None:
        product["name"] = payload.name
        
    save_db(db)
    
    return {
        "status": "success", 
        "message": f"Cập nhật thành công!",
        "data": product # Trả về bản đại diện mới nhất
    }