from pydantic import BaseModel, Field

class Queries(BaseModel):
    """Generate queries by creating a list of queries"""

    queries: list[str] = Field(
        description="The list of queries"
    )