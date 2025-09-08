from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    start_date: str = Field(
        pattern = r"^\d{2}\.\d{2}$",
        examples = ["05.09"],
        description = "Формат: ДД.ММ"
    )

class Project(ProjectCreate):
    id: UUID

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    start_date: Optional[str] = Field(None, pattern=r"^\d{2}\.\d{2}$", examples=["05.09"], description="Формат: ДД.ММ")


class TaskCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    difficulty: int = Field(ge=1, le=10)
    deadline: str = Field(
        pattern = r"^\d{2}\.\d{2}$",
        examples = ["05.09"],
        description = "Формат: ДД.ММ"
    )

class Task(TaskCreate):
    id: UUID

class TaskUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    difficulty: Optional[int] = Field(None, ge=1, le=10)
    deadline: Optional[str] = Field(None, pattern=r"^\d{2}\.\d{2}$", examples=["05.09"], description="Формат: ДД.ММ")


class DeveloperCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=18, le=75)
    skill: int = Field(ge=1, le=10)

class Developer(DeveloperCreate):
    id: UUID
    task: Optional[Task] = None

class DeveloperUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=18, le=75)
    skill: Optional[int] = Field(None, ge=1, le=10)