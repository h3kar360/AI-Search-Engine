import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services import conversations
from app.models.schema import InsertConvo, ConvoInfoResponse, ConvoChatsResponse, RaiseMessage

convo_router = APIRouter()

@convo_router.post("/", response_model=ConvoInfoResponse)
async def add_new_convo(insert_convo: InsertConvo, db: AsyncSession = Depends(get_db)):
    return await conversations.create_conversation(db, insert_convo)

@convo_router.get("/", response_model=list[ConvoInfoResponse])
async def get_all_convos(db: AsyncSession = Depends(get_db)):
    return await conversations.get_all_conversations(db)

@convo_router.get("/{id}", response_model=ConvoChatsResponse)
async def get_convo(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    convo = await conversations.get_conversation_by_id(db, id)

    if not convo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Conversation with id {id} not found'
        )

    return convo

@convo_router.put("/{id}", response_model=ConvoInfoResponse)
async def update_convo_title(id: uuid.UUID, updated_convo: InsertConvo, db: AsyncSession = Depends(get_db)):
    convo = await conversations.update_conversation(db, id, updated_convo)

    if not convo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Conversation with id {id} not found'
        )

    return convo

@convo_router.delete("/{id}", response_model=RaiseMessage)
async def delete_convo(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    is_deleted = await conversations.delete_conversation(db, id)

    if not is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Conversation with id {id} not found'
        )

    return RaiseMessage(
        message=f"Successfully deleted conversation id: {id}"
    )