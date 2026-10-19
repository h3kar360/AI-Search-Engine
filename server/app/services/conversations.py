import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from app.models.db import Conversations
from app.models.schema import InsertConvo   

from langgraph.graph import StateGraph
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

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

async def get_conversation_and_chats_by_id(db: AsyncSession, graph: StateGraph, id: uuid.UUID, user_id: str, limit: int = 10, page: int = 1) -> dict | None:
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
    chat_history: list[dict] = [
        {
            "id": message.id,
            "role": message.type,
            "content": message.content,
            "sources": message.additional_kwargs.get("sources", [])
        }
        for message in messages 
        if message.type in ("human", "ai") and message.content and not (message.type == "ai" and getattr(message, "tool_calls", None))
    ]

    curr_msg_len = len(chat_history)
    end = curr_msg_len - ((page - 1) * limit)
    start = max(0, end - limit)

    chats = []

    if end <= 0:
        chats = []
    else:
        chats = chat_history[start:end] 

    return {
        "id": convo_exists.id,
        "title": convo_exists.title,
        "chats": chats,
        "pagination": {
            "page": page,
            "limit": limit,
            "has_more": start > 0,
            "next_page": page + 1 if start > 0 else None
        }
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

async def delete_conversation(db: AsyncSession, id: uuid.UUID, user_id: str, checkpointer: AsyncPostgresSaver) -> uuid.UUID | None:
    result = await db.execute(
        delete(Conversations)
        .where(Conversations.id == id, Conversations.user_id == user_id)
        .returning(Conversations.id)
    )

    deleted_id = result.scalar_one_or_none()

    if deleted_id is None:
        return None

    await db.commit()

    await checkpointer.adelete_thread(id)

    return deleted_id