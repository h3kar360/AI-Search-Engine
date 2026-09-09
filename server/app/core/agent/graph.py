import json

from langgraph.graph import StateGraph, START, END

from app.core.agent.nodes import generate_queries_or_respond, response, call_web_search, embed_and_store_searches, search_for_answer, rewrite_queries, generate_no_answer, generate_answer
from app.core.agent.conditional_edges import continue_to_search, check_docs_relevance
from app.core.agent.state import InputState, OverallState, OutputState

workflow = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState)

workflow.add_node(generate_queries_or_respond)
workflow.add_node(response)
workflow.add_node(call_web_search)
workflow.add_node(embed_and_store_searches)
workflow.add_node(search_for_answer)
workflow.add_node(rewrite_queries)
workflow.add_node(generate_answer)
workflow.add_node(generate_no_answer)

workflow.add_edge(START, "generate_queries_or_respond")
workflow.add_conditional_edges(
    "generate_queries_or_respond",
    continue_to_search
)
workflow.add_edge("call_web_search", "embed_and_store_searches")
workflow.add_edge("embed_and_store_searches", "search_for_answer")
workflow.add_conditional_edges(
    "search_for_answer", 
    check_docs_relevance
)
workflow.add_conditional_edges(
    "rewrite_queries",
    continue_to_search
)
workflow.add_edge("generate_no_answer", END)
workflow.add_edge("generate_answer", END)
workflow.add_edge("response", END)

graph = workflow.compile()

async def stream_agent(input: dict):
    query = input.get("user_message", "")

    async for chunk in graph.astream(
        { "query": query },
        stream_mode=["custom", "messages"],
        version="v2"
    ):
        if chunk["type"] == "custom":
            if chunk["data"].get("sources"):
                payload = {
                            "type": "custom",
                            "log": chunk["data"]["log"],
                            "sources": chunk["data"]["sources"]
                        }
            else:
                payload = {
                            "type": "custom",
                            "log": chunk["data"]["log"],
                        }

            yield f"data: {json.dumps(payload)}\n\n"
        elif chunk["type"] == "messages":
            msg, metadata = chunk["data"]
            payload = {
                "type": "messages",
                "message": msg.content,
                "node": metadata.get("langgraph_node", "")
            }

            yield f"data: {json.dumps(payload)}\n\n"