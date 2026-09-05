from langgraph.types import Send

from app.core.agent.state import OverallState, SearchingDistributorState

def continue_to_search_tool(state: OverallState) -> list[Send] | str:
    queries = state["queries"]

    sends = []

    if state["requires_search"]:
        return "response"

    for query in queries:
        payload: SearchingDistributorState = {
            "query": query,
            "search_depth": 2,
            "retrieved_docs": []
        }
        
        sends.append(Send("call_web_search", payload))

    return sends