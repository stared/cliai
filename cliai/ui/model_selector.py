"""Model selection UI for CLI AI Chat."""

from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..config import (
    ModelConfig,
    Provider,
    AVAILABLE_MODELS,
    get_default_model,
    get_model_by_id,
    get_models_by_provider,
)
from .style import STYLES, COLORS


def _create_model_table() -> Table:
    """Create a Rich table for displaying models."""
    table = Table(title="Available Models", expand=True)

    table.add_column("#", style="dim")
    table.add_column("Model", style="bold")
    table.add_column("Provider")
    table.add_column("Description")

    for i, model in enumerate(AVAILABLE_MODELS, 1):
        provider_style = model.provider.value.lower()

        table.add_row(
            str(i),
            model.name,
            f"[{provider_style}]{model.provider.value}[/{provider_style}]",
            model.description,
        )

    return table


def select_model(model_id: Optional[str] = None) -> ModelConfig:
    """Display a UI for selecting a model.

    Args:
        model_id: Optional model ID to use. If provided and valid, no UI is shown.

    Returns:
        The selected model configuration
    """
    console = Console()

    # If a model ID was provided and it's valid, use it without showing UI
    if model_id:
        model = get_model_by_id(model_id)
        if model:
            console.print(f"Using model: [bold]{model.name}[/bold]", style=STYLES["info"])
            return model
        else:
            console.print(
                f"Model '{model_id}' not found. Please select from available models:",
                style=STYLES["warning"],
            )

    # Show the model selection UI
    console.print(Panel.fit("Select an AI Model", style=STYLES["title"]))

    # Display available models
    table = _create_model_table()
    console.print(table)
    console.print()

    # Get user selection
    default_model = get_default_model()
    default_index = AVAILABLE_MODELS.index(default_model) + 1

    while True:
        try:
            choice = console.input(
                f"Enter model number [1-{len(AVAILABLE_MODELS)}] (default: {default_index}): "
            )

            if not choice:
                return default_model

            index = int(choice) - 1
            if 0 <= index < len(AVAILABLE_MODELS):
                selected_model = AVAILABLE_MODELS[index]
                console.print(
                    f"Selected: [bold]{selected_model.name}[/bold]", style=STYLES["success"]
                )
                return selected_model
            else:
                console.print(
                    f"Please enter a number between 1 and {len(AVAILABLE_MODELS)}",
                    style=STYLES["error"],
                )
        except ValueError:
            console.print("Please enter a valid number", style=STYLES["error"])
