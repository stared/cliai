"""Chat interface UI for CLI AI Chat."""

import asyncio
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any, Generator, AsyncGenerator, Union
import os

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text
from rich.spinner import Spinner
from rich.console import RenderableType

from ..config import ModelConfig, get_history_file
from ..services import AIService, Message, Role
from .style import STYLES


class ChatInterface:
    """Interface for chatting with AI models."""

    def __init__(
        self, model_config: ModelConfig, service: AIService, new_conversation: bool = False
    ):
        """Initialize the chat interface.

        Args:
            model_config: Configuration for the model
            service: Service for communicating with the AI model
            new_conversation: Whether to start a new conversation regardless of history
        """
        self.model_config = model_config
        self.service = service
        self.console = Console()
        self.messages: list[Message] = []
        self.history_file = get_history_file()
        self.new_conversation = new_conversation
        self.show_user_messages = False  # Don't show user message panels for new messages

        # Add default system message
        self.messages.append(
            Message(
                role=Role.SYSTEM,
                content="You are a helpful AI assistant. Be concise but informative in your responses.",
            )
        )

        # Load conversation history if it exists and not starting a new conversation
        if not new_conversation:
            self._load_history()

    def _load_history(self) -> None:
        """Load conversation history from file if it exists."""
        try:
            if self.history_file.exists():
                with open(self.history_file, "r") as f:
                    history = json.load(f)

                # Look for a conversation with this model
                for conversation in history:
                    if conversation.get("model_id") == self.model_config.id:
                        # Found a conversation with this model
                        for msg_data in conversation.get("messages", []):
                            role_str = msg_data.get("role")
                            content = msg_data.get("content", "")

                            try:
                                role = Role(role_str)
                                # Don't duplicate system messages
                                if role == Role.SYSTEM and any(
                                    m.role == Role.SYSTEM for m in self.messages
                                ):
                                    continue

                                self.messages.append(Message(role=role, content=content))
                            except (ValueError, TypeError):
                                # Skip invalid messages
                                continue

                        # Only load one conversation
                        break
        except (json.JSONDecodeError, IOError):
            # If there's an error loading history, just start fresh
            pass

    def _save_history(self) -> None:
        """Save conversation history to file."""
        try:
            history: list[dict[str, Any]] = []

            # Load existing history if it exists
            if self.history_file.exists():
                with open(self.history_file, "r") as f:
                    try:
                        history = json.load(f)
                    except json.JSONDecodeError:
                        history = []

            # Convert messages to serializable format
            messages_data = [
                {"role": msg.role.value, "content": msg.content} for msg in self.messages
            ]

            # Check if we already have a conversation for this model
            found = False
            for conversation in history:
                if conversation.get("model_id") == self.model_config.id:
                    # Update existing conversation
                    conversation["messages"] = messages_data
                    conversation["last_updated"] = datetime.now().isoformat()
                    found = True
                    break

            if not found:
                # Create a new conversation
                history.append(
                    {
                        "model_id": self.model_config.id,
                        "model_name": self.model_config.name,
                        "provider": self.model_config.provider.value,
                        "messages": messages_data,
                        "created": datetime.now().isoformat(),
                        "last_updated": datetime.now().isoformat(),
                    }
                )

            # Save history
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.history_file, "w") as f:
                json.dump(history, f, indent=2)

        except IOError:
            # If we can't save history, just continue
            self.console.print(
                "Warning: Could not save conversation history", style=STYLES["warning"]
            )

    def _display_messages(self) -> None:
        """Display all messages in the conversation."""
        # Skip the system message
        for message in self.messages:
            if message.role == Role.SYSTEM:
                continue

            # Always show history messages
            self._display_message(message)

    def _display_message(self, message: Message) -> None:
        """Display a single message.

        Args:
            message: The message to display
        """
        if message.role == Role.USER:
            style = STYLES["user_name"]
            title = "You"
        elif message.role == Role.ASSISTANT:
            style = STYLES["assistant_name"]
            title = f"{self.model_config.name}"
        else:
            style = STYLES["system_name"]
            title = "System"

        # Use different renderable types based on the message role
        content: RenderableType
        if message.role == Role.ASSISTANT:
            content = Markdown(message.content)
        else:
            content = Text.from_markup(message.content)

        self.console.print(Panel(content, title=title, title_align="left", border_style=style))

    async def run(self) -> AsyncGenerator[Panel, None]:
        """Run the chat interface.

        Yields:
            Panels showing the progress of assistant responses
        """
        # Display welcome message
        self.console.print(
            Panel.fit(
                f"Chat with {self.model_config.name}",
                style=STYLES["title"],
            )
        )

        # Inform if continuing a previous conversation
        if not self.new_conversation:
            self.console.print("Continuing previous conversation.", style=STYLES["info"])

        self.console.print("Type '/help' for commands, or '/exit' to quit.", style=STYLES["info"])
        self.console.print()

        # Display existing conversation if any
        if any(m.role != Role.SYSTEM for m in self.messages):
            self._display_messages()

        # Main chat loop
        try:
            while True:
                # Get user input - use console.input() which shows the prompt but not the entered text
                # then show it formatted in the panel
                self.console.print("[bold purple]>[/bold purple] ", end="")
                user_input = input()

                # Skip empty inputs
                if not user_input.strip():
                    continue

                # Print a newline for visual separation
                self.console.print()

                # Handle commands
                if user_input.startswith("/"):
                    command = user_input.lower().strip()

                    if command == "/exit" or command == "/quit":
                        # Save the chat to markdown
                        if any(m.role != Role.SYSTEM for m in self.messages):
                            saved_path = self._save_to_markdown()
                            self.console.print(
                                f"Chat saved to: {saved_path}", style=STYLES["success"]
                            )

                        self.console.print("Exiting chat.", style=STYLES["info"])
                        break

                    elif command == "/help":
                        self._show_help()
                        continue

                    elif command == "/clear":
                        # Clear the conversation (but keep the system message)
                        system_messages = [m for m in self.messages if m.role == Role.SYSTEM]
                        self.messages = system_messages
                        self.console.print("Conversation cleared.", style=STYLES["info"])
                        continue

                    elif command == "/system":
                        # Edit the system prompt
                        self.console.print("Enter new system prompt: ", end="")
                        new_prompt = input()
                        if new_prompt:
                            # Replace existing system messages
                            self.messages = [m for m in self.messages if m.role != Role.SYSTEM]
                            self.messages.insert(0, Message(role=Role.SYSTEM, content=new_prompt))
                            self.console.print("System prompt updated.", style=STYLES["success"])
                        continue

                    else:
                        self.console.print(f"Unknown command: {command}", style=STYLES["error"])
                        continue

                # Add user message to conversation
                user_message = Message(role=Role.USER, content=user_input)
                self.messages.append(user_message)

                # Skip displaying the user message panel since they already saw what they typed
                # Just add a small gap for visual separation
                self.console.print()

                # Get response from the model
                try:
                    # Create a spinner while waiting for the response
                    spinner = Spinner("dots", text=f"Thinking...")

                    # Placeholder for the assistant's message
                    assistant_message = Message(role=Role.ASSISTANT, content="")

                    first_chunk_received = False
                    panel = Panel(
                        Markdown(""),
                        title=f"{self.model_config.name}",
                        title_align="left",
                        border_style=STYLES["assistant_name"],
                    )

                    # Stream the response
                    with Live(spinner, refresh_per_second=10) as live:
                        response = await self.service.generate_response(self.messages, stream=True)

                        # Check if we got a streaming response or a complete one
                        if isinstance(response, str):
                            # We got a complete response
                            content_text = response
                            assistant_message.content = content_text
                            # Replace spinner with the model's response
                            style = STYLES["assistant_name"]
                            title = f"{self.model_config.name}"
                            panel = Panel(
                                Markdown(content_text),
                                title=title,
                                title_align="left",
                                border_style=style,
                            )
                            live.update(panel)
                            yield panel
                        else:
                            # We got a streaming response
                            content_text = ""
                            async for chunk in response:
                                content_text += chunk
                                assistant_message.content = content_text

                                # Update the live display with the current content
                                style = STYLES["assistant_name"]
                                title = f"{self.model_config.name}"

                                # Once we start receiving content, replace the spinner
                                if not first_chunk_received and content_text.strip():
                                    first_chunk_received = True

                                panel = Panel(
                                    Markdown(content_text),
                                    title=title,
                                    title_align="left",
                                    border_style=style,
                                )
                                live.update(panel)
                                yield panel

                    # Add the complete assistant message to conversation
                    self.messages.append(assistant_message)

                    # Save conversation history
                    self._save_history()

                except Exception as e:
                    self.console.print(f"Error: {e}", style=STYLES["error"])

        finally:
            # Clean up
            await self.service.close()

    def _show_help(self) -> None:
        """Display help information."""
        help_text = """
        # Commands
        
        - `/exit` or `/quit` - Exit the chat (saves conversation to markdown)
        - `/clear` - Clear the conversation history
        - `/system` - Update the system prompt
        - `/help` - Show this help message
        
        # Tips
        
        - Use `cliai chat --continue` or `cliai chat -c` to continue the previous conversation
        - Conversations are automatically saved as markdown files when you exit
        """

        self.console.print(Markdown(help_text))

    def _save_to_markdown(self) -> str:
        """Save the conversation to a markdown file.

        Returns:
            Path to the saved markdown file
        """
        # Create a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_name = self.model_config.name.replace(" ", "_")
        filename = f"{timestamp}_{model_name}_chat.md"

        # Content for the markdown file
        content = f"# Chat with {self.model_config.name}\n\n"
        content += f"*Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
        content += f"*Model: {self.model_config.name} ({self.model_config.provider.value})*\n\n"
        content += "---\n\n"

        # Add system message first
        system_msgs = [m for m in self.messages if m.role == Role.SYSTEM]
        if system_msgs:
            content += "### System Prompt\n\n"
            content += f"```\n{system_msgs[0].content}\n```\n\n"
            content += "---\n\n"

        # Add conversation messages (skip system messages)
        for message in self.messages:
            if message.role == Role.SYSTEM:
                continue
            elif message.role == Role.USER:
                content += f"### 🧑 You\n\n{message.content}\n\n"
            elif message.role == Role.ASSISTANT:
                content += f"### 🤖 {self.model_config.name}\n\n{message.content}\n\n"

            content += "---\n\n"

        # Save to current working directory
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        return os.path.abspath(filename)
