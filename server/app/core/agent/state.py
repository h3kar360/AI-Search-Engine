from typing import Annotated, TypedDict, TypeVar

from langchain_core.documents import Document

T = TypeVar("T")

def reset_add_list_reducers(existing: list[T], incoming: list[T] | None) -> list[str]:
    if incoming is None:
        return []

    return (existing or []) + incoming

class InputState(TypedDict):
    query: str

class OverallState(TypedDict, total=False):
    query: str
    queries: list[str]
    sources: list[str]
    search_result: str
    requires_search: bool
    response: str
    vector_store_ids: Annotated[list[str], reset_add_list_reducers]
    retrieved_docs: Annotated[list[Document], reset_add_list_reducers]
    queries_retries: int

class SearchingDistributorState(TypedDict):
    query: str
    max_results: int

class OutputState(TypedDict):
    response: str