from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import AsyncGenerator


class Role(str, Enum):
    """Message role in a conversation."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class Message:
    """A message in a conversation."""

    role: Role
    content: str


class AIService(ABC):
    """Base class for AI model services."""

    @abstractmethod
    async def generate_response(
        self, messages: list[Message], stream: bool = True
    ) -> AsyncGenerator[str, None] | str:
        """Generate a response from the AI model.

        Args:
            messages: List of messages in the conversation
            stream: Whether to stream the response

        Returns:
            If stream=True, returns an async generator that yields response chunks.
            If stream=False, returns the complete response as a string.
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """Close any resources used by the service."""
        pass
