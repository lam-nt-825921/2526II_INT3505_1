import fastapi
from app.db.session import engine, Base
from app.models import user, product, review
from app.api.routes import auth, products
from app.core.errors import AppException
from app.api.exception_handlers import (
    app_exception_handler, 
    validation_exception_handler, 
    global_exception_handler
)

Base.metadata.create_all(bind=engine)

app = fastapi.FastAPI(
    title="Bài tập tuần 2",
    description="Xây dựng REST API cơ bản, kết hợp với Postman để mô tả đặc trưng của REST",
    version="3.0.0"
)

# Đăng ký các Exception Handler thống nhất Response Format
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(fastapi.exceptions.RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Xác thực"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Sản phẩm"])

@app.get("/")
def read_root():
    return {"Hello": "World"}