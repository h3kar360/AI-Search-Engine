import uuid

from langgraph.store.postgres.aio import AsyncPostgresStore

from app.core.llm import get_operator_llm, get_summarizer_llm
from app.core.agent.prompts import MEMORY_EXTRACTION_PROMPT, MEMORY_OPERATION_PROMPT

async def process_memory(store: AsyncPostgresStore, user_id: str, recent_messages: list[str]):
    operator_llm = get_operator_llm()
    summarizer_llm = get_summarizer_llm()

    namespace = ("memories", user_id)

    conversation = "\n".join(
        f"{msg.type}: {msg.content}" if hasattr(msg, "content") else str(msg)
        for msg in recent_messages
    )

    memory_extract_prompt = MEMORY_EXTRACTION_PROMPT.format(conversation=conversation)
    summarized_history = await summarizer_llm.ainvoke([
        { "role": "user", "content": memory_extract_prompt }
    ])

    candidate_memories = summarized_history.content

    existing_memories = await store.asearch(namespace, query=candidate_memories, limit=3)
    existing_memories_text = "\n".join(
        f"- Key: {memory.key} | Value: {memory.value.get("data", "")}"
        for memory in existing_memories
    )

    memory_operation_prompt = MEMORY_OPERATION_PROMPT.format(existing_memories=existing_memories_text, candidate_memories=candidate_memories)
    operations = await operator_llm.ainvoke([
        { "role": "user", "content": memory_operation_prompt }
    ])

    if operations.operation == "ADD":
        await store.aput(namespace, str(uuid.UUID), { "data": operations.value })
    elif operations.operation == "UPDATE":
        await store.aput(namespace, operations.key, { "data": operations.value })
    elif operations.operation == "DELETE":
        await store.adelete(namespace, operations.key)
    elif operations.operation == "NOOP":
        return
    