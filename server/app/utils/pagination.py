from sqlalchemy.orm import Query
from app.api.dependencies import PaginationParams

def paginate_query(query: Query, pagination: PaginationParams) -> dict:
    """Hàm lõi phân trang cho mọi loại truy vấn trả về phân trang"""
    total = query.count()
    
    offset = (pagination.page - 1) * pagination.size
    items = query.offset(offset).limit(pagination.size).all()
    
    total_pages = (total + pagination.size - 1) // pagination.size if pagination.size > 0 else 0
    
    return {
        "items": items,
        "total": total,
        "page": pagination.page,
        "size": pagination.size,
        "total_pages": total_pages
    }
