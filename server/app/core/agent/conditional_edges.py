from typing import Literal

from langgraph.types import Send

from app.core.agent.state import OverallState, SearchingDistributorState
from server.app.core.agent.prompts import GRADE_PROMPT
from server.app.core.llm import get_grading_llm

def continue_to_search_tool(state: OverallState) -> list[Send] | str:
    if not state.get("requires_search", False):
        return "response"

    sends = []
    for query in state.get("queries", []):
        payload: SearchingDistributorState = {
            "query": query,
            "search_depth": 2,
            "retrieved_docs": []
        }
        
        sends.append(Send("call_web_search", payload))

    return sends


def check_docs_relevance(state: OverallState) -> Literal["generate_answer", "rewrite_queries"]:
    """Determine whether the retrieved documents are relevant to the user's query"""
    query = state["query"]
    context = state["search_result"]

    grade_llm = get_grading_llm()
    prompt = GRADE_PROMPT.format(question=query, context=context)

    response = grade_llm.ainvoke([
        { "role": "user", "content": prompt },
    ])

    if response.binary_score == "yes":
        return "generate_answer"

    return "rewrite_queries"
    