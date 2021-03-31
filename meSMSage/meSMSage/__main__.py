"""Define the command-line interface for the meSMSage program."""

import logging
import logging.config

from rich.logging import RichHandler
from rich.traceback import install

import pandas
import typer

import configure
import demonstrate
import sheets



def main(
    googlesheet_id: str = typer.Option(...),
    debug_level: str = typer.Option("DEBUG")
):
    """Access the command-line argument(s) and then perform actions."""
    # configure the use of rich for improved terminal output
    # --> rich-based tracebacks to enable better debugging on program crash
    configure.configure_tracebacks()
    # --> rich-based logging to improve display of all program console output
    logger = configure.configure_logging(debug_level)
    # display the debugging output for the program's command-line arguments
    logger.debug(f"The Google Sheet is {googlesheet_id}.")
    logger.debug(f"The debugging level is {debug_level}.")
    # connect the specified Google Sheet using the default internal sheet of "Sheet1"
    sheet = sheets.connect_to_sheet(googlesheet_id)
    data_range = sheet.get_data_range()
    values = data_range.get_values()
    logger.info(f"All values: {values}")
    sheetfu_volunteers_dataframe = pandas.DataFrame(values[1:len(values)], columns=values[0])
    print(sheetfu_volunteers_dataframe)
    demonstrate.demonstrate_pandas_analysis(sheetfu_volunteers_dataframe)


if __name__ == "__main__":
    typer.run(main)
