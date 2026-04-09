import requests
import time

API_BASE = "http://127.0.0.1:8001/books"
ITERATIONS = 20
OFFSET = 95000

def print_data_sample(data_list):
    if not data_list:
        return
    if len(data_list) <= 5:
        for item in data_list:
            print("  ", item)
    else:
        for item in data_list[:3]:
            print("  ", item)
        print("   ...")
        for item in data_list[-2:]:
            print("  ", item)

def test_endpoint(name, url):
    total_time = 0
    server_time = 0
    print(f"Đang gọi: {name} (Lặp {ITERATIONS} lần)...")
    last_data = None
    for _ in range(ITERATIONS):
        start = time.time()
        res = requests.get(url)
        latency = time.time() - start
        
        data = res.json()
        total_time += latency
        server_time += data.get("db_query_time_ms", 0)
        last_data = data
        
    avg_latency = (total_time / ITERATIONS) * 1000 # ms
    avg_server = (server_time / ITERATIONS) # Tính sẵn = ms từ server trả về
    
    print(f"\n=> Mẫu dữ liệu lấy được ({name}):")
    print_data_sample(last_data.get("data", []))
    print(f"=> Thời gian DB trung bình: {avg_server:.3f} ms")
    
    return avg_server, avg_latency

def main():
    print(f"{'='*65}")
    print(f" BÁO CÁO BENCHMARK PHÂN TRANG (Mốc Offset/Cursor = {OFFSET})")
    print(f"{'='*65}")
    
    # 1. No pagination (Chỉ 1 lần test vì tải cực nặng lên DB cache)
    print("\n[Chiến thuật 1] Không phân trang")
    print("Test: Đang lấy trọn vẹn 100,000 bản ghi...")
    start_time = time.time()
    res = requests.get(f"{API_BASE}/no-page?limit=100000")
    no_page_latency = (time.time() - start_time) * 1000
    data = res.json()
    no_page_server = data.get("db_query_time_ms", 0)
    print(f"\n=> Mẫu dữ liệu lấy được (Không Phân Trang):")
    print_data_sample(data.get("data", []))
    print(f"=> Số lượng bản ghi lấy về: {data.get('count_fetched')}")
    print(f"=> Thời gian lấy (DB): {no_page_server:.3f} ms")
    print(f"=> HTTP Latency: {no_page_latency:.3f} ms")
    input("\nBấm Enter (next) để tiếp tục...")
    
    # 2. Offset Pagination
    print("\n[Chiến thuật 2] Offset Pagination")
    os, _l_os = test_endpoint("Offset Pagination", f"{API_BASE}/offset?offset={OFFSET}&limit=20")
    input("\nBấm Enter (next) để tiếp tục...")
    
    # 3. Cursor Pagination
    print("\n[Chiến thuật 3] Cursor Pagination")
    cs, _l_cs = test_endpoint("Cursor Pagination", f"{API_BASE}/cursor?cursor_id={OFFSET}&limit=20")
    input("\nBấm Enter (next) để xem bảng kết quả...")
    
    # Print bảng Markdown
    print("\n[+] BẢNG SO SÁNH TỐC ĐỘ:")
    print(f"| {'Chiến thuật':<25} | {'DB Query Time (ms)':<20} | {'HTTP Latency (ms)':<20} |")
    print(f"|{'-'*27}|{'-'*22}|{'-'*22}|")
    print(f"| {'Không Phân Trang (Z->A)':<25} | {no_page_server:<20.3f} | {no_page_latency:<20.3f} |")
    print(f"| {'Offset (Skip {OFFSET})':<25} | {os:<20.3f} | {_l_os:<20.3f} |")
    print(f"| {'Cursor (WHERE id > {OFFSET})':<25} | {cs:<20.3f} | {_l_cs:<20.3f} |")
    
    print(f"\n[+] KẾT LUẬN TỰ ĐỘNG:")
    if cs < os:
        diff = os / cs if cs > 0 else 999
        print(f"Phân trang CURSOR nhanh hơn OFFSET tới ~{diff:.1f} lần!")
        print("-> Giải thích: Offset phải đếm và lặp qua toàn bộ 95k bản ghi rác. Cursor lợi dụng Index B-Tree đi thẳng đến bản ghi 95000 ngay lập tức (Truy xuất O(1)).")

if __name__ == "__main__":
    main()
