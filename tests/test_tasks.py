from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_task():
    response = client.post("/tasks/", json={"task_type": "type_a", "data": "some data"})
    assert response.status_code == 200
    assert "task_id" in response.json()


def test_get_task_status():
    response = client.get("/tasks/1/status")
    assert response.status_code == 200
