"""Utility functions for manipulating the environment and textual content."""

from textwrap import indent
from typing import Dict
from typing import List

from dotenv import load_dotenv

from mesmsage import constants


def load_environment(env_file_name: str = None) -> None:
    """Load the environment using the specified .env file name."""
    # load the environment variables
    # --> no file is specified, so load from environment variables
    if env_file_name is None:
        load_dotenv()
    # --> file is specified, so load from it instead of environment variables
    else:
        load_dotenv(dotenv_path=env_file_name)


def get_printable_dictionary(provided_dict: Dict[str, List[str]]) -> str:
    """Create a textual representation of a dictionary."""
    lines = []
    # iterate through the names and activities in provided_dict
    # and create a list of lines for each key-value pair in provided_dict
    for name, activities in provided_dict.items():
        lines.append(name + " -> " + ", ".join(activities))
    # create a multiple-line string that contains all of the individual
    # listings of a person's name and their chosen activities. Then,
    # re-indent this multiple-line string so that it is tabbed in
    return reindent("\n".join(lines), constants.sizes.Tab)


def reindent(text: str, num_spaces: int = 4) -> str:
    """Add indentation spaces to a (potentially) multiline string."""
    return indent(text, constants.markers.Space * num_spaces)
