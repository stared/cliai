from enum import Enum, auto
from dataclasses import dataclass


class Provider(str, Enum):
    """AI model providers supported by the application."""

    OPENAI = "OpenAI"
    ANTHROPIC = "Anthropic"
    GOOGLE = "Google"


@dataclass
class ModelConfig:
    """Configuration for an AI model."""

    id: str
    name: str
    provider: Provider
    max_tokens: int
    description: str


# Supported model configurations
AVAILABLE_MODELS = [
    ModelConfig(
        id="gpt-4.5-preview-2025-02-27",
        name="GPT-4.5 Preview",
        provider=Provider.OPENAI,
        max_tokens=4096,
        description="Most capable OpenAI model, preview version from Feb 2025",
    ),
    ModelConfig(
        id="gpt-4o-2024-08-06",
        name="GPT-4o",
        provider=Provider.OPENAI,
        max_tokens=4096,
        description="Optimized version of GPT-4 from Aug 2024",
    ),
    ModelConfig(
        id="claude-3-7-sonnet-20250219",
        name="Claude 3.7 Sonnet",
        provider=Provider.ANTHROPIC,
        max_tokens=4096,
        description="Claude 3.7 Sonnet model from Feb 2025",
    ),
    ModelConfig(
        id="claude-3-5-sonnet-20241022",
        name="Claude 3.5 Sonnet",
        provider=Provider.ANTHROPIC,
        max_tokens=4096,
        description="Claude 3.5 Sonnet model from Oct 2024",
    ),
    ModelConfig(
        id="gemini-pro",
        name="Gemini Pro",
        provider=Provider.GOOGLE,
        max_tokens=4096,
        description="Google's Gemini Pro language model",
    ),
]


DEFAULT_MODEL_ID = "gpt-4o-2024-08-06"


def get_model_by_id(model_id: str) -> ModelConfig | None:
    """Get model configuration by ID."""
    for model in AVAILABLE_MODELS:
        if model.id == model_id:
            return model
    return None


def get_models_by_provider(provider: Provider) -> list[ModelConfig]:
    """Get all models from a specific provider."""
    return [model for model in AVAILABLE_MODELS if model.provider == provider]


def get_default_model() -> ModelConfig:
    """Get the default model configuration."""
    model = get_model_by_id(DEFAULT_MODEL_ID)
    if model is None:
        # Fallback to first available model if default is not found
        return AVAILABLE_MODELS[0]
    return model
