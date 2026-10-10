import asyncio
from pathlib import Path

from app.core.agent.graph import create_graph

async def main():
    graph = await create_graph(checkpointer=None, store=None)

    png_data = graph.get_graph(xray=False).draw_mermaid_png()

    output_path = Path("graph.png")
    output_path.write_bytes(png_data)

    print(f"Graph saved to {output_path.resolve()}")


if __name__ == "__main__":
    asyncio.run(main())