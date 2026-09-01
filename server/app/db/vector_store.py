import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
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

vector_store = PGVector(
    embeddings=embeddings,
    collection_name="web_docs",
    connection=engine
)

def get_vector_store() -> PGVector:
    return vector_store

def get_retriever(n: int = 2):
    return vector_store.as_retriever(
        search_kwargs={ "k": n }
    )