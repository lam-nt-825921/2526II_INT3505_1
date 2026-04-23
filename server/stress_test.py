import requests
import subprocess
import shutil
import sys

def run_stress_test():
    # 1. Cấu hình
    BASE_URL = "http://localhost:3000"
    LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
    TEST_URL = f"{BASE_URL}/api/v1/books"
    
    # Thông số test (Có thể điều chỉnh)
    CONCURRENCY = 50
    TOTAL_REQUESTS = 1000

    print("--- Bắt đầu quy trình Stress Test tự động ---")

    # 2. Đăng nhập lấy Token
    try:
        response = requests.post(LOGIN_URL, data={"username": "admin", "password": "admin123"})
        if response.status_code != 200:
            print(f"❌ Không thể đăng nhập. Lỗi: {response.text}")
            print("💡 Hãy chắc chắn bạn đã chạy 'python server/seed_test.py' và Server đang bật.")
            return
        
        token = response.json().get("access_token")
        print("✅ Đã lấy Access Token thành công.")
    except Exception as e:
        print(f"❌ Lỗi kết nối Server: {e}")
        return

    # 3. Kiểm tra công cụ có sẵn (hey hoặc ab)
    cmd = []
    if shutil.which("hey"):
        print("🚀 Phát hiện thấy 'hey', đang bắt đầu tấn công...")
        cmd = ["hey", "-n", str(TOTAL_REQUESTS), "-c", str(CONCURRENCY), 
               "-H", f"Authorization: Bearer {token}", TEST_URL]
    elif shutil.which("ab"):
        print("🚀 Phát hiện thấy 'ab' (Apache Benchmark), đang bắt đầu tấn công...")
        # Lưu ý: ab cần header truyền vào tham số -H riêng biệt
        cmd = ["ab", "-n", str(TOTAL_REQUESTS), "-c", str(CONCURRENCY), 
               "-H", f"Authorization: Bearer {token}", TEST_URL]
    else:
        print("❌ Không tìm thấy 'hey' hoặc 'ab' trong hệ thống.")
        print("💡 Vui lòng cài đặt 'hey' hoặc dùng Locust để thay thế.")
        return

    # 4. Thực thi lệnh
    print(f"执行 command: {' '.join(cmd)}")
    try:
        # Chạy và in kết quả trực tiếp ra màn hình
        subprocess.run(cmd, check=True)
    except Exception as e:
        print(f"❌ Lỗi khi chạy lệnh test: {e}")

if __name__ == "__main__":
    run_stress_test()
