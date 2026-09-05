from pydantic import BaseModel, Field
from typing import Optional

class Queries(BaseModel):
    """Generate queries by creating a list of queries"""

    queries: list[str] = Field(
        description="The list of queries"
    )

class RouteWebSearch(BaseModel):
    """Decide whether the LLM requires to search the web for answers"""

    requires_web_search: bool = Field(
        description="True if the user's request requires external web search for a relevant response; False for direct answers or greetings."
    )

    search_queries: list[str] = Field(
        default_factory=list,
        description="To write multiple relevant queries that do not overlap, but will generate meaningful queries that can make the most out of the search results in the internet. Only if requires_tool is True"
    )

    response: Optional[str] = Field(
        default=None,
        description="Direct answer to the user if requires_tool is False."
    )

class GradeDocuments(BaseModel):
    """Grade documents using a binary score for relevance check."""

    binary_score: str = Field(
        description="Relevance score: 'yes' if relevant, or 'no' if not relevant"
    )