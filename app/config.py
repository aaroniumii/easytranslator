from functools import lru_cache
from typing import Literal, Optional

from pydantic import BaseSettings, Field, root_validator


class Settings(BaseSettings):
    llm_provider: Literal["openai", "gemini"] = Field("openai", env="LLM_PROVIDER")
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4", env="OPENAI_MODEL")
    request_timeout: int = Field(30, env="OPENAI_TIMEOUT")
    gemini_api_key: Optional[str] = Field(None, env="GEMINI_API_KEY")
    gemini_model: str = Field("gemini-2.5-flash", env="GEMINI_MODEL")
    gemini_disable_thinking: bool = Field(False, env="GEMINI_DISABLE_THINKING")

    class Config:
        case_sensitive = False

    @root_validator
    def _validate_provider_configuration(cls, values: dict) -> dict:
        provider = values.get("llm_provider")
        if provider == "openai" and not values.get("openai_api_key"):
            raise ValueError("OPENAI_API_KEY must be set when LLM_PROVIDER is 'openai'.")
        if provider == "gemini" and not values.get("gemini_api_key"):
            raise ValueError("GEMINI_API_KEY must be set when LLM_PROVIDER is 'gemini'.")
        return values


@lru_cache()
def get_settings() -> Settings:
    return Settings()
