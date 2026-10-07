import time
import uuid

from fastapi import Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def get_current_user(
    request: Request
):
    user = getattr(request.state, "user", None)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized"
        )

    return user

def rate_limit(endpoint: str, limit: int, window_seconds: int):
    async def dependency(request: Request):
        user = getattr(request.state, "user", None)
        user_id = user["uid"] if user else request.client.host

        key = f"rate:{endpoint}:{user_id}"
        now = time.time()

        request_id = uuid.uuid4().hex

        start_window = now - window_seconds

        redis_client = request.app.state.redis_client

        async with redis_client.pipeline(transaction=True) as pipe:
            pipe.zremrangebyscore(key, 0, start_window)
            pipe.zcard(key)
            pipe.zrange(key, 0, 0, withscores=True)
            pipe.zadd(key, { request_id: now })
            pipe.expire(key, window_seconds)
            results = await pipe.execute()

        current_count = results[1] + 1
        reached_limit = current_count > limit

        if reached_limit:
            retry_after = results[2][0][1] + window_seconds - now

            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Conversation limit has been met", 
                    "retry_after": retry_after
                }
            )

    return dependency


        