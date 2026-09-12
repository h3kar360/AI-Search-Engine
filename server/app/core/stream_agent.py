import json

from app.core.agent.context import Context

from langchain.messages import HumanMessage
from langgraph.graph import StateGraph

async def stream_agent(graph: StateGraph, input: dict, user_id: str, config: dict):
    query = input.get("user_message", "")
    

    async for chunk_mode, chunk_data in graph.astream(
        { 
            "query": query,
            "messages": [HumanMessage(query)]
        },
        stream_mode=["custom", "messages"],
        config=config, 
        version="v3",
        context=Context(user_id=user_id)
    ):
        if chunk_mode == "custom":
            if chunk_data.get("sources"):
                payload = {
                            "type": "custom",
                            "log": chunk_data["log"],
                            "sources": chunk_data["sources"]
                        }
            else:
                payload = {
                            "type": "custom",
                            "log": chunk_data["log"],
                        }

            yield f"data: {json.dumps(payload)}\n\n"
        elif chunk_mode == "messages":
            msg, metadata = chunk_data
            payload = {
                "type": "messages",
                "message": msg.content,
                "node": metadata.get("langgraph_node", "")
            }

            yield f"data: {json.dumps(payload)}\n\n"