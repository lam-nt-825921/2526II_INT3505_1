from fastapi import FastAPI, Query
from typing import Optional
from models import Book
from schemas.cursor_based import CursorBasedResponse

app = FastAPI(title="Pagination Demo: Cursor-based", description="Demo chiến thuật phân trang Cursor-based cho API /books")

# Dữ liệu giả lập (Dummy data) cho Books
db_books = [
    Book(id=i, title=f"Sách lập trình {i}", author=f"Tác giả {i % 5}", status="available")
    for i in range(1, 101)
]

@app.get("/books", response_model=CursorBasedResponse[Book], tags=["Books"])
def get_books(
    cursor: Optional[int] = Query(None, description="ID của phần tử cuối cùng ở trang trước"), 
    limit: int = Query(20, ge=1, le=50, description="Số lượng phần tử tối đa trả về")
):
    """
    3. Cursor-based Pagination
    - Lấy danh sách sách sử dụng con trỏ (cursor) chỉ đến ID của phần tử cuối cùng đã biết.
    """
    start_index = 0
    if cursor is not None:
        # Tìm vị trí của cursor trong list
        for i, book in enumerate(db_books):
            if book.id == cursor:
                start_index = i + 1  # Lấy phần tử NGAY SAU cursor
                break

    items = db_books[start_index : start_index + limit]
    
    # Kiểm tra xem còn phần tử tiếp theo không
    has_next = (start_index + limit) < len(db_books)
    next_cursor = items[-1].id if items and has_next else None

    return CursorBasedResponse(
        items=items,
        next_cursor=next_cursor,
        has_next=has_next
    )
