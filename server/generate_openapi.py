import json
import sys
from app.main import app

def generate():
    openapi_schema = app.openapi()
    
    try:
        import yaml
        with open("swagger.yaml", "w", encoding="utf-8") as f:
            yaml.dump(openapi_schema, f, allow_unicode=True, sort_keys=False)
        print("Generated swagger.yaml successfully.")
    except ImportError:
        with open("swagger.json", "w", encoding="utf-8") as f:
            json.dump(openapi_schema, f, ensure_ascii=False, indent=2)
        print("pyyaml module not found. Generated swagger.json instead.")

if __name__ == "__main__":
    generate()
