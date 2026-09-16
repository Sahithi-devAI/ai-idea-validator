import os
from abc import ABC, abstractmethod

import anthropic


class LLMProvider(ABC):
    @abstractmethod
    def complete(self, system: str, messages: list, max_tokens: int = 1500) -> str:
        pass


class AnthropicProvider(LLMProvider):
    def __init__(self, model: str | None = None):
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        self.model = model or os.getenv("LLM_MODEL", "claude-sonnet-4-6")

    def complete(self, system: str, messages: list, max_tokens: int = 1500) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=messages,
        )
        return response.content[0].text


# V2: add OllamaProvider / vLLMProvider here, same interface

PROVIDERS: dict[str, type[LLMProvider]] = {
    "anthropic": AnthropicProvider,
}


def get_provider(provider: str = "anthropic") -> LLMProvider:
    cls = PROVIDERS.get(provider)
    if cls is None:
        raise ValueError(f"Unknown provider '{provider}'. Available: {list(PROVIDERS)}")
    return cls()
