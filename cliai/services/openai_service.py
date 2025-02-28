from typing import AsyncGenerator, Any

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

from ..config import ModelConfig, get_api_key, Provider
from .base import AIService, Message, Role


class OpenAIService(AIService):
    """Service for OpenAI models."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the OpenAI service.

        Args:
            model_config: Configuration for the model to use
        """
        self.model_config = model_config
        api_key = get_api_key(Provider.OPENAI)
        self.client = AsyncOpenAI(api_key=api_key)

    async def generate_response(
        self, messages: list[Message], stream: bool = True
    ) -> AsyncGenerator[str, None] | str:
        """Generate a response from the OpenAI model."""
        openai_messages = self._convert_messages(messages)

        if stream:
            return self._stream_response(openai_messages)
        else:
            return await self._complete_response(openai_messages)

    async def _complete_response(self, openai_messages: list[ChatCompletionMessageParam]) -> str:
        """Get a complete response from the model."""
        response = await self.client.chat.completions.create(
            model=self.model_config.id,
            messages=openai_messages,
            stream=False,
        )
        return response.choices[0].message.content or ""

    async def _stream_response(
        self, openai_messages: list[ChatCompletionMessageParam]
    ) -> AsyncGenerator[str, None]:
        """Stream a response from the model."""
        stream = await self.client.chat.completions.create(
            model=self.model_config.id,
            messages=openai_messages,
            stream=True,
        )

        async for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content

    def _convert_messages(self, messages: list[Message]) -> list[ChatCompletionMessageParam]:
        """Convert our message format to OpenAI's format."""
        return [{"role": message.role.value, "content": message.content} for message in messages]

    async def close(self) -> None:
        """Close the OpenAI client."""
        await self.client.close()
