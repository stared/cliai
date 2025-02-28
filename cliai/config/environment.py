import os
from pathlib import Path
from dotenv import load_dotenv

from .models import Provider


# Load environment variables from .env file
load_dotenv()


class MissingAPIKeyError(Exception):
    """Exception raised when an API key is missing."""

    def __init__(self, provider: Provider):
        self.provider = provider
        super().__init__(
            f"Missing API key for {provider.value}. Please set {self._get_env_var_name(provider)}."
        )

    @staticmethod
    def _get_env_var_name(provider: Provider) -> str:
        if provider == Provider.OPENAI:
            return "OPENAI_API_KEY"
        elif provider == Provider.ANTHROPIC:
            return "ANTHROPIC_API_KEY"
        elif provider == Provider.GOOGLE:
            return "GOOGLE_API_KEY"
        return "UNKNOWN_API_KEY"


def get_api_key(provider: Provider) -> str:
    """Get the API key for a specific provider from environment variables."""
    if provider == Provider.OPENAI:
        api_key = os.getenv("OPENAI_API_KEY")
    elif provider == Provider.ANTHROPIC:
        api_key = os.getenv("ANTHROPIC_API_KEY")
    elif provider == Provider.GOOGLE:
        api_key = os.getenv("GOOGLE_API_KEY")
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    if api_key is None or api_key.strip() == "":
        raise MissingAPIKeyError(provider)

    return api_key


def get_cache_dir() -> Path:
    """Get the cache directory for the application."""
    user_cache_dir = os.getenv("XDG_CACHE_HOME")
    if user_cache_dir:
        base_dir = Path(user_cache_dir)
    else:
        base_dir = Path.home() / ".cache"

    cache_dir = base_dir / "cliai"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def get_history_file() -> Path:
    """Get the path to the history file."""
    return get_cache_dir() / "history.json"
