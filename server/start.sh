#!/bin/sh
set -e

echo "Running database migrations..."
uv run alembic upgrade head

echo "Initializing Langgraph's async saver and store..."
uv run python -m scripts.init_langgraph

echo "Starting the FastAPI application..."
exec uv run uvicorn app.main:app  \
    --host 0.0.0.0 \
    --port "${PORT:-8000}"