from pydantic import BaseModel, Field
from typing import Optional, Literal

class Queries(BaseModel):
    """Generate queries by creating a list of queries"""

    search_queries: list[str] = Field(
        default_factory=list,
        description="To write multiple relevant queries that do not overlap, but will generate meaningful queries that can make the most out of the search results in the internet. Only if requires_tool is True"
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

class Summarizer(BaseModel):
    """Summarize the recent message history"""

    content: str = Field(
        description="Write the summary of the conversation history. Seperate each point with '||'."
    )

class MemoryOperation(BaseModel):
    """Decide what operations to do in its long term memory"""

    operation: Literal["ADD", "UPDATE", "DELETE", "NOOP"] = Field(
        description="Decide what operation to use, choices: 'ADD' to insert a new piece of memory to storage, 'UPDATE' to update an existing memory in storage, 'DELETE' to delete an existing memory in storage, 'NOOP' for no operation."
    )

    key: str = Field(
        description="The key of which we want to 'UPDATE' or 'DELETE'. It can be extracted from the prompt."
    )

    value: Optional[str] = Field(
        description="The content that we want to add ('ADD') or update ('UPDATE') in the memory. Leave empty for 'DELETE'"
    )