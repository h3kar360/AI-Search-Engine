import json
import uuid

from fastapi import APIRouter, Form, Request, BackgroundTasks, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from redis_fastapi import rate_limit

from app.core.stream_agent import stream_agent
from app.core.agent.memory import process_memory
from app.core.agent.graph import create_graph
from app.core.agent.context import Context
from app.dependencies import get_current_user

chat_router = APIRouter()

@chat_router.post("/{id}", dependencies=[Depends(rate_limit(
        "20/hour",
        on_limit_exceeded=lambda r, res: JSONResponse(
            { 
                "error": "Conversation limit has been met", "retry_after": res.retry_after
            }, status_code=429
        )
    ))])
async def chat_with_llm(request: Request, background_tasks: BackgroundTasks, id: uuid.UUID, 
                        user_message: str = Form(...), user = Depends(get_current_user)):
    graph = request.app.state.graph
    store = request.app.state.store
    convo_id = id
    user_id = user["uid"]

    config = {
            "configurable": {
                "thread_id": convo_id
            }
        }

    context = Context(user_id=str(user_id))

    initial_state = await graph.aget_state(config)
    initial_messages = initial_state.values.get("messages", [])
    initial_index = len(initial_messages)

    async def event_generator():
        try:
            async for chunk in stream_agent(
                graph=graph, 
                input={"user_message": user_message}, 
                context=context,
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

@chat_router.post("", dependencies=[Depends(rate_limit(
        "10/hour",
        on_limit_exceeded=lambda r, res: JSONResponse(
            { 
                "error": "Conversation limit has been met", "retry_after": res.retry_after
            }, status_code=429
        )
    ))])
async def chat_with_llm_as_guest(user_message: str = Form(...)):
    graph = await create_graph(checkpointer=None, store=None)

    async def event_generator():
        try:
            async for chunk in stream_agent(
                graph=graph, 
                input={"user_message": user_message},
                context=None,
                config=None
            ):
                yield chunk
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            # "X-Accel-Buffering": "no" 
        }
    )
