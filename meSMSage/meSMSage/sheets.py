"""Connect to a Google Sheet using gspread to access sheets at data frames."""

import os

from dotenv import load_dotenv
from sheetfu import model
from sheetfu import SpreadsheetApp

import configure


SHEET = "Sheet1"


def connect_to_sheet(requested_spreadsheet_id: str, requested_sheet_name: str = SHEET) -> model.Sheet:
    """Connect to the specified Google Sheet and return the requested sheet (default is "Sheet1")."""
    logger = configure.configure_logging()
    load_dotenv()
    logger.debug(f"Environment: {os.getenv('SHEETFU_CONFIG_TYPE')}")
    sa = SpreadsheetApp(from_env=True)
    spreadsheet = sa.open_by_id(requested_spreadsheet_id)
    sheet = spreadsheet.get_sheet_by_name(requested_sheet_name)
    print(type(sheet))
    return sheet
