from typing import Annotated, TypedDict, TypeVar

from langchain_core.documents import Document
from langgraph.graph import MessagesState

T = TypeVar("T")

def reset_add_list_reducers(existing: list[T], incoming: list[T] | None) -> list[str]:
    if incoming is None:
        return []

    return (existing or []) + incoming

class InputState(MessagesState):
    query: str

class OverallState(MessagesState, total=False):
    query: str
    queries: list[str]
    sources: Annotated[list[str], reset_add_list_reducers]
    search_result: str
    requires_search: bool
    response: str
    retrieved_docs: Annotated[list[Document], reset_add_list_reducers]
    queries_retries: int

class SearchingDistributorState(TypedDict):
    query: str
    max_results: int

class OutputState(MessagesState):
    response: str
    sources: list[str] | None