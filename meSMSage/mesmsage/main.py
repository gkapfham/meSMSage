"""Define the command-line interface for the meSMSage program."""

import os

from enum import Enum
from pathlib import Path

from rich.console import Console
from rich.progress import Progress
from rich.text import Text


from mesmsage import configure
from mesmsage import constants
from mesmsage import demonstrate
from mesmsage import extract
from mesmsage import interface
from mesmsage import sheets
from mesmsage import util

import typer

app = typer.Typer()


class DebugLevel(str, Enum):
    """The predefined levels for debugging."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@app.command()
def history():
    """Show SMS message history."""
    typer.echo("History of SMS sending")


@app.command()
def send(
    googlesheet_id: str = typer.Option(...),
    debug_level: DebugLevel = DebugLevel.ERROR,
    env_file: Path = typer.Option(None),
):
    """Send SMS messages."""
    # configure the use of rich for improved terminal output
    # --> rich-based tracebacks to enable better debugging on program crash
    configure.configure_tracebacks()
    # --> rich-based logging to improve display of all program console output
    logger = configure.configure_logging(debug_level.value)
    # create a console used to display messages in terminal window
    console = Console()
    console.print()
    with Progress(transient=True) as progress:
        access_dataframe_task = progress.add_task("Downloading Google Sheet", total=0.5)
        # DEBUG: display the debugging output for the program's command-line arguments
        logger.debug(f"The Google Sheet is {googlesheet_id}.")
        logger.debug(f"The debugging level is {debug_level.value}.")
        # construct the full name of the .env file
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
                [os.getcwd(), os.sep, ".env"]
            )
            # DEBUG: indicate the use of the .env file in the current working directory
            logger.debug("Using constructed .env file in current directory")
        # DEBUG: display the constructed name of the .env file
        logger.debug(f"Environment file: {env_file_name}")
        # load the required secure environment for connecting to Google Sheets
        util.load_environment(env_file_name)
        progress.update(access_dataframe_task, advance=0.4)
        # connect the specified Google Sheet using the default internal sheet of "Sheet1"
        sheet = sheets.connect_to_sheet(googlesheet_id)
        progress.update(access_dataframe_task, advance=0.4)
        # extract the Pandas data frame from the sheet in sheetfu's internal format
        dataframe = sheets.extract_dataframe(sheet)
        progress.update(access_dataframe_task, advance=0.2)
        console.print()
    # extract all of the individual names from the dataframe
    individual_names_series = extract.get_individual_names(dataframe)
    individual_names_list = extract.convert_series_to_list(individual_names_series)
    console.print()
    chosen_individual_names = interface.perform_fuzzy_selection(individual_names_list)
    chosen_individual_names_str = interface.reindent("\n".join(chosen_individual_names), 4)
    chosen_individual_names_text = Text(chosen_individual_names_str)
    console.print()
    console.print("Sending SMS messages to:")
    console.print()
    console.print(chosen_individual_names_text)
    console.print()
    # EXTRA:demonstrate the use of the dataframe with an example
    demonstrate.demonstrate_pandas_analysis(dataframe)
