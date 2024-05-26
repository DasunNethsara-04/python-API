# imports
import pydantic
from fastapi import FastAPI, HTTPException
from uuid import UUID, uuid4
from typing import List, Optional

# list (acting like a database)
tasks: list = []

# initialize the app
app: FastAPI = FastAPI()

class Task(pydantic.BaseModel):
    """
    A model representing a task.

    Attributes:
        id (Optional[UUID]): A unique identifier for the task.
        title (str): The title of the task.
        description (Optional[str]): An optional description of the task.
        completed (bool): A flag indicating whether the task is completed.
    """
    id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

# routers
@app.get("/", response_model=List[Task])
async def read_tasks():
    """
    Retrieve all tasks.

    This function retrieves all tasks from the in-memory list.

    Parameters:
        response_model (List[Task]): The expected return type of the function.

    Returns:
        List[Task]: A list of all tasks.
    """
    return tasks

@app.post("/tasks/", response_model=Task)
async def create_task(task: Task) -> Task:
    """
    Create a new task.

    This function creates a new task and assigns it a unique ID. The task is then added to the list of tasks.

    Parameters:
        task (Task): The task object to be created, containing the task's title, description, and completion status.

    Returns:
        Task: The newly created task object, including its unique ID.
    """
    task.id = uuid4()
    tasks.append(task)
    return task

@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: UUID) -> Task:
    """
    Retrieve a specific task.

    This function retrieves a specific task from the in-memory list based on the provided task ID.

    Parameters:
        task_id (UUID): The unique identifier of the task to be retrieved.

    Returns:
        Task: The task object with the provided task ID, or raises HTTPException with status code 404 if the task is not found.
    """
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task Not Found")

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: UUID, task_update: Task) -> Task:
    """
    Update a specific task.

    This function updates a specific task in the in-memory list based on the provided task ID.

    Parameters:
        task_id (UUID): The unique identifier of the task to be updated.
        task_update (Task): The updated task object containing the new title, description, and completion status.

    Returns:
        Task: The updated task object with the provided task ID. If the task is not found, it raises an HTTPException with status code 404.
    """
    for index, task in enumerate(tasks):
        if task.id == task_id:
            updated_task = task.copy(update=task_update.dict(exclude_unset=True))
            tasks[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task Not Found")

@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: UUID) -> Task:
    """
    Delete a specific task.

    This function deletes a specific task from the in-memory list based on the provided task ID.

    Parameters:
        task_id (UUID): The unique identifier of the task to be deleted.

    Returns:
        Task: The task object with the provided task ID, or raises HTTPException with status code 404 if the task is not found.

    Raises:
        HTTPException: If the task is not found in the list.
    """
    for index, task in enumerate(tasks):
        if task.id == task_id:
            return tasks.pop(index)
    raise HTTPException(status_code=404, detail="Task Not Found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=8000)