from app.core.agent.state import InputState, OverallState
from app.core.llm import get_web_search_llm
from app.models.llm_schema import RouteWebSearch

ROUTER_PROMPT = """You are an intent router for an AI search engine.
Analyze the user query:
1. If it requires external information or real-time web search, set requires_web_search=True and generate a maximum of {n} amount of queries in 'search_queries'.
2. If it is a greeting, general knowledge query, or meta-question, set requires_web_search=False and provide a direct response in 'response'."""

async def generate_queries_or_respond(state: InputState) -> OverallState:
    """Call the model to generate a response based on the current state. Given
    the question, it will decide to generate queries to search online, or simply respond to the user.
    """

    deciding_llm = get_web_search_llm()

    decision: RouteWebSearch = await deciding_llm.ainvoke([
        { "role": "system", "content": ROUTER_PROMPT.format(n=3) },
        { "role": "user", "content": state["query"] }
    ])

    return {
        "query": state["query"],
        "queries": decision.search_queries,
        "requires_search": decision.requires_web_search,
        "response": decision.response
    }

    
