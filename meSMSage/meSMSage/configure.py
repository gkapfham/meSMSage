"""Configure logging and console output."""

import logging
import logging.config

from rich.logging import RichHandler
from rich.traceback import install

DEFAULT_LOGGING_LEVEL = "DEBUG"
FORMAT = "%(message)s"
RICH = "rich"

logger = None


def configure_tracebacks() -> None:
    """Configure stack tracebacks arising from a crash to use rich."""
    install()


def configure_logging(debug_level: str = DEFAULT_LOGGING_LEVEL) -> logging.Logger:
    """Configure standard Python logging package to use rich."""
    logging.basicConfig(
        level=debug_level, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )
    global logger
    if logger is None:
        logger = logging.getLogger(RICH)
    return logger
