FROM python:3.14

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv
RUN uv sync --frozen

COPY . .

RUN chmod +x start.sh

EXPOSE 8000

CMD ["./start.sh"]
