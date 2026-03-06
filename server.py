from fastapi import FastAPI

app = FastAPI()

# Dữ liệu giả lập (Mock Data)
db = {
    "1": {"name": "Laptop Gaming", "price": 2500, "brand": "Asus"},
    "2": {"name": "Macbook Air", "price": 1200, "brand": "Apple"}
}

@app.get("/")
def home():
    return {"message": "Chào mừng bạn đến với API của tôi!"}

@app.get("/product/{product_id}")
def get_product(product_id: str):
    if product_id in db:
        return {"status": "success", "data": db[product_id]}
    return {"status": "error", "message": "Không tìm thấy sản phẩm"}