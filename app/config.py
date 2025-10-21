from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4", env="OPENAI_MODEL")
    request_timeout: int = Field(30, env="OPENAI_TIMEOUT")

    class Config:
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
