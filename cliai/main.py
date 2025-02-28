"""Main CLI application for CLI AI Chat."""

import asyncio
from typing import Optional, List, Annotated

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .config import (
    ModelConfig,
    Provider,
    AVAILABLE_MODELS,
    get_model_by_id,
    MissingAPIKeyError,
)
from .services import get_service_for_model, Message, Role
from .ui import select_model, ChatInterface, STYLES


# Create the Typer app
app = typer.Typer(
    name="cliai",
    help="Chat with AI models through a command-line interface",
    add_completion=False,
)

console = Console()


@app.command("chat")
def chat_command(
    model: Annotated[
        Optional[str],
        typer.Option(
            "--model",
            "-m",
            help="Model ID to use for chat",
        ),
    ] = None,
    system: Annotated[
        Optional[str],
        typer.Option(
            "--system",
            "-s",
            help="Initial system message",
        ),
    ] = None,
    continue_conversation: Annotated[
        bool,
        typer.Option(
            "--continue",
            "-c",
            help="Continue the previous conversation instead of starting a new one",
        ),
    ] = False,
) -> None:
    """Start a chat session with an AI model."""
    # Default is to start a new conversation, unless --continue is specified
    asyncio.run(_chat_async(model, system, not continue_conversation))


@app.command("models")
def models_command() -> None:
    """List all available AI models."""
    table = Table(title="Available Models")

    table.add_column("Model ID", style="bold")
    table.add_column("Name")
    table.add_column("Provider", style="cyan")
    table.add_column("Description")

    for model in AVAILABLE_MODELS:
        provider_style = model.provider.value.lower()

        table.add_row(
            model.id,
            model.name,
            f"[{provider_style}]{model.provider.value}[/{provider_style}]",
            model.description,
        )

    console.print(table)


async def _chat_async(
    model_id: Optional[str] = None, system_message: Optional[str] = None, new: bool = False
) -> None:
    """Run the chat interface asynchronously.

    Args:
        model_id: Optional model ID to use
        system_message: Optional system message
        new: Whether to start a new conversation
    """
    try:
        # Select the model to use
        model_config = select_model(model_id)

        # Create the service for the model
        service = get_service_for_model(model_config)

        # Create the chat interface
        chat = ChatInterface(model_config, service, new_conversation=new)

        # Set custom system message if provided
        if system_message:
            # Replace existing system messages
            chat.messages = [m for m in chat.messages if m.role != Role.SYSTEM]
            chat.messages.insert(0, Message(role=Role.SYSTEM, content=system_message))

        # Run the chat interface
        async for _ in chat.run():
            # We don't need to do anything with the yielded panels
            pass

    except MissingAPIKeyError as e:
        console.print(Panel(f"Error: {e}", title="API Key Missing", border_style=STYLES["error"]))

        # Suggest setting up the API key
        provider_env_var = e._get_env_var_name(e.provider)
        console.print(
            f"\nPlease set the {provider_env_var} environment variable or add it to your .env file."
        )
        console.print(f"You can get an API key from the {e.provider.value} website.")

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        console.print("\nExiting chat.", style=STYLES["info"])

    except Exception as e:
        console.print(f"Error: {e}", style=STYLES["error"])


if __name__ == "__main__":
    app()
