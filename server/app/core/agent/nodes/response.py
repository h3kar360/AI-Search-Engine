
from app.core.agent.state import OutputState, OverallState


def response(state: OverallState) -> OutputState:
    return {
        "response": state["response"]
    }