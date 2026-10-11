from functools import lru_cache

from langchain_openai import ChatOpenAI

from settings import settings


@lru_cache(maxsize=1)
def create_llm() -> ChatOpenAI:
    """Create and reuse the LangChain chat model through OpenRouter."""
    
    return ChatOpenAI(
        model = settings.openrouter_model,
        api_key = settings.openrouter_api_key,
        base_url = settings.openrouter_base_url,
        temperature = 0.2,
        max_retries = 2,
        timeout = 60,
    )