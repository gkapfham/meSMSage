"""Provide a command-line interface."""

import logging

from typing import List

from InquirerPy import get_style, inquirer  # type: ignore

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
        info=True,
        vi_mode=True,
    ).execute(raise_keyboard_interrupt=False)
    return selection_list


def create_individuals_list(
    chosen_individuals_list: List[str], total_individuals_list: List[str]
) -> List[str]:
    """Check to see if the list of current individuals contains a request for all individuals."""
    # DEBUG: display details about the individuals chosen and passed as input
    logger = logging.getLogger(constants.logging.Rich)
    logger.debug(f"Chosen individuals: {chosen_individuals_list}")
    logger.debug(f"Total individuals: {total_individuals_list}")
    # if "All Individuals" was chosen as at least one of the inputs
    # then this function must return all possible individuals
    if constants.markers.All_Individuals in chosen_individuals_list:
        logger.debug("All individuals was chosen")
        # extract the marker of "All Individuals" from the total list
        # of every person evident in the spreadsheet of individuals
        total_individuals_list.remove(constants.markers.All_Individuals)
        return total_individuals_list
    return chosen_individuals_list
