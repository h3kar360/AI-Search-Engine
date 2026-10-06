from fastapi import Request
from firebase_admin import auth

async def firebase_auth_middleware(request: Request, call_next):
    authorization = request.headers.get("Authorization")
    request.state.user = None

    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ", 1)[1]

        try:
            decoded_token = auth.verify_id_token(token)
            request.state.user = decoded_token
        except Exception:
            request.state.user = None

    response = await call_next(request)

    return response
