import json

from app.core.agent.context import Context

from langchain.messages import HumanMessage
from langgraph.graph import StateGraph

async def stream_agent(graph: StateGraph, input: dict, context: Context | None, config: dict | None):
    query = input.get("user_message", "")
    

    async for chunk_mode, chunk_data in graph.astream(
        { 
            "query": query,
            "messages": [HumanMessage(query)]
        },
        stream_mode=["custom", "messages"],
        config=config, 
        version="v3",
        context=context
    ):
        if chunk_mode == "custom":
            payload = {
                        "type": "custom",
                        "log": chunk_data["log"],
                    }

            yield f"data: {json.dumps(payload)}\n\n"
        elif chunk_mode == "messages":
            msg, metadata = chunk_data
            payload = {
                "type": "messages",
                "role": msg.type,
                "message": msg.content,
                "additional_kwargs": msg.additional_kwargs,
                "node": metadata.get("langgraph_node", "")
            }

            yield f"data: {json.dumps(payload)}\n\n"