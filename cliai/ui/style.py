"""Style definitions for the CLI AI Chat application."""

from rich.style import Style
from rich.theme import Theme


# Color definitions
COLORS = {
    "openai": "#00A67D",  # OpenAI green
    "anthropic": "#D0A215",  # Anthropic gold
    "google": "#4285F4",  # Google blue
    "user": "#9370DB",  # Purple for user
    "system": "#808080",  # Gray for system
    "assistant": "#4169E1",  # Royal blue for assistant
    "info": "#87CEEB",  # Sky blue for info messages
    "error": "#FF6347",  # Tomato red for errors
    "success": "#90EE90",  # Light green for success
    "warning": "#FFD700",  # Gold for warnings
    "highlight": "#FFA500",  # Orange for highlights
}


# Style definitions
STYLES = {
    "title": Style(color="white", bold=True),
    "subtitle": Style(color="white", italic=True),
    "info": Style(color=COLORS["info"]),
    "error": Style(color=COLORS["error"], bold=True),
    "success": Style(color=COLORS["success"]),
    "warning": Style(color=COLORS["warning"]),
    # Provider-specific styles
    "openai": Style(color=COLORS["openai"], bold=True),
    "anthropic": Style(color=COLORS["anthropic"], bold=True),
    "google": Style(color=COLORS["google"], bold=True),
    # Message styles
    "user_name": Style(color=COLORS["user"], bold=True),
    "user_message": Style(color="white"),
    "assistant_name": Style(color=COLORS["assistant"], bold=True),
    "assistant_message": Style(color="white"),
    "system_name": Style(color=COLORS["system"], bold=True),
    "system_message": Style(color=COLORS["system"]),
    # Input styles
    "prompt": Style(color=COLORS["highlight"], bold=True),
    "input": Style(color="white"),
    # Selection styles
    "selection": Style(color=COLORS["highlight"]),
    "selected": Style(color=COLORS["success"], bold=True),
    "unselected": Style(color="white"),
    # Command styles
    "command": Style(color=COLORS["info"], bold=True),
    "shortcut": Style(color=COLORS["highlight"], bold=True),
}


# Create a theme for use with Rich
THEME = Theme(
    {
        "info": COLORS["info"],
        "error": COLORS["error"],
        "success": COLORS["success"],
        "warning": COLORS["warning"],
        "user": COLORS["user"],
        "assistant": COLORS["assistant"],
        "system": COLORS["system"],
        "openai": COLORS["openai"],
        "anthropic": COLORS["anthropic"],
        "google": COLORS["google"],
        "highlight": COLORS["highlight"],
    }
)
