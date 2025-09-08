from pydantic import BaseModel, Field
from typing import Optional

class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    start_date: str = Field(
        pattern = r"^\d{2}\.\d{2}$",
        examples = ["05.09"],
        description = "Формат: ДД.ММ"
    )

class Project(ProjectCreate):
    id: int

class TaskCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    difficulty: int = Field(ge=1, le=10)
    deadline: str = Field(
        pattern = r"^\d{2}\.\d{2}$",
        examples = ["05.09"],
        description = "Формат: ДД.ММ"
    )

class Task(TaskCreate):
    id: int

class DeveloperCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=18, le=75)
    skill: int = Field(ge=1, le=10)

class Developer(DeveloperCreate):
    id: int
    task: Optional[Task] = None