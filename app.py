# imports
import pydantic
from fastapi import FastAPI

# initialize the app
app: FastAPI = FastAPI()

# routers
@app.get("/")
async def read() -> dict[str, str]:
    return {"message": "Hello World from FastAPI"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=8000)