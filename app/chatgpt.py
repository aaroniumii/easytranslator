from functools import lru_cache

from openai import OpenAI

from .config import get_settings


class ChatGPTClient:
    def __init__(self) -> None:
        settings = get_settings()
        self._client = OpenAI(api_key=settings.openai_api_key, timeout=settings.request_timeout)
        self._model = settings.openai_model

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
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text},
            ],
            temperature=0.3,
        )
        message = response.choices[0].message
        content = message.content if message and message.content else ""
        return content.strip()


@lru_cache()
def get_client() -> ChatGPTClient:
    return ChatGPTClient()
