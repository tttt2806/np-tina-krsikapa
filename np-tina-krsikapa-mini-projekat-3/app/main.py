"""Mali Task API sa dva endpointa: POST /tasks i GET /tasks/{task_id}."""

from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel, Field, field_validator

MAX_TASKS = 1000

app = FastAPI(title="Task API", version="1.0.0")


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)
    priority: int = Field(default=1, ge=1, le=5)

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("title must not be blank")
        return cleaned


class Task(TaskCreate):
    id: int


_tasks: dict[int, Task] = {}


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> Task:
    if len(_tasks) >= MAX_TASKS:
        raise HTTPException(
            status_code=status.HTTP_507_INSUFFICIENT_STORAGE,
            detail="Task limit reached",
        )
    task = Task(id=len(_tasks) + 1, **payload.model_dump())
    _tasks[task.id] = task
    return task


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int = Path(ge=1)) -> Task:
    task = _tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task
