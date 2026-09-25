import os

from contextlib import asynccontextmanager
from sqlalchemy import text
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.api.v1.router import router
from app.db.database import engine
from app.db.session import Base
from app.db.agent_memory import get_checkpointer, get_store
from app.core.agent.graph import create_graph
# just initialize firebase in main
from app.core.firebase import firebase_app

load_dotenv()
CLIENT_URL = os.getenv("CLIENT_URL")

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # await conn.execute(text("DROP SCHEMA public CASCADE"))
        # await conn.execute(text("CREATE SCHEMA public"))

        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))

        await conn.run_sync(Base.metadata.create_all)

    async with (
        get_checkpointer() as checkpointer,
        get_store() as store
    ):
        app.state.store = store
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

@app.get("/")
def root():
    return { "message": "hello" }