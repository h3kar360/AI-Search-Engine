from app.core.agent.state import InputState, OverallState
from app.core.llm import get_llm



async def generate_queries_or_respond(state: InputState) -> OverallState:
    """Call the model to generate a response based on the current state. Given
    the question, it will decide to generate queries to search online with the generate_queries tool, 
    or simply respond to the user.
    """

    # get model instance
    response_model = get_llm()
    response = await response_model.ainvoke(state["query"])

    return {
        "query": state["query"],
        "messages": [response]
    }

    
