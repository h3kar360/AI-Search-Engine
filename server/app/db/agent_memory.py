import os

from contextlib import asynccontextmanager
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.postgres.aio import AsyncPostgresStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

embeddings_model = os.getenv("EMBEDDINGS_MODEL")
embeddings_dimensions = os.getenv("EMBEDDINGS_DIMENSIONS")

POSTGRES_DATABASE_URL = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/ai_search_db"

embeddings = GoogleGenerativeAIEmbeddings(model=embeddings_model)

@asynccontextmanager
async def get_checkpointer():
    async with AsyncPostgresSaver.from_conn_string(POSTGRES_DATABASE_URL) as checkpointer:
        # await checkpointer.setup()
        yield checkpointer

@asynccontextmanager
async def get_store():
    async with AsyncPostgresStore.from_conn_string(
        POSTGRES_DATABASE_URL,
        index={
            "embed": embeddings,
            "dims": embeddings_dimensions
        }
    ) as store:
        await store.setup()
        yield store