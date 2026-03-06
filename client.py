import requests
import time

def fetch_data(product_id):
    url = f"http://127.0.0.1:8000/product/{product_id}"
    
    print(f"--- Đang gửi yêu cầu lấy sản phẩm ID: {product_id} ---")
    
    try:
        # Thực hiện Fetch dữ liệu (GET request)
        response = requests.get(url)
        
        # Kiểm tra Status Code
        if response.status_code == 200:
            result = response.json() # Chuyển đổi bản đại diện JSON sang Dictionary
            if result['status'] == 'success':
                data = result['data']
                print(f"✅ Thành công! Tên: {data['name']} | Giá: ${data['price']}")
            else:
                print(f"❌ Lỗi: {result['message']}")
        else:
            print(f"⚠️ Lỗi kết nối: Status {response.status_code}")
            
    except Exception as e:
        print(f"❗ Không thể kết nối tới Server: {e}")

if __name__ == "__main__":
    # Giả lập thao tác người dùng fetch dữ liệu
    fetch_data("1")
    time.sleep(1) # Nghỉ 1 xíu cho giống thật
    fetch_data("99") # Thử một ID không tồn tại