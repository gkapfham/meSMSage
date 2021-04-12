"""Define the command-line interface for the meSMSage program."""

import logging
import os
import signal
import sys

from enum import Enum
from logging import Logger
from pathlib import Path
from typing import Dict
from typing import List
from typing import Tuple

from rich.console import Console
from rich.text import Text

from pandas import DataFrame

from mesmsage import configure
from mesmsage import constants
from mesmsage import demonstrate
from mesmsage import extract
from mesmsage import interface
from mesmsage import sheets
from mesmsage import sms
from mesmsage import util
from mesmsage import webhook

import typer

cli = typer.Typer()


class DebugLevel(str, Enum):
    """The predefined levels for debugging."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


def setup(debug_level: DebugLevel) -> Tuple[Console, Logger]:
    """Perform the setup steps and return a Console for terminal-based display."""
    # configure the use of rich for improved terminal output:
    # --> rich-based tracebacks to enable better debugging on program crash
    configure.configure_tracebacks()
    # --> rich-based logging to improve display of all program console output
    logger = configure.configure_logging(debug_level.value)
    # --> rich-based console to display messages and features in terminal window
    console = Console()
    return console, logger


def load_environment(env_file: Path, logger: Logger) -> None:
    """Load the environment using the dotenv package."""
    env_file_name = constants.markers.Nothing
    # the file was specified and it is valid so derive its full name
    if env_file is not None:
        if env_file.is_file():
            # DEBUG: indicate that the .env file on command-line is in use
            logger.debug("Using provided .env file from the command-line")
            # convert the Pathlib Path to a string
            env_file_name = str(env_file)
    # the file name was not specified so construct the default name
    else:
        env_file_name = constants.markers.Nothing.join(
            [os.getcwd(), os.sep, constants.files.Env]
        )
        # DEBUG: indicate the use of the .env file in the current working directory
        logger.debug("Using constructed .env file in current directory")
    # DEBUG: display the constructed name of the .env file
    logger.debug(f"Environment file: {env_file_name}")
    # load the required secure environment for connecting to Google Sheets
    util.load_environment(env_file_name)


def download(googlesheet_id: str, env_file: Path, debug_level: DebugLevel) -> DataFrame:
    """Download the spreadsheet from Google Sheets, process it, and return an Pandas data frame."""
    logger = logging.getLogger(constants.logging.Rich)
    # DEBUG: display the debugging output for the program's command-line arguments
    logger.debug(f"The Google Sheet is {googlesheet_id}.")
    logger.debug(f"The debugging level is {debug_level.value}.")
    # construct the full name of the .env file
    load_environment(env_file, logger)
    # connect the specified Google Sheet using the default internal sheet of "Sheet1"
    sheet = sheets.connect_to_sheet(googlesheet_id)
    # extract the Pandas data frame from the sheet in sheetfu's internal format
    dataframe = sheets.extract_dataframe(sheet)
    # console.print(constants.markers.Indent + "Downloading")
    return dataframe


def select_individuals(dataframe: DataFrame) -> List[str]:
    """Interactively select the individuals who will receive the SMS messages."""
    # extract all of the individual names from the dataframe
    individual_names_series = extract.get_individual_names(dataframe)
    individual_names_list = extract.convert_series_to_list(individual_names_series)
    # prepend the "All Individuals" option to the list of choices for
    # the user so that a person does not have to select every person
    # in order to send the SMS to all people in the spreadsheet
    individual_names_list.insert(
        constants.sizes.First, constants.markers.All_Individuals
    )
    # allow the user to perform the fuzzy selection of individuals
    chosen_individual_names_list = interface.perform_fuzzy_selection(
        individual_names_list
    )
    # if "All Individuals" was selected, then make sure to return every
    # individual in the spreadsheet instead of returning the label
    # "All Individuals", which is only a convenience marker for users
    # Note that create_individuals_list assumes that the marker
    # "All Individuals" is always going to be individual_names_list
    return interface.create_individuals_list(
        chosen_individual_names_list, individual_names_list
    )


def display_recipients(
    chosen_individual_names_list: List[str], console: Console
) -> None:
    """Display the names of people who will receive the SMS message."""
    chosen_individual_names_str = util.reindent(
        "\n".join(chosen_individual_names_list), constants.sizes.Tab
    )
    chosen_individual_names_text = Text(chosen_individual_names_str)
    console.print()
    console.print("Sending SMS messages to:")
    console.print()
    console.print(chosen_individual_names_text)
    console.print()


def display_activities(
    individual_activities_dict: Dict[str, List[str]], console: Console
) -> None:
    """Display the names of individuals and their associated activities."""
    console.print("Sending reminders for these activities:")
    console.print()
    activities_text = util.get_printable_dictionary_list(individual_activities_dict)
    console.print(activities_text)
    console.print()


def display_sms(
    number_sms_dict: Dict[str, str], console: Console, dry_run: bool = False
) -> None:
    """Display the names of individuals and their associated activities."""
    if not dry_run:
        console.print("Preparing to send these SMS:")
    else:
        console.print("Would send send these SMS:")
    console.print()
    sms_text = util.get_printable_dictionary_str(number_sms_dict)
    console.print(sms_text)
    console.print()


def connect_and_download(
    googlesheet_id: str, debug_level: DebugLevel, env_file: Path
) -> Tuple[DataFrame, Console, Logger]:
    """Connect to the spreadsheet and then download it and return it."""
    # STEP: setup the console and the logger and then create a blank line for space
    console, logger = setup(debug_level)
    console.print()
    # STEP: download the spreadsheet and produce a Pandas data frame
    dataframe = download(googlesheet_id, env_file, debug_level)
    return dataframe, console, logger


@cli.command()
def send(
    googlesheet_id: str = typer.Option(...),
    debug_level: DebugLevel = DebugLevel.ERROR,
    env_file: Path = typer.Option(None),
    dry_run: bool = typer.Option(False),
):
    """Send SMS messages."""
    # STEP: connect to the spreadsheet, download it, and use it in follow-on steps
    dataframe, console, logger = connect_and_download(
        googlesheet_id, debug_level, env_file
    )
    # STEP: let the person using the program select individuals to receive the SMS
    chosen_individual_names_list = select_individuals(dataframe)
    # STEP: display the names of individuals who will receive the SMS
    display_recipients(chosen_individual_names_list, console)
    # STEP: get the phone numbers of the selected individuals
    phone_numbers_dictionary = extract.get_individual_numbers(
        dataframe, chosen_individual_names_list
    )
    logger.debug(f"Phone numbers: {phone_numbers_dictionary}")
    # STEP: get the activities for individuals
    name_activities_dictionary = extract.get_individual_activities(
        dataframe, chosen_individual_names_list
    )
    logger.debug(f"Individuals and activities: {name_activities_dictionary}")
    display_activities(name_activities_dictionary, console)
    # STEP: generate the messages for the individuals
    number_sms_dictionary = extract.get_sms_messages(
        phone_numbers_dictionary, name_activities_dictionary
    )
    logger.debug(f"Phone numbers and SMS messages: {number_sms_dictionary}")
    display_sms(number_sms_dictionary, console, dry_run)
    # STEP: send the SMS messages for each individual
    if not dry_run:
        sid = sms.send_messages(number_sms_dictionary)
        logger.debug(f"Twilio returned SID: {sid}")


@cli.command()
def demo(
    googlesheet_id: str = typer.Option(...),
    debug_level: DebugLevel = DebugLevel.ERROR,
    env_file: Path = typer.Option(None),
):
    """Demonstrate features."""
    # STEP: connect to the spreadsheet, download it, and use it for a demonstration
    dataframe, console, logger = connect_and_download(
        googlesheet_id, debug_level, env_file
    )
    # EXTRA: demonstrate the use of the dataframe with an example
    demonstrate.demonstrate_pandas_analysis(dataframe)


@cli.command()
def receive(
    googlesheet_id: str = typer.Option(...),
    debug_level: DebugLevel = DebugLevel.ERROR,
    env_file: Path = typer.Option(None),
):
    """Receive SMS messages using a webhook."""
    # setup the console and the logger instance
    console, logger = setup(debug_level)
    console.print()
    # load the environment from the specified .env file
    # (or from the default file if one was not specified)
    load_environment(env_file, logger)
    logger.debug("Calling the main function for the webhook")
    # start the ngrok and WSGI servers using the webhook module
    webhook.main(googlesheet_id, logger, console)


@cli.command()
def history():
    """Show SMS message history."""
    typer.echo("History of SMS sending")
