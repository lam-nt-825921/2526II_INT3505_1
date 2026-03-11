from fastapi import FastAPI
from app.db.session import engine, Base
from app.models import user, product
from app.api.routes import auth, products

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bài tập tuần 2",
    description="Xây dựng REST API cơ bản, kết hợp với Postman để mô tả đặc trưng của REST",
    version="3.0.0"
)

app.include_router(auth.router, prefix="/auth", tags=["Xác thực"])
app.include_router(products.router, prefix="/products", tags=["Sản phẩm"])

@app.get("/")
def read_root():
    return {"Hello": "World"}