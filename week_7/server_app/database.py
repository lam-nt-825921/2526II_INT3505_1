from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Nạp các biến môi trường từ file .env
load_dotenv()

# Lấy đường dẫn từ .env (nếu không có thì dùng dạng rỗng)
MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise ValueError("❌ Lỗi: Bạn chưa cung cấp 'MONGO_URL' trong file .env")

client = MongoClient(MONGO_URL)
cols = client.shop_db

def get_db():
    try:
        yield cols
    finally:
        pass
