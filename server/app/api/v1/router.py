from fastapi import APIRouter
from app.api.v1.conversations import convo_router

router = APIRouter()

router.include_router(convo_router, prefix="/conversations")