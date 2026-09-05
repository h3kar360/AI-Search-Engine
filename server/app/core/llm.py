from langchain.chat_models import init_chat_model, BaseChatModel
from app.models.llm_schema import RouteWebSearch
from dotenv import load_dotenv

load_dotenv()

def get_llm(model_name: str = "google_genai:gemini-3.5-flash-lite", temperature: float = 0.7) -> BaseChatModel:
    return init_chat_model(model=model_name, temperature=temperature)

def get_web_search_llm(model_name: str = "google_genai:gemini-3.5-flash-lite", temperature: float = 0.0) -> BaseChatModel:
    web_search_llm = init_chat_model(model=model_name, temperature=temperature)
    return web_search_llm.with_structured_output(RouteWebSearch)