import os

from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv

load_dotenv()

db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{db_username}:{db_password}@{db_host}:{db_port}/ai_search_db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)