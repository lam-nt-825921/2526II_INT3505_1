import fastapi
from app.db.session import engine, Base
from app.api import api_router
from app.core.errors import AppException
from app.api.exception_handlers import (
    app_exception_handler, 
    validation_exception_handler, 
    global_exception_handler
)

Base.metadata.create_all(bind=engine)

app = fastapi.FastAPI(
    title="Library API",
    description="API quản lý thư viện sách trực tuyến, hỗ trợ Chủ sách và Người đọc theo chuẩn OpenAPI",
    version="1.0.0"
)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(fastapi.exceptions.RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Library API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=3000, reload=True)