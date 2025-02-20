from fastapi import FastAPI
from app import api
from app.db.connection import engine
from app.db.models import Task

app = FastAPI(title="Task Manager")
app.include_router(api.router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Task.metadata.create_all)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
