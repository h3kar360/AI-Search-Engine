from contextlib import asynccontextmanager
from sqlalchemy import text
from fastapi import FastAPI

from app.api.v1.router import router
from app.db.database import engine
from app.db.session import Base
from app.db.agent_memory import get_checkpointer, get_store
from app.core.agent.graph import create_graph

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
        # await conn.run_sync(Base.metadata.drop_all)
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

app.include_router(router, prefix="/api/v1")

@app.get("/")
def root():
    return { "message": "hello" }