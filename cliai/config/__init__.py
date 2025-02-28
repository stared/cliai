"""Configuration module for CLI AI Chat."""

from .models import (
    Provider,
    ModelConfig,
    AVAILABLE_MODELS,
    DEFAULT_MODEL_ID,
    get_model_by_id,
    get_models_by_provider,
    get_default_model,
)

from .environment import (
    get_api_key,
    get_cache_dir,
    get_history_file,
    MissingAPIKeyError,
)

__all__ = [
    "Provider",
    "ModelConfig",
    "AVAILABLE_MODELS",
    "DEFAULT_MODEL_ID",
    "get_model_by_id",
    "get_models_by_provider",
    "get_default_model",
    "get_api_key",
    "get_cache_dir",
    "get_history_file",
    "MissingAPIKeyError",
]
