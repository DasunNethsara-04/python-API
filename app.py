# imports
from token import OP
import pydantic
from fastapi import FastAPI
from uuid import UUID, uuid4
from typing import List, Optional

# list (acting like a database)
tasks: list = []

# initialize the app
app: FastAPI = FastAPI()

class Task(pydantic.BaseModel):
    id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

# routers
@app.get("/")
async def read_tasks(response_model=List[Task]):
    return tasks

@app.post("/tasks/", response_model=Task)
async def create_task(task: Task) -> Task:
    task.id = uuid4()
    tasks.append(task)
    return task

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=8000)