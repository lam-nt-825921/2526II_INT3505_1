from fastapi.testclient import TestClient

from app.main import app
from app.routes.items import items_store

client = TestClient(app)


def test_create_and_list_items():
    items_store.clear()

    create_response = client.post(
        "/api/v1/items",
        json={"name": "pytest item", "description": "created from test"},
    )
    list_response = client.get("/api/v1/items")

    assert create_response.status_code == 201
    assert create_response.json()["name"] == "pytest item"
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
