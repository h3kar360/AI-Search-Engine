import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db import ChatHistory
from app.models.schema import SendChat, SaveChat

async def send_chat(db: AsyncSession, query: SendChat) -> str:
    print()

async def save_chat(db: AsyncSession, chat_content: SaveChat) -> ChatHistory:
    db_chat = ChatHistory(**chat_content.model_dump())
    db.add(db_chat)
    await db.commit()
    await db.refresh(db_chat)
    return db_chat