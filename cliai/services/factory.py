from ..config import ModelConfig, Provider
from .base import AIService
from .openai_service import OpenAIService
from .anthropic_service import AnthropicService
from .google_service import GoogleService


def get_service_for_model(model_config: ModelConfig) -> AIService:
    """Create an AI service for the specified model.

    Args:
        model_config: Configuration for the model to use

    Returns:
        An appropriate AIService instance for the model

    Raises:
        ValueError: If the provider is not supported
    """
    if model_config.provider == Provider.OPENAI:
        return OpenAIService(model_config)
    elif model_config.provider == Provider.ANTHROPIC:
        return AnthropicService(model_config)
    elif model_config.provider == Provider.GOOGLE:
        return GoogleService(model_config)
    else:
        raise ValueError(f"Unsupported provider: {model_config.provider}")
