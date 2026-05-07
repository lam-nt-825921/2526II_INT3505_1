import requests
import json

BASE_URL = "http://127.0.0.1:8001/v1"

def test_v1_flow():
    # # 1. Register
    # user_data = {
    #     "username": "testuser",
    #     "full_name": "Test User",
    #     "password": "password123"
    # }
    # print("Registering...")
    # resp = requests.post(f"{BASE_URL}/register", json=user_data)
    # print(f"Status: {resp.status_code}, Body: {resp.json()}")

    # 2. Login
    login_data = {
        "username": "testuser",
        "password": "password123"
    }
    print("\nLogging in...")
    resp = requests.post(f"{BASE_URL}/login", json=login_data)
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"Token received")

    # 3. Get Accounts
    print("\nGetting accounts...")
    resp = requests.get(f"{BASE_URL}/accounts", headers=headers)
    accounts = resp.json()
    print(f"Accounts: {accounts}")
    acc_num = accounts[0]["account_number"]
    acc_id = accounts[0]["id"]

    # 4. Withdraw (Amount as String in V1)
    withdraw_data = {
        "account_number": acc_num,
        "amount": "150.50", # STRING
        "description": "Coffee and cake"
    }
    print(f"\nWithdrawing {withdraw_data['amount']} (as string)...")
    resp = requests.post(f"{BASE_URL}/withdraw", json=withdraw_data, headers=headers)
    print(f"Status: {resp.status_code}, Body: {resp.json()}")
    print("\n--- Deprecation Headers Checked ---")
    print(f"X-API-Version: {resp.headers.get('X-API-Version')}")
    print(f"Deprecation: {resp.headers.get('Deprecation')}")
    print(f"Sunset: {resp.headers.get('Sunset')}")
    print(f"Warning: {resp.headers.get('Warning')}")
    print("-----------------------------------\n")

    # 5. Get Transactions
    print(f"\nGetting transactions for account {acc_id}...")
    resp = requests.get(f"{BASE_URL}/accounts/{acc_id}/transactions", headers=headers)
    print(f"Transactions: {resp.json()}")

if __name__ == "__main__":
    # Note: Make sure the server is running on port 8001
    try:
        test_v1_flow()
    except Exception as e:
        print(f"Error: {e}. Is the server running?")
