import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from app.models.db import Conversations
from app.models.schema import InsertConvo

from langgraph.graph import StateGraph

async def create_conversation(db: AsyncSession, new_convo: InsertConvo, user_id: str) -> Conversations:
    db_convo = Conversations(**new_convo.model_dump(), user_id=user_id)
    db.add(db_convo)
    await db.commit()
    await db.refresh(db_convo)
    return db_convo

async def get_all_conversations(db: AsyncSession, user_id: str) -> list[Conversations]:
    result = await db.execute(
        select(Conversations)
        .where(Conversations.user_id == user_id)
    )
    return list(result.scalars().all())

async def get_conversation_by_id(db: AsyncSession, graph: StateGraph, id: uuid.UUID, user_id: str) -> dict | None:
    result = await db.execute(
        select(Conversations)
        .where(Conversations.id == id, Conversations.user_id == user_id)
    )

    convo_exists = result.scalar_one_or_none()

    if not convo_exists:
        return None

    config = {
        "configurable": {
            "thread_id": str(id)
        }
    }

    state = await graph.aget_state(config)
    messages = state.values.get("messages", [])
    chat_history: list[dict] = []

    # might add pagincation in later versions...
    # current_msg_len = len(messages)
    # start_index = max(0, current_msg_len - limit)

    chat_history = [
        {
            "id": message.id,
            "role": message.type,
            "content": message.content,
            "sources": message.additional_kwargs.get("sources", [])
        }
        for message in messages 
        if message.type in ("human", "ai") and message.content and not (message.type == "ai" and getattr(message, "tool_calls", None))
    ]
    
    return {
        "id": convo_exists.id,
        "title": convo_exists.title,
        "chats": chat_history
    }

async def update_conversation(db: AsyncSession, id: uuid.UUID, updated_convo: InsertConvo, user_id: str) -> Conversations | None:
    result = await db.execute(
        update(Conversations)
        .where(Conversations.id == id, user_id == user_id)
        .values(**updated_convo.model_dump(), user_id=user_id)
        .returning(Conversations)
    )

    await db.commit()
    return result.scalar_one_or_none()

async def delete_conversation(db: AsyncSession, id: uuid.UUID, user_id: str) -> uuid.UUID | None:
    result = await db.execute(
        delete(Conversations)
        .where(Conversations.id == id, Conversations.user_id == user_id)
        .returning(Conversations.id)
    )

    await db.commit()
    return result.scalar_one_or_none()