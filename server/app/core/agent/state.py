import operator
from typing import Annotated, TypedDict

from langchain_core.documents import Document

class InputState(TypedDict):
    query: str

class OverallState(TypedDict):
    query: str
    queries: list[str]
    search_results: list[dict]
    requires_search: bool
    response: str

class SearchingDistributorState(TypedDict):
    query: str
    search_depth: int
    retrieved_docs: Annotated[list[Document], operator.add]

class OutputState(TypedDict):
    response: str