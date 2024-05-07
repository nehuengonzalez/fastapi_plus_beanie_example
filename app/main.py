from app.settings import TaskServiceBaseSettings
from app.things_routes import router as task_router

from contextlib import asynccontextmanager
from fastapi import FastAPI
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.cors import CORSMiddleware

from app.models import MongoThing

settings = TaskServiceBaseSettings()


DESCRIPTION = """
This API powers whatever I want to make

It supports:

- Account sign-up and management
- Something really cool that will blow your socks off
"""


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore
    """Initialize application services."""
    app.db = AsyncIOMotorClient(settings.mongo_url).account  # type: ignore[attr-defined]
    await init_beanie(app.db, document_models=[MongoThing])  # type: ignore[arg-type,attr-defined]
    print("Startup complete")
    yield
    print("Shutdown complete")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(task_router, tags=["things"], prefix="/things")
