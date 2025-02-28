from typing import AsyncGenerator, Any, Awaitable, Callable

import google.generativeai as genai
from google.generativeai.types import GenerationConfig

from ..config import ModelConfig, get_api_key, Provider
from .base import AIService, Message, Role


class GoogleService(AIService):
    """Service for Google Gemini models."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the Google service.

        Args:
            model_config: Configuration for the model to use
        """
        self.model_config = model_config
        api_key = get_api_key(Provider.GOOGLE)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name=self.model_config.id,
            generation_config=GenerationConfig(
                max_output_tokens=self.model_config.max_tokens,
            ),
        )

    async def generate_response(
        self, messages: list[Message], stream: bool = True
    ) -> AsyncGenerator[str, None] | str:
        """Generate a response from the Google model."""
        google_messages = self._convert_messages(messages)

        if stream:
            return self._stream_response(google_messages)
        else:
            return await self._complete_response(google_messages)

    async def _complete_response(self, google_messages: list[dict[str, Any]]) -> str:
        """Get a complete response from the model."""
        chat = self.model.start_chat(history=google_messages)
        response = await chat.send_message_async("")
        return response.text

    async def _stream_response(
        self, google_messages: list[dict[str, Any]]
    ) -> AsyncGenerator[str, None]:
        """Stream a response from the model."""
        chat = self.model.start_chat(history=google_messages)

        async for chunk in chat.send_message_async("", stream=True):
            if chunk.text:
                yield chunk.text

    def _convert_messages(self, messages: list[Message]) -> list[dict[str, Any]]:
        """Convert our message format to Google's format."""
        result = []

        # Handle system message separately
        system_messages = [m for m in messages if m.role == Role.SYSTEM]
        user_messages = [m for m in messages if m.role != Role.SYSTEM]

        # Add system message as a parameter if present
        if system_messages:
            # For now we just use the first system message
            system_content = system_messages[0].content
        else:
            system_content = None

        # Convert remaining messages
        for message in user_messages:
            role = "user" if message.role == Role.USER else "model"
            result.append({"role": role, "parts": [message.content]})

        return result

    async def close(self) -> None:
        """Close the Google client."""
        # Google Generative AI client doesn't need explicit closing
        pass
