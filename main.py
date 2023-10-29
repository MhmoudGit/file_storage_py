from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from database import connect, disconnect
from config import app_configs
from api.routes import user


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    # Startup
    await connect()
    yield
    # Shutdown
    await disconnect()


app = FastAPI(
    **app_configs,
    lifespan=lifespan,
)

app.include_router(user.router)
