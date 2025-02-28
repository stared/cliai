from typing import AsyncGenerator, List, Dict, Any

import anthropic
from anthropic import AsyncAnthropic

from ..config import ModelConfig, get_api_key, Provider
from .base import AIService, Message, Role


class AnthropicService(AIService):
    """Service for Anthropic Claude models."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the Anthropic service.

        Args:
            model_config: Configuration for the model to use
        """
        self.model_config = model_config
        api_key = get_api_key(Provider.ANTHROPIC)
        self.client = AsyncAnthropic(api_key=api_key)

    async def generate_response(
        self, messages: list[Message], stream: bool = True
    ) -> AsyncGenerator[str, None] | str:
        """Generate a response from the Anthropic model."""
        anthropic_messages = self._convert_messages(messages)

        if stream:
            return self._stream_response(anthropic_messages)
        else:
            return await self._complete_response(anthropic_messages)

    async def _complete_response(self, anthropic_messages: list[dict[str, Any]]) -> str:
        """Get a complete response from the model."""
        response = await self.client.messages.create(
            model=self.model_config.id,
            messages=anthropic_messages,
            max_tokens=self.model_config.max_tokens,
        )
        return response.content[0].text

    async def _stream_response(
        self, anthropic_messages: list[dict[str, Any]]
    ) -> AsyncGenerator[str, None]:
        """Stream a response from the model."""
        stream = await self.client.messages.create(
            model=self.model_config.id,
            messages=anthropic_messages,
            max_tokens=self.model_config.max_tokens,
            stream=True,
        )

        async for chunk in stream:
            if chunk.type == "content_block_delta" and chunk.delta.text:
                yield chunk.delta.text

    def _convert_messages(self, messages: list[Message]) -> list[dict[str, Any]]:
        """Convert our message format to Anthropic's format."""
        result = []
        for message in messages:
            # Anthropic doesn't have a direct system message,
            # so we'll convert system messages to user messages for now
            role = "user" if message.role == Role.SYSTEM else message.role.value
            result.append({"role": role, "content": message.content})
        return result

    async def close(self) -> None:
        """Close the Anthropic client."""
        await self.client.close()
