import sqlite3
import random
import time

DB_NAME = "benchmark.db"
TOTAL_RECORDS = 100_000

def seed_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Xoá bảng nếu đã tồn tại
    cursor.execute("DROP TABLE IF EXISTS books")
    
    # Tạo bảng
    cursor.execute("""
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    
    print(f"Bắt đầu seed {TOTAL_RECORDS} bản ghi để thử nghiệm phân trang...")
    start_time = time.time()
    
    # Chuẩn bị dữ liệu mẫu
    authors = ["John Doe", "Jane Smith", "Bob Martin", "Martin Fowler", "Robert C. Martin"]
    
    # Insert theo batch cho cực nhanh
    batch_size = 10000
    for i in range(0, TOTAL_RECORDS, batch_size):
        records = [
            (f"Cuốn sách số {j}", random.choice(authors), round(random.uniform(10.0, 100.0), 2))
            for j in range(i + 1, i + batch_size + 1)
        ]
        cursor.executemany(
            "INSERT INTO books (title, author, price) VALUES (?, ?, ?)",
            records
        )
        conn.commit()
        print(f" -> Đã insert {i + batch_size} bản ghi...")
        
    print(f"Hoàn tất trong {time.time() - start_time:.2f} giây.")
    conn.close()

if __name__ == "__main__":
    seed_database()
