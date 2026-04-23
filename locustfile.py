import random
from locust import HttpUser, task, between

class LibraryUser(HttpUser):
    # Thời gian chờ giữa các task từ 1-3 giây để giả lập người dùng thật
    wait_time = between(1, 3)
    token = None

    def on_start(self):
        """Được gọi khi một User bắt đầu: Thực hiện Login"""
        response = self.client.post("/api/v1/auth/login", data={
            "username": "admin",
            "password": "admin123"
        })
        if response.status_code == 200:
            self.token = response.json().get("access_token")
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            print(f"Login failed: {response.status_code} - {response.text}")

    @task(3)
    def view_books(self):
        """Xem danh sách sách"""
        if self.token:
            self.client.get("/api/v1/books", headers=self.headers, name="/api/v1/books")

    @task(1)
    def view_book_detail(self):
        """Xem chi tiết sách"""
        if self.token:
            book_id = 1 # Database hiện tại chỉ có 1 cuốn sách (ID: 1) từ seed_test.py
            self.client.get(f"/api/v1/books/{book_id}", headers=self.headers, name="/api/v1/books/[id]")

    @task(2)
    def check_me(self):
        """Kiểm tra profile"""
        if self.token:
            self.client.get("/api/v1/users/me", headers=self.headers, name="/api/v1/users/me")
