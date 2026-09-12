from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.postgres.aio import AsyncPostgresStore

from app.core.agent.nodes import generate_queries_or_respond, response, call_web_search, embed_store_search, rewrite_queries, generate_no_answer, generate_answer
from app.core.agent.conditional_edges import continue_to_search, check_docs_relevance
from app.core.agent.state import InputState, OverallState, OutputState
from app.core.agent.context import Context

async def create_graph(checkpointer: AsyncPostgresSaver, store: AsyncPostgresStore):
    workflow = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState, context_schema=Context)

    workflow.add_node(generate_queries_or_respond)
    workflow.add_node(response)
    workflow.add_node(call_web_search)
    workflow.add_node(embed_store_search)
    workflow.add_node(rewrite_queries)
    workflow.add_node(generate_answer)
    workflow.add_node(generate_no_answer)

    workflow.add_edge(START, "generate_queries_or_respond")
    workflow.add_conditional_edges(
        "generate_queries_or_respond",
        continue_to_search
    )
    workflow.add_edge("call_web_search", "embed_store_search")
    workflow.add_conditional_edges(
        "embed_store_search", 
        check_docs_relevance
    )
    workflow.add_conditional_edges(
        "rewrite_queries",
        continue_to_search
    )
    workflow.add_edge("generate_no_answer", END)
    workflow.add_edge("generate_answer", END)
    workflow.add_edge("response", END)

    return workflow.compile(checkpointer=checkpointer, store=store)