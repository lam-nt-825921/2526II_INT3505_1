from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_logs_endpoint_returns_application_logs():
    client.get("/health")

    response = client.get("/admin/logs?limit=10")

    assert response.status_code == 200
    assert response.json()["count"] >= 1
    assert "logs" in response.json()
