import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def fetch_and_buy(product_id):
    url = f"{BASE_URL}/product/{product_id}"
    print(f"--- Đang gửi yêu cầu GET lấy thông tin sản phẩm ID: {product_id} ---")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success':
                data = result['data']
                print(f"✅ Tìm thấy! Tên: {data['name']} | Giá: ${data['price']} | Số lượng còn: {data.get('quantity', 0)}")
                
                # Trích xuất link mua hàng do Server chỉ định (HATEOAS)
                buy_endpoint = data.get('buy_link')
                
                if buy_endpoint:
                    print(f"\n[HATEOAS] Server yêu cầu gọi tới URI sau để mua: {buy_endpoint}")
                    
                    user_input = input("-> Mua sản phẩm này? (yes/no): ").strip().lower()
                    if user_input == 'yes':
                        buy_url = f"{BASE_URL}{buy_endpoint}"
                        print(f"\n--- Đang gửi yêu cầu POST đến {buy_url} ---")
                        
                        # Gọi endpoint do chính Server cung cấp
                        buy_response = requests.post(buy_url)
                        
                        if buy_response.status_code == 200:
                            buy_result = buy_response.json()
                            if buy_result['status'] == 'success':
                                print(f"🎉 {buy_result['message']}")
                            else:
                                print(f"❌ Mua thất bại: {buy_result['message']}")
                        else:
                            print(f"⚠️ Lỗi kết nối khi mua: Status {buy_response.status_code}")
                    else:
                        print("Đã hủy mua.")
                else:
                    print("⚠️ Sản phẩm không có link mua hàng hợp lệ.")
            else:
                print(f"❌ Lỗi: {result['message']}")
        else:
            print(f"⚠️ Lỗi kết nối: Status {response.status_code}")
            
    except Exception as e:
        print(f"❗ Không thể kết nối tới Server: {e}")

if __name__ == "__main__":
    fetch_and_buy("1")
