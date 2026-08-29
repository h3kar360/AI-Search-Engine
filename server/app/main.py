from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import router
from app.db.database import engine
from app.db.session import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)
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