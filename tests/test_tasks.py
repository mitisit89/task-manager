import pytest
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_create_task():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/tasks", json={"task_type": "add", "payload": {"a": 2, "b": 3}})
    assert response.status_code == 200
    data = response.json()
    assert data["task_type"] == "addition"
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_get_nonexistent_task():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/tasks/9999")
    assert response.status_code == 404
