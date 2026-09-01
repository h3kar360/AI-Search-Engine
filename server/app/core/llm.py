import os

from langchain.chat_models import init_chat_model, BaseChatModel
from dotenv import load_dotenv

load_dotenv()

def get_llm(model_name: str = "google_genai:gemini-3.5-flash-lite", temperature: float = 0.7) -> BaseChatModel:
    return init_chat_model(model=model_name, temperature=temperature)