"""Connect to a Google Sheet using gspread to access sheets at data frames."""

import gspread

CREDENTIALS = "credentials.json"


def connect(requested_sheet: str) -> gspread.Worksheet:
    """Connect to the specified Google Sheet and return a worksheet."""
    # create a connection to the specified Google Sheet
    google_client = gspread.service_account(CREDENTIALS)
    worksheet = google_client.open(requested_sheet).sheet1
    return worksheet
