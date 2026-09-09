from typing import Literal

from langgraph.types import Send
from langgraph.config import get_stream_writer

from app.core.agent.state import OverallState, SearchingDistributorState
from app.core.agent.prompts import GRADE_PROMPT
from app.core.llm import get_grading_llm

def continue_to_search(state: OverallState) -> list[Send] | str:
    """Sends parallel nodes to search for each queries generated"""
    requires_search = state.get("requires_search", False)
    queries = state.get("queries", [])

    writer = get_stream_writer()
        
    writer({
        "log": "Allocating parallel agents to search the web"
    })

    if not requires_search:
        return "response"
    
    if requires_search and not queries:
        return "generate_no_answer"

    sends = []
    for query in state.get("queries", []):
        payload: SearchingDistributorState = {
            "query": query,
            "max_results": 2
        }
        
        sends.append(Send("call_web_search", payload))

    return sends

async def check_docs_relevance(state: OverallState) -> Literal["generate_answer", "rewrite_queries", "generate_no_answer"]:
    """Determine whether the retrieved documents are relevant to the user's query"""
    query = state["query"]
    context = state["search_result"]
    queries_retries = state["queries_retries"]

    writer = get_stream_writer()
        
    writer({
        "log": "Determining quality of search results"
    })

    grade_llm = get_grading_llm()
    prompt = GRADE_PROMPT.format(question=query, context=context)

    response = await grade_llm.ainvoke([
        { "role": "user", "content": prompt },
    ])

    score = response.binary_score.strip().lower()

    if score == "yes":
        return "generate_answer"
    elif queries_retries >= 2:
        return "generate_no_answer"
    else:
        return "rewrite_queries"
    