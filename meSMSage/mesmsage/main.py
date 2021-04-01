"""Define the command-line interface for the meSMSage program."""

import typer


app = typer.Typer()


from enum import Enum


from mesmsage import configure
from mesmsage import demonstrate
from mesmsage import sheets


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
    googlesheet_id: str = typer.Option(...), debug_level: DebugLevel = DebugLevel.DEBUG
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
    # connect the specified Google Sheet using the default internal sheet of "Sheet1"
    sheet = sheets.connect_to_sheet(googlesheet_id)
    # extract the Pandas data frame from the sheet in sheetfu's internal format
    dataframe = sheets.extract_dataframe(sheet)
    # demonstrate the use of the dataframe with an example
    demonstrate.demonstrate_pandas_analysis(dataframe)
