"""Define the command-line interface for the meSMSage program."""

import os

from enum import Enum
from pathlib import Path


from mesmsage import configure
from mesmsage import constants
from mesmsage import demonstrate
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
    debug_level: DebugLevel = DebugLevel.DEBUG,
    env_file: Path = typer.Option(None),
):
    """Send SMS messages."""
    # configure the use of rich for improved terminal output
    # --> rich-based tracebacks to enable better debugging on program crash
    configure.configure_tracebacks()
    # --> rich-based logging to improve display of all program console output
    logger = configure.configure_logging(debug_level.value)
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
        env_file_name = constants.markers.Nothing.join([os.getcwd(), os.sep, ".env"])
        # DEBUG: indicate the use of the .env file in the current working directory
        logger.debug("Using constructed .env file in current directory")
    # DEBUG: display the constructed name of the .env file
    logger.debug(f"Environment file: {env_file_name}")
    # load the required secure environment for connecting to Google Sheets
    util.load_environment(env_file_name)
    # connect the specified Google Sheet using the default internal sheet of "Sheet1"
    sheet = sheets.connect_to_sheet(googlesheet_id)
    # extract the Pandas data frame from the sheet in sheetfu's internal format
    dataframe = sheets.extract_dataframe(sheet)
    # demonstrate the use of the dataframe with an example
    demonstrate.demonstrate_pandas_analysis(dataframe)
