"""Connect to a Google Sheet using gspread to access sheets at data frames."""

import pandas

from dotenv import load_dotenv
from sheetfu import model
from sheetfu import SpreadsheetApp

from mesmsage import configure

SHEET = "Sheet1"


def connect_to_sheet(
    requested_spreadsheet_id: str, env_file_name: str, requested_sheet_name: str = SHEET
) -> model.Sheet:
    """Connect to the specified Google Sheet and return the requested sheet (default is "Sheet1")."""
    # extract a logger
    logger = configure.configure_logging()
    # load the environment variables, either from a .env file if it is available
    load_dotenv(dotenv_path=env_file_name)
    # use sheetfu to load the spreadsheet with configuration in environment variables
    sa = SpreadsheetApp(from_env=True)
    # get the spreadsheet by its identifier and then extract the specific
    # worksheet from it, with Google Sheets making the default worksheet "Sheet1"
    spreadsheet = sa.open_by_id(requested_spreadsheet_id)
    sheet = spreadsheet.get_sheet_by_name(requested_sheet_name)
    logger.debug(sheet)
    logger.debug(type(sheet))
    return sheet


def extract_dataframe(sheet: model.Sheet) -> pandas.DataFrame:
    """Extract a Pandas DataFrame from the sheet in sheetfu's internal format."""
    data_range = sheet.get_data_range()
    values = data_range.get_values()
    extracted_dataframe = pandas.DataFrame(values[1 : len(values)], columns=values[0])
    return extracted_dataframe