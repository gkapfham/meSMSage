"""Configure logging and console output."""

import logging
import logging.config

from rich.logging import RichHandler
from rich.traceback import install

from mesmsage import constants

logger = None


def configure_tracebacks() -> None:
    """Configure stack tracebacks arising from a crash to use rich."""
    install()


def configure_logging(
    debug_level: str = constants.logging.Default_Logging_Level, force: bool = False
) -> logging.Logger:
    """Configure standard Python logging package to use rich."""
    logging.basicConfig(
        level=debug_level,
        format=constants.logging.Format,
        datefmt="[%X]",
        handlers=[RichHandler()],
    )
    # if the global logger has not yet been set, set it to the configured logger
    global logger
    if logger is None or force is True:
        logger = logging.getLogger(constants.logging.Rich)
    return logger
