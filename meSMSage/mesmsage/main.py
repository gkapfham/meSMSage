"""Define the command-line interface for the meSMSage program."""

from enum import Enum
from pathlib import Path


from mesmsage import configure
from mesmsage import demonstrate
from mesmsage import sheets

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
    env_file: Path = typer.Option(...),
    debug_level: DebugLevel = DebugLevel.DEBUG,
):
    """Send SMS messages."""
    # configure the use of rich for improved terminal output
    # --> rich-based tracebacks to enable better debugging on program crash
    configure.configure_tracebacks()
    # --> rich-based logging to improve display of all program console output
    logger = configure.configure_logging(debug_level.value)
    # display the debugging output for the program's command-line arguments
    logger.debug(f"The Google Sheet is {googlesheet_id}.")
    logger.debug(f"The debugging level is {debug_level.value}.")
    # construct the full name of the .env file
    if env_file is None:
        typer.echo("No data file specified!")
        raise typer.Abort()
    # the file was specified and it is valid so derive its full name
    if env_file.is_file():
        env_file_name = env_file.parent.name + env_file.anchor + env_file.name
    # connect the specified Google Sheet using the default internal sheet of "Sheet1"
    sheet = sheets.connect_to_sheet(googlesheet_id, env_file_name)
    # extract the Pandas data frame from the sheet in sheetfu's internal format
    dataframe = sheets.extract_dataframe(sheet)
    # demonstrate the use of the dataframe with an example
    demonstrate.demonstrate_pandas_analysis(dataframe)
