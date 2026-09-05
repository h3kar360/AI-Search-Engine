import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from langchain_core.vectorstores import InMemoryVectorStore
from sqlalchemy.ext.asyncio import create_async_engine

from dotenv import load_dotenv

load_dotenv()

db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

embeddings_model = os.getenv("EMBEDDINGS_MODEL")

PGVECTOR_DATABASE_URL = f"postgresql+psycopg://{db_username}:{db_password}@{db_host}:{db_port}/ai_search_db"

engine = create_async_engine(PGVECTOR_DATABASE_URL)

embeddings = GoogleGenerativeAIEmbeddings(model=embeddings_model)

pgvector_store = PGVector(
    embeddings=embeddings,
    collection_name="web_docs",
    connection=engine
)

in_memory_vector_store = InMemoryVectorStore(embeddings)

def get_pgvector_store() -> PGVector:
    return pgvector_store

def get_memory_vector_store() -> InMemoryVectorStore:
    return in_memory_vector_store

def get_pgretriever(k: int = 2):
    return pgvector_store.as_retriever(
        search_kwargs={ "k": k }
    )

def get_in_memory_retriever(k: int = 2):
    return in_memory_vector_store.as_retriever(
        search_kwargs={ "k": k }
    )