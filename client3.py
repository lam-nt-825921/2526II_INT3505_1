import requests

BASE_URL = "http://127.0.0.1:8000"

def fetch_and_patch(product_id):
    url = f"{BASE_URL}/product/{product_id}"
    print(f"--- 1. Đang gửi yêu cầu GET lấy bản đại diện (representation) của sản phẩm ID: {product_id} ---")
    
    try:
        # Bước 1: Lấy bản đại diện hiện tại
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success':
                data = result['data']
                print(f"✅ Tình trạng hiện tại: Tên: {data['name']} | Giá: ${data['price']} | Số lượng: {data.get('quantity', 0)}")
                
                # Bước 2: Thao tác thay đổi trên bản đại diện (client tự xử lý)
                print("\n[MANIPULATION] Client quyết định thay đổi số lượng thành 100...")
                new_quantity = 100
                payload = {
                    "quantity": new_quantity
                }
                
                user_input = input(f"-> Gửi yêu cầu PATCH cập nhật số lượng lên {new_quantity}? (yes/no): ").strip().lower()
                if user_input == 'yes':
                    print(f"\n--- 2. Đang gửi yêu cầu PATCH tới {url} ---")
                    print(f"[MANIPULATION] Payload (Bản đại diện gửi đi): {payload}")
                    
                    # Bước 3: Gửi phần đại diện thay đổi cập nhật lên Server
                    patch_response = requests.patch(url, json=payload)
                    
                    if patch_response.status_code == 200:
                        patch_result = patch_response.json()
                        if patch_result['status'] == 'success':
                            updated_data = patch_result['data']
                            print(f"🎉 {patch_result['message']}")
                            print(f"✅ Dữ liệu mới từ Server: Tên: {updated_data['name']} | Số lượng mới: {updated_data['quantity']}")
                        else:
                            print(f"❌ Cập nhật thất bại: {patch_result['message']}")
                    else:
                        print(f"⚠️ Lỗi kết nối khi cập nhật: Status {patch_response.status_code}")
                else:
                    print("Đã hủy cập nhật.")
            else:
                print(f"❌ Lỗi: {result['message']}")
        else:
            print(f"⚠️ Lỗi kết nối: Status {response.status_code}")
            
    except Exception as e:
        print(f"❗ Không thể kết nối tới Server: {e}")

if __name__ == "__main__":
    fetch_and_patch("1")
