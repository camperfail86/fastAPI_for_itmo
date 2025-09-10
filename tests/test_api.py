import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from storage import Projects, Developers, Tasks

@pytest.fixture(autouse=True)
def reset_storage():
    Projects.clear()
    Developers.clear()
    Tasks.clear()

# PROJECTS

@pytest.mark.asyncio
async def test_get_projects():
    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.get("/projects")
        assert response.status_code == 200
        data = response.json()
        assert len(data["list"]) == 0

@pytest.mark.asyncio
async def test_post_and_delete_project():
    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.post("/projects", json={"name": "Чат-бот", "start_date": "06.09"})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Чат-бот"

    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.get("/projects")
        assert response.status_code == 200
        proj = response.json()
        assert len(proj["list"]) == 1
        assert proj["list"][0]["start_date"] == "06.09"

    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.post("/projects", json={"name": "Телеграм-бот", "start_date": "07.09"})
        assert response.status_code == 200
        id_for_test = response.json()["id"]

    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.get("/projects")
        assert response.status_code == 200
        proj = response.json()["list"]
        assert len(proj) == 2
        assert proj[0]["name"] == "Чат-бот"
        assert proj[1]["name"] == "Телеграм-бот"

    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.delete(f"/projects/{id_for_test}")
        assert response.status_code == 202


@pytest.mark.asyncio
async def test_patch_project():
    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.post("/projects", json={"name": "Настройка серверной части", "start_date": "10.09"})
        assert response.status_code == 200
        data = response.json()
        id_for_test = data["id"]


    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)
    ) as client:
        response = await client.patch(f"/projects/{id_for_test}", json={"start_date": "10.10"})
        assert response.status_code == 200

    async with AsyncClient(
        base_url="http://localhost:8000",
        transport=ASGITransport(app=app)
    ) as client:
        response = await client.get(f"/projects/{id_for_test}")
        assert response.status_code == 200
        proj = response.json()
        assert proj["start_date"] == "10.10"
        assert proj["name"] == "Настройка серверной части"


# TASKS

@pytest.mark.asyncio
async def test_get_tasks():
    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.get("/tasks")
        assert response.status_code == 200
        data = response.json()["list"]
        assert len(data) == 0

@pytest.mark.asyncio
async def test_post_tasks():
    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.post("/tasks", json = {"name": "Фикс бага", "difficulty": 1, "deadline": "14.09"})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Фикс бага"

    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.get("/tasks")
        assert response.status_code == 200
        data = response.json()["list"]
        assert len(data) == 1

@pytest.mark.asyncio
async def test_patch_and_delete_task():
    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.post("/tasks", json = {"name": "Добавление фичи", "difficulty": 2, "deadline": "22.09"})
        assert response.status_code == 200
        data = response.json()
        id_for_test = data["id"]

    async with AsyncClient(
        base_url="http://localhost:8000",
        transport=ASGITransport(app=app)
    ) as client:
        response = await client.patch(f"/tasks/{id_for_test}", json={"difficulty": 2, "deadline": "25.09"})
        assert response.status_code == 200
        data = response.json()
        assert data["response"] == "Задача изменена"

    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.delete(f"/tasks/{id_for_test}")
        assert response.status_code == 202
        data = response.json()
        assert data["response"] == "Задача удалена"

    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.get(f"/tasks/{id_for_test}")
        assert response.status_code == 404


# Developers
@pytest.mark.asyncio
async def test_get_developers():
    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.get("/developers")
        assert response.status_code == 200
        data = response.json()["list"]
        assert len(data) == 0

@pytest.mark.asyncio
async def test_post_developer():
    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.post("/developers", json = {"name": "Григорий Маринец-Дейнеко", "skill": 3, "age": 21})
        assert response.status_code == 200
        data = response.json()
        assert data["skill"] == 3
        assert data["age"] == 21
        assert data["name"] == "Григорий Маринец-Дейнеко"

    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.get("/developers")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

@pytest.mark.asyncio
async def test_patch_and_delete_developer():
    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.post("/developers", json = {"name": "Гусейн Байрамов", "skill": 1, "age": 22})
        assert response.status_code == 200
        data = response.json()
        id_for_test = data["id"]

    async with AsyncClient(
        base_url="http://localhost:8000",
        transport=ASGITransport(app=app)
    ) as client:
        response = await client.patch(f"/developers/{id_for_test}", json={"skill": 2})
        assert response.status_code == 200
        data = response.json()
        assert data["response"] == "Данные разработчика успешно изменены"

    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.delete(f"/developers/{id_for_test}")
        assert response.status_code == 202
        data = response.json()
        assert data["response"] == "Разработчик удален"

    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.get(f"/developers/{id_for_test}")
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_change_task_developer():
    async with AsyncClient(
        base_url="http://localhost:8000",
        transport=ASGITransport(app=app)
    ) as client:
        response = await client.post(f"/developers", json = {"name": "Гусейн Байрамов", "skill": 1, "age": 22})
        assert response.status_code == 200
        data = response.json()
        id_for_test = data["id"]
        assert data["name"] == "Гусейн Байрамов"


    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.get(f"/developers/{id_for_test}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == id_for_test
        assert data["name"] == "Гусейн Байрамов"
        assert data["skill"] != 2
        assert data["task"] == None

    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.post("/tasks", json = {"name": "Добавление фичи", "difficulty": 2, "deadline": "22.09"})
        assert response.status_code == 200
        data = response.json()
        id_task = data["id"]


    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.patch(f"/developers/{id_for_test}/{id_task}")
        assert response.status_code == 200

    async with AsyncClient(
            base_url="http://localhost:8000",
            transport=ASGITransport(app=app)) as client:
        response = await client.get(f"/developers/{id_for_test}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == id_for_test
        assert data["name"] == "Гусейн Байрамов"
        assert data["skill"] != 2
        assert data["task"]["id"] == id_task
        assert data["task"]["name"] == "Добавление фичи"

