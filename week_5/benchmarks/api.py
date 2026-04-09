from fastapi import FastAPI, Query
import sqlite3
import time

app = FastAPI(title="Pagination Speed Benchmark API")

DB_NAME = "benchmark.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/books/no-page")
def get_books_no_page(limit: int = Query(100000)):
    """
    Chiến thuật 1: KHÔNG PHÂN TRANG
    Rút thẳng một lượng khổng lồ. 
    """
    conn = get_db_connection()
    start_time = time.time()
    
    # Raw SQL
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books LIMIT ?", (limit,))
    rows = cursor.fetchall()
    
    elapsed = time.time() - start_time
    conn.close()
    
    return {
        "strategy": "No Pagination",
        "db_query_time_ms": elapsed * 1000,
        "count_fetched": len(rows),
        "data": [dict(r) for r in rows]
    }

@app.get("/books/offset")
def get_books_offset(offset: int = Query(90000), limit: int = 20):
    """
    Chiến thuật 2: OFFSET PAGINATION (Cách Cũ)
    Lấy offset 90k, tức là bắt DB quét và SKIP 90k dòng trước khi lấy 20 dòng.
    """
    conn = get_db_connection()
    start_time = time.time()
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books LIMIT ? OFFSET ?", (limit, offset))
    rows = cursor.fetchall()
    
    elapsed = time.time() - start_time
    conn.close()
    
    return {
        "strategy": "Offset Pagination",
        "offset_used": offset,
        "db_query_time_ms": elapsed * 1000,
        "count_fetched": len(rows),
        "data": [dict(r) for r in rows]
    }

@app.get("/books/cursor")
def get_books_cursor(cursor_id: int = Query(90000), limit: int = 20):
    """
    Chiến thuật 3: CURSOR PAGINATION (Cách Tối Ưu)
    Nhảy thẳng đến mốc `id = 90000` thông qua Index Primary Key B-Tree.
    """
    conn = get_db_connection()
    start_time = time.time()
    
    cursor = conn.cursor()
    # Dùng WHERE id > thay vì offset
    cursor.execute("SELECT * FROM books WHERE id > ? ORDER BY id ASC LIMIT ?", (cursor_id, limit))
    rows = cursor.fetchall()
    
    elapsed = time.time() - start_time
    conn.close()
    
    return {
        "strategy": "Cursor Pagination",
        "cursor_used": cursor_id,
        "db_query_time_ms": elapsed * 1000,
        "count_fetched": len(rows),
        "data": [dict(r) for r in rows]
    }
