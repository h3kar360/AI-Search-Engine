from fastapi import APIRouter
from app.api.v1.conversations.conversations import convo_router
from app.api.v1.conversations.chat import chat_router

router = APIRouter()

router.include_router(convo_router, prefix="/conversations")
router.include_router(chat_router, prefix="/conversations/chat")