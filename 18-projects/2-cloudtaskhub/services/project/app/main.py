from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Project Service")


class Task(BaseModel):
    id: int
    title: str
    done: bool = False


fake_tasks_db: List[Task] = [
    Task(id=1, title="Créer la structure du projet", done=True),
    Task(id=2, title="Écrire les services FastAPI", done=False),
]


@app.get("/health")
def health():
    return {"status": "ok", "service": "project"}


@app.get("/tasks")
def list_tasks():
    return fake_tasks_db


@app.post("/tasks")
def create_task(task: Task):
    fake_tasks_db.append(task)
    return {"message": "task created (fake)", "task": task}


@app.on_event("startup")
async def _startup():
    Instrumentator().instrument(app).expose(app)
