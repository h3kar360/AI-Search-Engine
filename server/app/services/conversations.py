import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from app.models.db import Conversations
from app.models.schema import InsertConvo

async def create_conversation(db: AsyncSession, new_convo: InsertConvo) -> Conversations:
    db_convo = Conversations(**new_convo.model_dump())
    db.add(db_convo)
    await db.commit()
    await db.refresh(db_convo)
    return db_convo

async def get_all_conversations(db: AsyncSession) -> list[Conversations]:
    result = await db.execute(select(Conversations))
    return list(result.scalars().all())

async def get_conversation_by_id(db: AsyncSession, id: uuid.UUID) -> Conversations | None:
    return await db.get(Conversations, id)

async def update_conversation(db: AsyncSession, id: uuid.UUID, updated_convo: InsertConvo) -> Conversations | None:
    result = await db.execute(
        update(Conversations)
        .where(Conversations.id == id)
        .values(**updated_convo.model_dump())
        .returning(Conversations)
    )

    await db.commit()
    return result.scalar_one_or_none()

async def delete_conversation(db: AsyncSession, id: uuid.UUID) -> uuid.UUID | None:
    result = await db.execute(
        delete(Conversations)
        .where(Conversations.id == id)
        .returning(Conversations.id)
    )

    await db.commit()
    return result.scalar_one_or_none