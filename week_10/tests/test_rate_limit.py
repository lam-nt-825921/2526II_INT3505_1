from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_write_endpoint_rate_limit_eventually_returns_429():
    statuses = [
        client.post("/api/v1/items", json={"name": f"limited-{index}"}).status_code
        for index in range(12)
    ]

    assert 429 in statuses
