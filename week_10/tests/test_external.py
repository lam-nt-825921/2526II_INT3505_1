import pybreaker
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_external_circuit_open_returns_503(monkeypatch):
    def fake_external_status():
        raise pybreaker.CircuitBreakerError("circuit open")

    monkeypatch.setattr("app.routes.external.fetch_external_status", fake_external_status)

    response = client.get("/api/v1/external/status")

    assert response.status_code == 503
    assert response.json()["detail"] == "External service circuit is open"
