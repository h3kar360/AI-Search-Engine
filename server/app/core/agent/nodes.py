import uuid

from app.core.agent.state import InputState, OverallState, OutputState
from app.core.llm import get_web_search_llm, get_llm, get_rewrite_llm
from app.models.llm_schema import RouteWebSearch
from app.tools.web_search_tool import web_search_tool
from app.core.agent.state import SearchingDistributorState
from app.core.agent.prompts import ROUTER_PROMPT, GENERATE_PROMPT, REWRITE_PROMPT
from app.db.vector_store import get_memory_vector_store
from app.core.agent.context import Context

from langgraph.config import get_stream_writer
from langchain.messages import AIMessage, ToolMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.runtime import Runtime

from datetime import datetime

n = 3

async def generate_queries_or_respond(state: InputState, runtime: Runtime[Context]) -> OverallState:
    """Call the model to generate a response based on the current state. Given
    the question, it will decide to generate queries to search online, or simply respond to the user.
    """
    query = state["query"]

    # Obtaining all relevant chat history / agent's memory from short and long term memory
    chat_history = state.get("messages", [])
    user_id = runtime.context.user_id
    namespace = ("memories", user_id)
    memories = await runtime.store.asearch(namespace, query=query)
    user_bound_memories = "\n".join([data.value["data"] for data in memories])

    writer = get_stream_writer()

    writer({
        "log": "Determining whether to generate queries to search or respond"
    })

    curr_date = datetime.now()
    format_curr_date = curr_date.strftime("%B %d, %Y")

    deciding_llm = get_web_search_llm()

    decision: RouteWebSearch = await deciding_llm.ainvoke([
        { "role": "system", "content": ROUTER_PROMPT.format(chat_history=chat_history, user_bound_memories=user_bound_memories, n=n, date=format_curr_date) },
        { "role": "user", "content": query }
    ])

    message = ""

    if decision.requires_web_search:
        writer({
            "log": "Generating relevant queries to search"
        })

        message = AIMessage("\n\n".join(query for query in decision.search_queries))
    else:
        writer({
            "log": "Generating respond and proceeding to response node"
        })

        message = AIMessage(decision.response)

    return {
        "query": state["query"],
        "queries": decision.search_queries,
        "requires_search": decision.requires_web_search,
        "response": decision.response,
        "queries_retries": 0,
        "messages": [message]
    }

async def call_web_search(state: SearchingDistributorState) -> OverallState:
    """Call the web search tool to get most recent and relevant information on recent matters"""
    writer = get_stream_writer()

    writer({
        "log": f"Calling web search tool to search about {state['query']}"
    })

    call_id = f"call_{uuid.uuid4().hex[:8]}"

    tool_call = {
        "name": "web_search_tool",
        "args": {
            "query": state["query"],
            "max_results": state["max_results"]
        },
        "id": call_id,
        "type": "tool_call"
    }

    tool_call_message = AIMessage(content="", tool_calls=[tool_call])

    retrieved_searched_docs = await web_search_tool.ainvoke(tool_call["args"])

    writer({
        "log": f"Successfully retrieved web pages on {state['query']}"
    })

    formatted_content = ""
    for doc in retrieved_searched_docs:
        formatted_content += f"content: {doc.page_content}\n\nsource: {doc.metadata["source"]}\n\n"

    tool_message = ToolMessage(content=formatted_content, tool_call_id=call_id)

    return {
        "retrieved_docs": retrieved_searched_docs or [],
        "messages": [tool_call_message, tool_message]
    }

async def embed_store_search(state: OverallState) -> OverallState:   
    """Embed all the retrieved documents and store it to an in memory vector store, then it searches for the most relevant chunk based on the query""" 
    docs_to_store = state["retrieved_docs"]

    # initialize in memory vector store here so python garbage collector will delete the all in memory stored documents after function ends
    vector_store = get_memory_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={ "k": 3 })

    writer = get_stream_writer()
    
    writer({
        "log": "Embedding and storing all retrieved documents"
    })

    if not docs_to_store:
        return {
            "vector_store_ids": [],
            "retrieved_docs": None
        }

    # split the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    docs_split = text_splitter.split_documents(docs_to_store)

    # add split documents to in memory vector store
    await vector_store.aadd_documents(docs_split)

    # search for relevant content/chunk from original query
    writer({
        "log": f"Using retrieved search results to formulate an answer on {state["query"]}"
    })

    retrieved_docs = await retriever.ainvoke(state["query"])

    docs_page_contents = []
    docs_sources = []
    message = ""

    # format the documents to string to be placed for messages
    for doc in retrieved_docs:
        docs_page_contents.append(doc.page_content)
        docs_sources.append(doc.metadata.get("source", "Unknown"))
        message += f"content: {doc.page_content}\n\nsource: {doc.metadata["source"]}\n\n"

    docs_as_text = "\n\n".join(docs_page_contents)
    
    message = AIMessage("Embedding all retrieved documents and storing it to an in memory vector store")

    return {
        "retrieved_docs": None,
        "sources": docs_sources,
        "search_result": docs_as_text,
        "messages": [message]
    }

# async def search_for_answer(state: OverallState) -> OverallState:
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
    message = ""

    for doc in retrieved_docs:
        docs_page_contents.append(doc.page_content)
        docs_sources.append(doc.metadata.get("source", "Unknown"))
        message += f"content: {doc.page_content}\n\nsource: {doc.metadata["source"]}\n\n"

    docs_as_text = "\n\n".join(docs_page_contents)

    return {
        "sources": docs_sources,
        "search_result": docs_as_text,
        "vector_store_ids": None,
        "messages": [message]
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
        "sources": state["sources"],
        "messages": [AIMessage(response.content)]
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

    message = ", ".join(query for query in new_queries.search_queries)

    return {
        "queries": new_queries.search_queries,
        "queries_retries": queries_retries + 1,
        "sources": None,
        "messages": [message]
    }

async def generate_no_answer(state: OverallState) -> OutputState:
    """Generate no answer because there are no relevant context in the web"""
    writer = get_stream_writer()
        
    writer({
        "log": "Generating response"
    })

    response = f"There are no relevant search results on '{state["query"]}'"
    message = AIMessage(response)

    return {
        "response": response,
        "sources": None,
        "messages": [message]
    }

def response(state: OverallState) -> OutputState:
    """Parse the state from overall state to the output state"""
    writer = get_stream_writer()
        
    writer({
        "log": "Generating response"
    })

    response = state["response"]
    message = AIMessage(response)

    return {
        "response": response,
        "sources": None,
        "messages": [message]
    }