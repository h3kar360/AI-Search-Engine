from app.core.agent.state import InputState, OverallState, OutputState
from app.core.llm import get_web_search_llm, get_llm, get_rewrite_llm
from app.models.llm_schema import RouteWebSearch
from app.tools.web_search_tool import web_search_tool
from app.core.agent.state import SearchingDistributorState
from app.core.agent.prompts import ROUTER_PROMPT, GENERATE_PROMPT, REWRITE_PROMPT
from app.db.vector_store import get_memory_vector_store

from langgraph.config import get_stream_writer

from datetime import datetime

vector_store = get_memory_vector_store()
retriever = vector_store.as_retriever(search_kwargs={ "k": 3 })

n = 3

async def generate_queries_or_respond(state: InputState) -> OverallState:
    """Call the model to generate a response based on the current state. Given
    the question, it will decide to generate queries to search online, or simply respond to the user.
    """

    writer = get_stream_writer()

    writer({
        "log": "Determining whether to generate queries to search or respond"
    })

    curr_date = datetime.now()
    format_curr_date = curr_date.strftime("%B %d, %Y")

    deciding_llm = get_web_search_llm()

    decision: RouteWebSearch = await deciding_llm.ainvoke([
        { "role": "system", "content": ROUTER_PROMPT.format(n=n, date=format_curr_date) },
        { "role": "user", "content": state["query"] }
    ])

    if decision.requires_web_search:
        writer({
            "log": "Generating relevant queries to search"
        })
    else:
        writer({
            "log": "Generating respond and proceeding to response node"
        })

    return {
        "query": state["query"],
        "queries": decision.search_queries,
        "requires_search": decision.requires_web_search,
        "response": decision.response,
        "queries_retries": 0
    }

async def call_web_search(state: SearchingDistributorState) -> OverallState:
    """Call the web search tool to get most recent and relevant information on recent matters"""
    writer = get_stream_writer()

    writer({
        "log": f"Calling web search tool to search about {state['query']}"
    })

    retrieved_searched_docs = await web_search_tool.ainvoke({
        "query": state["query"],
        "max_results": state["max_results"]
    })

    writer({
        "log": f"Successfully retrieved web pages on {state['query']}"
    })

    return {
        "retrieved_docs": retrieved_searched_docs or []
    }

async def embed_and_store_searches(state: OverallState) -> OverallState:   
    """Embed all the retrieved documents and store it to an in memory vector store to be used later""" 
    docs_to_store = state["retrieved_docs"]

    writer = get_stream_writer()
    
    writer({
        "log": "Embedding and storing all retrieved documents"
    })

    if not docs_to_store:
        return {
            "vector_store_ids": [],
            "retrieved_docs": None
        }

    ids = await vector_store.aadd_documents(docs_to_store)

    return {
        "vector_store_ids": ids,
        "retrieved_docs": None
    }

async def search_for_answer(state: OverallState) -> OverallState:
    """Search through the vector store to get the most relevant context to the user's query"""
    writer = get_stream_writer()

    try:
        writer({
            "log": f"Using retrieved search results to formulate an answer on {state["query"]}"
        })
        retrieved_docs = await retriever.ainvoke(state["query"])
    finally:
        if state.get("vector_store_ids"):
            await vector_store.adelete(ids=state["vector_store_ids"])

    docs_page_contents = []
    docs_sources = []

    for doc in retrieved_docs:
        docs_page_contents.append(doc.page_content)
        docs_sources.append(doc.metadata.get("source", "Unknown"))

    docs_as_text = "\n\n".join(docs_page_contents)

    return {
        "sources": docs_sources,
        "search_result": docs_as_text,
        "vector_store_ids": None
    }

async def generate_answer(state: OverallState) -> OutputState:
    """Generate an answer based on all the context given and the user's query"""
    writer = get_stream_writer()
    
    writer({
        "log": "Generating response"
    })

    llm = get_llm()
    prompt = GENERATE_PROMPT.format(question=state["query"], context=state["search_result"])

    response = await llm.ainvoke([
        { "role": "user", "content": prompt }
    ])

    writer({
        "log": "Response has been generated",
        "sources": state["sources"]
    })

    return {
        "response": response.content,
        "sources": state["sources"]
    }

async def rewrite_queries(state: OverallState) -> OverallState:
    """Rewrite the queries to be better quality so it should get the most relevant and high quality information in the web"""
    queries_retries = state["queries_retries"]
    queries = state["queries"]
    query = state["query"]

    writer = get_stream_writer()
        
    writer({
        "log": "Rewriting queries to search for better search results"
    })

    rewrite_llm = get_rewrite_llm()

    queries_as_str = "\n\n".join(q for q in queries)

    prompt = REWRITE_PROMPT.format(question=query, queries=queries_as_str, n=n)

    new_queries = await rewrite_llm.ainvoke([
        { "role": "user", "content": prompt }
    ])

    return {
        "queries": new_queries.search_queries,
        "queries_retries": queries_retries + 1,
        "sources": None
    }

async def generate_no_answer(state: OverallState) -> OutputState:
    """Generate no answer because there are no relevant context in the web"""
    writer = get_stream_writer()
        
    writer({
        "log": "Generating response"
    })

    return {
        "response": f"There are no search results on {state['query']}",
        "sources": None
    }

def response(state: OverallState) -> OutputState:
    """Parse the state from overall state to the output state"""
    writer = get_stream_writer()
        
    writer({
        "log": "Generating response"
    })

    return {
        "response": state["response"],
        "sources": None
    }