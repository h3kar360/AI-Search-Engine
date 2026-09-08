import asyncio

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

print("it is running here")

async def stream_agent():
    print("--- STARTING STREAM TEST ---\n")
    async for chunk in graph.astream(
        {"query": "what is lake ontario renamed to in the USA right now?"},
        stream_mode=["updates", "custom"],
        version="v2"
    ):
        if chunk["type"] == "updates":
            for node_name, state in chunk["data"].items():
                print(f"Node {node_name} updated: {state}")
        elif chunk["type"] == "custom":
            print(f"Status: {chunk['data']['status']}")

if __name__ == "__main__":
    asyncio.run(stream_agent())