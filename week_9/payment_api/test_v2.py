import requests
import json

BASE_URL_V1 = "http://127.0.0.1:8001/v1"
BASE_URL_V2 = "http://127.0.0.1:8001/v2"

def test_minimalist_v2():
    # 1. Login via V1 (V2 does not have login)
    login_data = {
        "username": "testuser",
        "password": "password123"
    }
    print("Logging in via V1...")
    resp = requests.post(f"{BASE_URL_V1}/login", json=login_data)
    if resp.status_code != 200:
        print("Login failed. Run test_v1.py first.")
        return
        
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"Token received from V1")

    # 2. Get Accounts via V1 (V2 does not have accounts)
    print("\nGetting accounts via V1...")
    resp = requests.get(f"{BASE_URL_V1}/accounts", headers=headers)
    accounts = resp.json()
    acc_num = accounts[0]["account_number"]
    print(f"Accounts (from V1): {accounts}")
    
    # 3. Withdraw via V2 (This is the ONLY V2 endpoint)
    withdraw_data = {
        "account_number": acc_num,
        "amount": 50.0, # FLOAT in V2
        "description": "Minimalist V2 Withdrawal"
    }
    print(f"\nWithdrawing {withdraw_data['amount']} (as float) via V2...")
    resp = requests.post(f"{BASE_URL_V2}/withdraw", json=withdraw_data, headers=headers)
    print(f"Status: {resp.status_code}, Body: {resp.json()}")
    print(f"X-API-Version: {resp.headers.get('X-API-Version')}")

if __name__ == "__main__":
    try:
        test_minimalist_v2()
    except Exception as e:
        print(f"Error: {e}. Is the server running?")
