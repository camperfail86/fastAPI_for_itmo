import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from classes import Project, Task, Developer, ProjectCreate, TaskCreate, DeveloperCreate
from storage import Projects, Developers, Tasks
from uuid import uuid4, UUID

app = FastAPI()

# Проекты
@app.get("/projects", tags=["Проекты"], summary="Получить все проекты")
def get_projects():
    return Projects

@app.get("/projects/{project_id}", tags=["Проекты"], summary="Получить определенный проект")
def get_project(project_id: UUID):
    for project in Projects:
        if project.id == project_id:
            return project
    raise HTTPException(status_code = 404, detail = "Проект не найден")

@app.post("/projects", tags=["Проекты"], summary="Добавить проект")
def create_project(new_project: ProjectCreate):
    proj = Project(id = uuid4(), name = new_project.name, start_date = new_project.start_date)
    Projects.append(proj)
    return proj

@app.delete("/projects/{project_id}", tags = ["Проекты"], summary = "Удалить проект")
def delete_project(project_id: UUID):
    for project in Projects:
        if project.id == project_id:
            Projects.remove(project)
            return JSONResponse(
                content={"response": "Проект успешно удален"},
                status_code=202
            )
    raise HTTPException(status_code = 404, detail = "Такого проекта не существует")

@app.patch("/projects/{project_id}", tags = ["Проекты"], summary = "Изменить проект")
def update_project(project_id: UUID, new_project: ProjectCreate):
    for project in Projects:
        if project.id == project_id:
            project.name = new_project.name
            project.start_date = new_project.start_date
            return {"response": "Проект успешно изменен"}
    raise HTTPException(status_code = 404, detail = "Такого проекта не существует")



# Таски
@app.get("/tasks", tags = ["Задачи"], summary = "Получить все задачи")
def get_tasks():
    return Tasks

@app.get("/tasks/{task_id}", tags = ["Задачи"], summary = "Получить конкретную задачу")
def get_task(task_id: UUID):
    for task in Tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code = 404, detail = "Задача не найдена")

@app.post("/tasks", tags = ["Задачи"], summary = "Добавить задачу")
def create_task(task: TaskCreate):
    t = Task(id = uuid4(), name = task.name, difficulty = task.difficulty, deadline = task.deadline)
    Tasks.append(t)
    return t

@app.delete("/tasks/{task_id}", tags = ["Задачи"], summary = "Удалить задачу")
def delete_task(task_id: UUID):
    for task in Tasks:
        if task.id == task_id:
            Tasks.remove(task)
            return JSONResponse(
                content={"response": "Задача удалена"},
                status_code=202
            )
    raise HTTPException(status_code = 404, detail = "Задача не найдена")

@app.patch("/tasks/{task_id}", tags = ["Задачи"], summary = "Изменить задачу")
def update_task(task_id: UUID, new_task: TaskCreate):
    for task in Tasks:
        if task.id == task_id:
            task.name = new_task.name
            task.difficulty = new_task.difficulty
            task.deadline = new_task.deadline
            return {"response": "Задача изменена"}
    raise HTTPException(status_code = 404, detail = "Задача не найдена")

# Разрабы
@app.get("/developers", tags=["Разработчики"], summary="Получить всех разработчиков")
def get_developers():
    return Developers

@app.get("/developers/{developer_id}", tags=["Разработчики"], summary="Получить одного разработчика")
def get_developer(developer_id: UUID):
    for developer in Developers:
        if developer.id == developer_id:
            return developer
    raise HTTPException(status_code = 404, detail = "Разработчик не найден")

@app.delete("/developers/{developer_id}", tags=["Разработчики"], summary="Удалить разработчика", status_code = 202)
def delete_developer(developer_id: UUID):
    for developer in Developers:
        if developer.id == developer_id:
            Developers.remove(developer)
            return JSONResponse(
                content={"response": "Разработчик удален"},
                status_code=202
            )
    raise HTTPException(status_code = 404, detail = "Разработчик не найден")

@app.post("/developers", tags=["Разработчики"], summary="Добавить разработчика")
def create_developer(developer: DeveloperCreate):
    dev = Developer(id = uuid4(), name = developer.name, age = developer.age, skill = developer.skill, task = None)
    Developers.append(dev)
    return dev

@app.patch("/developers/{developer_id}", tags=["Разработчики"], summary="Изменить данные у разработчика")
def update_developer(developer_id: UUID, new_developer: DeveloperCreate):
    for developer in Developers:
        if developer.id == developer_id:
            developer.name = new_developer.name
            developer.age = new_developer.age
            developer.skill = new_developer.skill
            return {"response": "Данные разработчика успешно изменены"}
    raise HTTPException(status_code = 404, detail = "Разработчик не найден")

@app.patch("/developers/{developer_id}/{task_id}", tags=["Разработчики"], summary="Изменить/добавить задачу разработчику")
def update_task_developer(developer_id: UUID, task_id: UUID):
    for developer in Developers:
        if developer.id == developer_id:
            for task in Tasks:
                if task.id == task_id:
                    developer.task = task
                    return developer
    raise HTTPException(status_code = 404, detail = "Такой разработчик или задача не найдены")


if __name__ == "__main__":
    uvicorn.run("main:app", reload = True)


