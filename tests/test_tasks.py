from main import app
from fastapi.testclient import TestClient

test_cliet = TestClient(app=app)


def test_dashboard():
    response = test_cliet.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type")


def test_create_task_add():
    response = test_cliet.post("/publish-task", json={"task_type": "add", "payload": {"a": 2, "b": 3}})
    assert response.status_code == 202
    data = response.json()
    assert data["status"] == "pending"


def test_create_task_mul():
    response = test_cliet.post("/publish-task", json={"task_type": "multiply", "payload": {"a": 2, "b": 3}})
    assert response.status_code == 202
    data = response.json()
    assert data["status"] == "pending"


def test_create_task_rev():
    response = test_cliet.post("/publish-task", json={"task_type": "reverse", "payload": {"text": "hello"}})
    assert response.status_code == 202
    data = response.json()
    assert data["status"] == "pending"


def test_create_and_cancel_task():
    response = test_cliet.post("/publish-task", json={"task_type": "add", "payload": {"a": 2, "b": 3}})
    assert response.status_code == 202
    data = response.json()
    task_id = data["id"]
    cancel_response = test_cliet.post(f"/tasks/{task_id}/cancel")
    assert cancel_response.status_code == 200


def test_get_task_list():
    response = test_cliet.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) >= 0


def test_get_nonexistent_task():
    response = test_cliet.get("/tasks/9999")
    assert response.status_code == 404


def update_task_and_run_again():
    response = test_cliet.put("/tasks/1", json={"task_type": "add", "payload": {"a": 2, "b": 3}})
    assert response.status_code == 200
    data = response.json()
    task_id = data["id"]
    run_response = test_cliet.post(f"/tasks/{task_id}/run")
    assert run_response.status_code == 200
