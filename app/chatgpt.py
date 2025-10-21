from functools import lru_cache
from typing import Any, Dict, Optional

from openai import OpenAI

from .config import get_settings


class ChatGPTClient:
    def __init__(self) -> None:
        settings = get_settings()
        self._provider = settings.llm_provider
        self._model = settings.openai_model
        self._request_timeout = settings.request_timeout
        self._gemini_types = None
        self._gemini_disable_thinking = settings.gemini_disable_thinking

        if self._provider == "openai":
            self._client = OpenAI(api_key=settings.openai_api_key)
        elif self._provider == "gemini":
            from google import genai  # type: ignore
            from google.genai import types  # type: ignore

            self._client = genai.Client(api_key=settings.gemini_api_key)
            self._model = settings.gemini_model
            self._gemini_types = types
        else:  # pragma: no cover - defensive branch for future providers
            raise ValueError(f"Unsupported LLM provider: {self._provider}")

    def translate(self, text: str, source_language: str, target_language: str) -> str:
        prompt = (
            "You are a professional translator. Translate the user's text from "
            f"{source_language} to {target_language}. Only respond with the translated text."
        )
        return self._complete(prompt, text)

    def correct(self, text: str, language: str) -> str:
        prompt = (
            "You are a meticulous editor. Improve the grammar, spelling, and logic of the "
            f"following {language} text. Return only the corrected version."
        )
        return self._complete(prompt, text)

    def _complete(self, system_prompt: str, user_text: str) -> str:
        if self._provider == "openai":
            response = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text},
                ],
                temperature=0.3,
                timeout=self._request_timeout,
            )
            message = response.choices[0].message
            content = ""
            if message and message.content:
                if isinstance(message.content, list):
                    content = "".join(
                        part.get("text", "") if isinstance(part, dict) else str(part)
                        for part in message.content
                    )
                else:
                    content = message.content
            return content.strip()

        if self._provider == "gemini" and self._gemini_types is not None:
            config_kwargs: Dict[str, Any] = {
                "temperature": 0.3,
                "system_instruction": system_prompt,
            }
            if self._gemini_disable_thinking:
                config_kwargs["thinking_config"] = self._gemini_types.ThinkingConfig(
                    thinking_budget=0
                )

            config = self._gemini_types.GenerateContentConfig(**config_kwargs)
            response = self._client.models.generate_content(  # type: ignore[attr-defined]
                model=self._model,
                contents=[user_text],
                config=config,
            )
            content: Optional[str] = getattr(response, "text", None)
            return (content or "").strip()

        raise RuntimeError(f"Unsupported provider configuration: {self._provider}")


@lru_cache()
def get_client() -> ChatGPTClient:
    return ChatGPTClient()
