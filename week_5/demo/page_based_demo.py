from fastapi import FastAPI, Query
from models import Book
from schemas.page_based import PageBasedResponse

app = FastAPI(title="Pagination Demo: Page-based", description="Demo chiến thuật phân trang Page-based cho API /books")

# Dữ liệu giả lập (Dummy data) cho Books
db_books = [
    Book(id=i, title=f"Sách lập trình {i}", author=f"Tác giả {i % 5}", status="available")
    for i in range(1, 101)
]

@app.get("/books", response_model=PageBasedResponse[Book], tags=["Books"])
def get_books(
    page: int = Query(1, ge=1, description="Số trang hiện tại (bắt đầu từ 1)"), 
    size: int = Query(20, ge=1, le=50, description="Kích thước mỗi trang")
):
    """
    2. Page-based Pagination
    - Lấy danh sách sách dựa trên số trang (page) và kích thước trang (size).
    """
    offset = (page - 1) * size
    items = db_books[offset : offset + size]
    total_pages = (len(db_books) + size - 1) // size
    
    return PageBasedResponse(
        items=items,
        total=len(db_books),
        page=page,
        size=size,
        total_pages=total_pages
    )
