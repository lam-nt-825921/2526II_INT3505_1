from fastapi import FastAPI, Query
from models import Book
from schemas.offset_limit import OffsetLimitResponse

app = FastAPI(title="Pagination Demo: Offset/Limit", description="Demo chiến thuật phân trang Offset/Limit cho API /books")

# Dữ liệu giả lập (Dummy data) cho Books
db_books = [
    Book(id=i, title=f"Sách lập trình {i}", author=f"Tác giả {i % 5}", status="available")
    for i in range(1, 101)
]

@app.get("/books", response_model=OffsetLimitResponse[Book], tags=["Books"])
def get_books(
    offset: int = Query(0, ge=0, description="Vị trí bắt đầu"), 
    limit: int = Query(20, ge=1, le=50, description="Số lượng phần tử tối đa trả về")
):
    """
    1. Offset/Limit Pagination
    - Lấy danh sách sách dựa trên số dòng bỏ qua (offset) và số dòng lấy (limit).
    """
    items = db_books[offset : offset + limit]
    return OffsetLimitResponse(
        items=items,
        total=len(db_books),
        offset=offset,
        limit=limit
    )
