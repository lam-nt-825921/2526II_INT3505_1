from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_metrics_endpoint_exists():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "http_requests" in response.text or "http_request" in response.text
