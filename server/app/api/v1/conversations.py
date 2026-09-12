import uuid
import json

from fastapi import APIRouter, Depends, HTTPException, status, Form, Request, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services import conversations
from app.models.schema import InsertConvo, ConvoInfoResponse, ConvoChatsResponse, RaiseMessage
from app.core.stream_agent import stream_agent
from app.core.agent.memory import process_memory

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

@convo_router.post("/chat")
async def chat_with_llm(request: Request, background_tasks: BackgroundTasks, user_message: str = Form(...)):
    graph = request.app.state.graph
    store = request.app.state.store
    convo_id = "chat_123"
    user_id = "user_123"

    config = {
            "configurable": {
                "thread_id": convo_id
            }
        }

    initial_state = await graph.aget_state(config)
    initial_messages = initial_state.values.get("messages", [])
    initial_index = len(initial_messages)

    async def event_generator():
        try:
            async for chunk in stream_agent(
                graph=graph, 
                input={"user_message": user_message}, 
                user_id=user_id,
                config=config
            ):
                yield chunk
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        finally:
            final_state = await graph.aget_state(config)

            all_messages = final_state.values.get("messages", [])
            recent_messages = all_messages[initial_index:]

            background_tasks.add_task(
                process_memory,
                store=store,
                user_id=user_id,
                recent_messages=recent_messages
            )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            # "X-Accel-Buffering": "no" 
        }
    )