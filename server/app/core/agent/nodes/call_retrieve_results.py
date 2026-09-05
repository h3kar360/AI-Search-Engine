from app.core.agent.state import QueryDistributorState
from app.tools.retrieve_search_results import retrieve_search_results_tool

async def call_retrieve_results(state: QueryDistributorState) -> QueryDistributorState:
    retrieved_docs = await retrieve_search_results_tool.ainvoke({
        "query": state["query"],
        "search_depth": state["search_depth"]
    })

    return {
        "retrieved_docs": retrieved_docs
    }