import requests
import sys
import os

# Thêm đường dẫn để gọi được seed_test nếu cần
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def get_access_token():
    url = "http://localhost:3000/api/v1/auth/login"
    payload = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        print("--- Đang lấy Access Token ---")
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            print("✅ Lấy token thành công!")
            print(f"\nACCESS_TOKEN:\n{token}\n")
            return token
        elif response.status_code == 401 or response.status_code == 404:
            print("❌ Thất bại: Tài khoản không tồn tại hoặc sai pass.")
            print("💡 Hãy đảm bảo bạn đã chạy 'python server/seed_test.py' trước đó.")
        else:
            print(f"❌ Lỗi {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Lỗi: Không thể kết nối tới Server (http://localhost:3000).")
        print("💡 Hãy đảm bảo Server FastAPI đang chạy.")
    
    return None

if __name__ == "__main__":
    get_access_token()
