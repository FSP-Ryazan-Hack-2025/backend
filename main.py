import os
import uvicorn

from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.staticfiles import StaticFiles

from src.users.user_routers import router as users_router
# from src.users.admin_routers import router as admin_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.system("alembic upgrade head")

    yield


app = FastAPI(
    title="Ryazan-Hack-Backend",
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory="assets"))


@app.get("/ping")
async def ping_pong():
    return "pong"


app.include_router(users_router)
# app.include_router(admin_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0"
    )
