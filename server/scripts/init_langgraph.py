import sys
import asyncio

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.postgres.aio import AsyncPostgresStore

from app.db.agent_memory import (
    POSTGRES_DATABASE_URL,
    embeddings,
    embeddings_dimensions,
)


async def main():
    print("Setting up LangGraph checkpointer...")

    async with AsyncPostgresSaver.from_conn_string(
        POSTGRES_DATABASE_URL
    ) as checkpointer:
        await checkpointer.setup()

    print("Checkpointer setup complete.")

    print("Setting up LangGraph store...")

    async with AsyncPostgresStore.from_conn_string(
        POSTGRES_DATABASE_URL,
        index={
            "embed": embeddings,
            "dims": embeddings_dimensions,
        },
    ) as store:
        await store.setup()

    print("Store setup complete.")


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.run(
            main(),
            loop_factory=asyncio.SelectorEventLoop,
        )
    else:
        asyncio.run(main())