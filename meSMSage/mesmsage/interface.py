"""Provide a command-line interface."""

from textwrap import indent
from typing import List

from InquirerPy import get_style, inquirer

from mesmsage import constants


style = get_style(
    {
        "fuzzy_prompt": "#87afd7",
        "fuzzy_info": "#87afd7",
        "fuzzy_match": "#d78700",
        "input": "#767676",
        "marker": "#d78700",
        "pointer": "#afaf5f",
        "validator": "#d75f5f",
    },
    style_override=True,
)


def perform_fuzzy_selection(
    source: List, label: str = constants.sheets.Name_Prompt
) -> List:
    """Create a fuzzy selector for the given list with the provided label."""
    selection_list = inquirer.fuzzy(
        message="Select at least one " + label + ":",
        instruction="<<Fuzzy search, Tab selects, Enter confirms, Vim keybindings>>",
        choices=source,
        multiselect=True,
        validate=lambda result: len(result) > 0,
        transformer=lambda modify: "done!",
        invalid_message="Must select at least one " + label,
        max_height="70%",
        style=style,
        qmark="➔",
        border=False,
        info=False,
        vi_mode=True,
    ).execute(raise_keyboard_interrupt=False)
    return selection_list


def reindent(text: str, num_spaces: int = 4) -> str:
    """Add indentation spaces to a (potentially) multiline string."""
    return indent(text, constants.markers.Space * num_spaces)
