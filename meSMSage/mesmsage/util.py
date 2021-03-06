"""Utility functions for manipulating the environment and textual content."""

from textwrap import indent
from textwrap import wrap
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


def get_printable_dictionary_list(provided_dict: Dict[str, List[str]]) -> str:
    """Create a textual representation of a dictionary where the value is a list."""
    lines = []
    # iterate through the names and activities in provided_dict
    # and create a list of lines for each key-value pair in provided_dict
    for key, value_list in provided_dict.items():
        lines.append(key + " -> " + ", ".join(value_list))
    # create a multiple-line string that contains all of the individual
    # listings of a person's name and their chosen activities. Then,
    # re-indent this multiple-line string so that it is tabbed in
    return reindent("\n".join(lines), constants.sizes.Tab)


def get_printable_dictionary_str(provided_dict: Dict[str, str]) -> str:
    """Create a textual representation of a dictionary."""
    lines = []
    # iterate through the names and activities in provided_dict
    # and create a list of lines for each key-value pair in provided_dict
    for key, value_str in provided_dict.items():
        lines.append(key + " -> " + "\n".join(wrap(value_str, width=50)))
    # create a multiple-line string that contains all of the individual
    # listings of a person's name and their chosen activities. Then,
    # re-indent this multiple-line string so that it is tabbed in
    return reindent("\n".join(lines), constants.sizes.Tab)


def get_spiffy_list(contents: List[str]) -> str:
    """Create a list that expands the contents in the string to a complete sentence."""
    # join all items except the last one with a comma between them
    if len(contents) > 1:
        out = ", ".join(contents[:-1])
        # add the last element, separated by the word "and"
        return "{}, and {}".format(out, contents[-1])
    elif len(contents) == 1:
        return " ".join(contents)
    else:
        return ""


def reindent(text: str, num_spaces: int = 4) -> str:
    """Add indentation spaces to a (potentially) multiline string."""
    return indent(text, constants.markers.Space * num_spaces)
