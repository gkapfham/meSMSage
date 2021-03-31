"""Define the command-line interface for the meSMSage program."""

from enum import Enum

import pandas
import typer

import configure
import demonstrate
import sheets


class DebugLevel(str, Enum):
    """The predefined levels for debugging."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


def main(
    googlesheet_id: str = typer.Option(...), debug_level: DebugLevel = DebugLevel.DEBUG
):
    """Access the command-line argument(s) and then perform actions."""
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
    # data_range = sheet.get_data_range()
    # values = data_range.get_values()
    # logger.info(f"All values: {values}")
    # sheetfu_volunteers_dataframe = pandas.DataFrame(
    #     values[1 : len(values)], columns=values[0]
    # )
    # print(sheetfu_volunteers_dataframe)
    demonstrate.demonstrate_pandas_analysis(dataframe)


if __name__ == "__main__":
    typer.run(main)
