"""Entry point for CLI AI Chat."""

import sys

if __name__ == "__main__":
    from .main import app

    sys.exit(app())
