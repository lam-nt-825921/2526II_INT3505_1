import json
import sys

try:
    from main import app
    
    print("Đang trích xuất schema tự động từ FastAPI (mã nguồn)...")
    
    # Rút trích cấu trúc OpenAPI chuẩn 3.0 từ FastAPI
    openapi_schema = app.openapi()
    
    # 1. Lưu cấu trúc dưới dạng JSON
    with open('openapi.json', 'w', encoding='utf-8') as f:
        json.dump(openapi_schema, f, ensure_ascii=False, indent=2)
    print("✓ Đã sinh thành công file: openapi.json")
    
    # 2. Lưu cấu trúc dưới dạng YAML (nếu thư viện PyYAML đã cài đặt)
    try:
        import yaml
        with open('openapi.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(openapi_schema, f, allow_unicode=True, sort_keys=False)
        print("✓ Đã sinh thành công file: openapi.yaml")
    except ImportError:
        print("⚠ Bỏ qua định dạng YAML do chưa cài thư viện PyYAML (`pip install pyyaml`).")
        print("  Tuy nhiên biểu đồ openapi.json đã được sinh hoàn hảo!")
        
except Exception as e:
    print(f"Lỗi khi sinh OpenAI Schema: {e}")
    sys.exit(1)
