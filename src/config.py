from functools import cache
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class AgentSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    openai_model: str = "gpt-4o-mini"
    hf_embeddings_model: str = "intfloat/multilingual-e5-base"
    openai_api_key: str = ""
    store_path :str = "chess_expert_store"
    docs_path :str = "docs"


@cache
def get_agent_settings() -> AgentSettings:
    return AgentSettings()
