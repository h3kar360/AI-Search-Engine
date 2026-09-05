from langgraph.graph import StateGraph, START, END

from app.core.agent.nodes import generate_queries_or_respond, response, call_retrieve_results
from app.core.agent.custom_edges import continue_to_search_tool
from app.core.agent.state import *
from app.tools import *

workflow = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState)

workflow.add_node(generate_queries_or_respond)
workflow.add_node(response)
workflow.add_node(call_retrieve_results)

workflow.add_edge(START, "generate_queries_or_respond")
workflow.add_conditional_edges(
    "generate_queries_or_respond",
    continue_to_search_tool
)
workflow.add_edge("response", END)
