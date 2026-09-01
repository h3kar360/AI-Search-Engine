from langchain_core.documents import Document
from langchain.tools import tool

from app.db.vector_store import get_retriever

@tool
async def retrieve_search_results(query: str) -> list[Document]:
    """Search and return stored documents/searches based on the query given"""
    retriever = get_retriever()
    retrieved_docs = await retriever.ainvoke(query)
    return retrieved_docs
    
