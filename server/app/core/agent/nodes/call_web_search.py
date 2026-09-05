from app.tools.web_search_tool import web_search_tool
from app.core.agent.state import SearchingDistributorState


async def call_web_search(state: SearchingDistributorState) -> SearchingDistributorState:
    retrieved_searched_docs = await web_search_tool.ainvoke({
        "query": state["query"],
        "search_depth": state["search_depth"]
    })

    return {
        "retrieved_docs": retrieved_searched_docs
    }
