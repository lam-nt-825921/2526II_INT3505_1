from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_logs_endpoint_returns_application_logs():
    client.get("/health")

    response = client.get("/admin/logs?limit=10")

    assert response.status_code == 200
    assert response.json()["count"] >= 1
    assert "logs" in response.json()


def test_trace_endpoint_returns_request_timeline():
    health_response = client.get("/health")
    trace_id = health_response.headers["X-Trace-ID"]

    response = client.get(f"/admin/traces/{trace_id}")
    body = response.json()

    assert response.status_code == 200
    assert body["trace_id"] == trace_id
    assert body["root_span"]["kind"] == "server"
    assert body["root_span"]["attributes"]["http.route"] == "/health"
    assert any(event["event"] == "request_started" for event in body["events"])
    assert any(event["event"] == "request_completed" for event in body["events"])
