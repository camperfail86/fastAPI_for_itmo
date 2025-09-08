import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from storage import Projects, Developers, Tasks

@pytest.fixture(autouse=True)
def reset_storage():
    Projects.clear(); Developers.clear(); Tasks.clear()
    yield
    Projects.clear(); Developers.clear(); Tasks.clear()

@pytest.mark.asyncio
async def test_get_projects():
    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.get("/projects")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0

@pytest.mark.asyncio
async def test_post_and_delete_project():
    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.post("/projects", json={"name": "Чат-бот", "start_date": "06.09"})
        assert response.status_code == 200
        data = response.json()
        assert data["response"] == "Проект успешно добавлен"

    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.get("/projects")
        assert response.status_code == 200
        proj = response.json()
        assert len(proj) == 1

    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.post("/projects", json={"name": "Телеграм-бот", "start_date": "07.09"})
        assert response.status_code == 200
        data = response.json()
        assert data["response"] == "Проект успешно добавлен"

    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.get("/projects")
        assert response.status_code == 200
        proj = response.json()
        assert len(proj) == 2

    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.delete("/projects/1000")
        assert response.status_code == 202
        proj = response.json()
        assert proj["response"] == "Проект успешно удален"
        assert len(proj) == 1



# @pytest.mark.asyncio
# async def test_patch_project():
#     async with AsyncClient(
#             base_url="http://localhost:8000",
#             transport=ASGITransport(app=app)) as client:
#         response = await client.post("/projects", json={"name": "Настройка серверной части", "start_date": "10.09"})
#         assert response.status_code == 200
#         data = response.json()
#         assert data["response"] == "Проект успешно добавлен"
#     proj_id = 1002
#     async with AsyncClient(
#         base_url="http://localhost:8000",
#         transport=ASGITransport(app=app)
#     ) as client:
#         response = await client.get(f"/projects/{proj_id}")
#         assert response.status_code == 200
#         proj = response.json()
#         assert proj["id"] == 1002
#         assert proj["start_date"] == "10.09"
#
#
#     async with AsyncClient(
#             base_url="http://localhost:8000",
#             transport=ASGITransport(app=app)
#     ) as client:
#         response = await client.patch(f"/projects/{proj_id}", json={"name": "Чат-бот", "start_date": "10.10"})
#         assert response.status_code == 200
#
#     async with AsyncClient(
#         base_url="http://localhost:8000",
#         transport=ASGITransport(app=app)
#     ) as client:
#         response = await client.get("/projects/1001")
#         assert response.status_code == 200
#         proj = response.json()
#         assert proj["id"] == 1001
#         assert proj["start_date"] == "10.10"


@pytest.mark.asyncio
async def test_get_tasks():
    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.get("/tasks")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0

@pytest.mark.asyncio
async def test_post_tasks():
    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.post("/tasks", json = {"name": "Фикса бага", "difficulty": "1", "deadline": "14.09"})
        assert response.status_code == 200
        data = response.json()
        assert data["response"] == "Задача успешно добавлена"

    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.get("/tasks")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

# @pytest.mark.asyncio
# async def test_patch_and_delete_task():
#     async with AsyncClient(
#         base_url="http://localhost:8000",
#         transport=ASGITransport(app=app)
#     ) as client:
#         response = await client.patch(f"/tasks/{100}", json="")
#         assert response.status_code == 200