from langgraph.graph import StateGraph, START, END

from app.core.agent.nodes import generate_queries_or_respond, response, call_web_search, embed_and_store_searches, rewrite_queries, generate_no_answer, generate_answer
from app.core.agent.conditional_edges import continue_to_search_tool, check_docs_relevance
from app.core.agent.state import InputState, OverallState, OutputState

workflow = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState)

workflow.add_node(generate_queries_or_respond)
workflow.add_node(response)
workflow.add_node(call_web_search)
workflow.add_node(embed_and_store_searches)
workflow.add_node(rewrite_queries)
workflow.add_node(generate_answer)
workflow.add_node(generate_no_answer)

workflow.add_edge(START, "generate_queries_or_respond")
workflow.add_conditional_edges(
    "generate_queries_or_respond",
    continue_to_search_tool
)
workflow.add_edge("call_web_search", "embed_and_store_searches")
workflow.add_conditional_edges(
    "embed_and_store_searches", 
    check_docs_relevance
)
workflow.add_edge("rewrite_queries", "call_web_search")
workflow.add_edge("generate_no_answer", END)
workflow.add_edge("generate_answer", END)
workflow.add_edge("response", END)

