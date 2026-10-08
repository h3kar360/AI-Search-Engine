import os

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.api.v1.router import router
from app.db.database import engine
from app.db.agent_memory import get_checkpointer, get_store
from app.core.redis import get_redis_client
from app.core.agent.graph import create_graph
from app.middleware.firebase import firebase_auth_middleware
# just initialize firebase in main
from app.core.firebase import firebase_app

load_dotenv()
CLIENT_URL = os.getenv("CLIENT_URL")

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with (
        get_checkpointer() as checkpointer,
        get_store() as store,
        get_redis_client() as redis_client
    ):
        app.state.store = store
        app.state.checkpointer = checkpointer
        app.state.redis_client = redis_client
        app.state.graph = await create_graph(checkpointer=checkpointer, store=store)
        yield

    await engine.dispose()

app = FastAPI(
    title="AI Search Engine",
    description="An AI search engine",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[CLIENT_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router, prefix="/api/v1")

app.middleware("http")(firebase_auth_middleware)

@app.get("/")
def root():
    return { "message": f"Thanks for helping us cold start up the server. Please head back on to {CLIENT_URL}" }