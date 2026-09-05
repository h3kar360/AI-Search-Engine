import os

from langchain.tools import tool
from langchain_core.documents import Document
from tavily import AsyncTavilyClient
from dotenv import load_dotenv

load_dotenv()

@tool
async def web_search_tool(query: str, max_results: int) -> list[Document]:
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    tavily_client = AsyncTavilyClient(api_key=TAVILY_API_KEY)

    response = await tavily_client.search(query=query, search_depth="basic", max_results=max_results)
    raw_results = response.get("results", [])

    return [
        Document(
            page_content=item["content"],
            metadata={ "source": item["url"] }
        )
        for item in raw_results
    ]