# AI Search Agent

An AI-powered search agent that can answer questions directly or search the web when more information is needed. It uses LangGraph to manage the workflow, evaluate retrieved information, and retry searches when the results are not relevant enough.

## Features

- **Intelligent routing:** Decides whether to answer a question directly or perform web research.
- **Parallel web search:** Generates multiple search queries and executes web searches in parallel using Tavily.
- **Vector search:** Generates embeddings for retrieved documents, stores them temporarily, and retrieves the three most relevant sources using vector similarity.
- **Relevance grading:** Evaluates retrieved documents before generating an answer.
- **Query rewriting:** Rewrites search queries when the retrieved documents are not relevant enough, with up to two retries.
- **Fallback responses:** Returns a no-answer response when relevant information cannot be found after the retry limit.
- **Conversation history:** Maintains conversation state across requests using LangGraph checkpoints.
- **Short-term and long-term memory:** Uses PostgreSQL and pgvector-backed storage to support conversation history and user-specific memories.
- **Authentication:** Uses Firebase Authentication to manage user identity and access.
- **Rate limiting:** Uses Redis to limit API requests and help control resource usage.
- **Streaming responses:** Streams agent updates and responses to the frontend.
- **Web interface:** Provides a chat interface for interacting with the agent and viewing responses.

## How It Works

The agent follows a multi-step workflow managed by LangGraph:

1. **Summarization:** Summarizes conversation history when needed to keep the context manageable.
2. **Query routing:** Determines whether the question can be answered directly or requires web research.
3. **Parallel search:** Generates multiple queries and searches the web using Tavily.
4. **Embedding and storage:** Converts retrieved documents into embeddings and stores them in a temporary vector store for retrieval.
5. **Retrieval:** Uses vector similarity to select the three most relevant documents.
6. **Relevance grading:** Evaluates whether the retrieved documents are relevant to the question.
7. **Query rewriting:** If the results are insufficient, rewrites the queries and repeats the search process, allowing up to two retries.
8. **Answer generation:** Generates an answer using relevant retrieved information, or returns a fallback response if sufficient information cannot be found.

Questions that do not require web research follow the direct-response path.

## Tech Stack

**Backend**

- Python
- FastAPI
- LangChain
- LangGraph

**AI and Search**

- Google Gemini
- Tavily Search API
- Google Generative AI Embeddings

**Database and Infrastructure**

- PostgreSQL
- pgvector
- Redis
- Firebase Authentication
- Docker

**Frontend**

- React
- TypeScript

## Architecture

The frontend sends user requests to the FastAPI backend. After authentication and request validation, LangGraph manages the agent workflow and its conditional routing.

PostgreSQL stores persistent conversation state and long-term memories, while pgvector supports vector-based memory retrieval. Redis provides rate limiting, and Tavily supplies web search results. The backend streams responses and updates to the frontend.

## Getting Started

### Prerequisites

- Python
- Node.js and npm
- PostgreSQL with pgvector support
- Redis
- Firebase project
- Tavily API key
- Google Gemini API key

### Configuration

Configure the required environment variables for your backend and frontend. These include your database connection, Redis connection, Firebase configuration, Tavily API key, and Google Gemini API key.

Do not commit API keys, service-account credentials, or other secrets to the repository.

### Run Locally

1. Clone the repository.
2. Configure the backend environment variables.
3. Install the backend dependencies using the project's dependency manager.
4. Initialize the database and required LangGraph persistence tables.
5. Start the FastAPI backend.
6. Configure the frontend environment variables.
7. Install the frontend dependencies and start the React development server.

Refer to the backend and frontend project configuration for the exact commands and environment variable names.

## Deployment

The application has been deployed with a hosted frontend and backend. The backend uses managed PostgreSQL and Redis services for persistence and rate limiting.

## Future Improvements

- Benchmark API performance and latency using k6.
- Build a retrieval evaluation dataset to measure search quality.
- Experiment with hybrid retrieval and reranking.
- Improve automated testing and continuous integration.
