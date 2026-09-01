from typing import TypedDict

from langgraph.graph import MessagesState

class InputState(TypedDict):
    query: str

class OverallState(MessagesState):
    query: str
    queries: list[str]
    search_results: list[dict]

class OutputState(TypedDict):
    response: str