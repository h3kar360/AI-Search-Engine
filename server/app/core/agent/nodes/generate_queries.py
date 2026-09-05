from langchain.messages import AIMessage

from app.core.llm import get_llm
from app.core.agent.state import OverallState
from app.models.llm_schema import Queries

GENERATE_QUERIES_SYSTEM_PROMPT = """
You are a search agent and you will write multiple relevant queries that do not overlap, 
but will generate meaningful queries that can make the most out of the search results in the internet.

Your query is: {query} 
You are only allowed to generate a maximum {number_of_queries} number of queries.
"""

async def generate_queries(state: OverallState) -> OverallState:
    """Generate relevant queries based on the query given to search online for relevant context"""
    n = 5

    generate_queries_model = get_llm()
    prompt = GENERATE_QUERIES_SYSTEM_PROMPT.format(
        query=state["query"],
        number_of_queries=n
    )

    queries = await generate_queries_model.with_structured_output(Queries).ainvoke(
        [{ "role": "user", "content": prompt }]
    )

    return {
        "queries": queries
    }
