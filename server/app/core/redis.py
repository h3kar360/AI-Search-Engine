import os
import redis.asyncio as redis

from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

redis_url = os.getenv("REDIS_URL")

@asynccontextmanager
async def get_redis_client():
    async with redis.Redis.from_url(redis_url) as redis_client:
        yield redis_client