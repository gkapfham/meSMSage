"""Connect to a Google Sheet using gspread to access sheets at data frames."""

from dotenv import load_dotenv
from sheetfu import SpreadsheetApp

from decouple import config

SHEET = "Sheet1"


def create_keyfile_dictionary():
    """Return a dictionary that contains all of the correct environment variables."""
    variables_keys = {
        "type": config("SHEET_TYPE"),
        "project_id": config("SHEET_PROJECT_ID"),
        "private_key_id": config("SHEET_PRIVATE_KEY_ID"),
        "private_key": config("SHEET_PRIVATE_KEY"),
        "client_email": config("SHEET_CLIENT_EMAIL"),
        "client_id": config("SHEET_CLIENT_ID"),
        "auth_uri": config("SHEET_AUTH_URI"),
        "token_uri": config("SHEET_TOKEN_URI"),
        "auth_provider_x509_cert_url": config("SHEET_AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": config("SHEET_CLIENT_X509_CERT_URL")
    }
    return variables_keys


def connect_to_sheet(requested_spreadsheet_id: str, requested_sheet_name: str = SHEET):
    """Connect to the specified Google Sheet and return the requested sheet (default is "Sheet1")."""
    load_dotenv()
    sa = SpreadsheetApp(from_env=True)
    spreadsheet = sa.open_by_id(requested_spreadsheet_id)
    sheet = spreadsheet.get_sheet_by_name(requested_sheet_name)
    return sheet

    # sheet = spreadsheet.get_sheet_by_name('Sheet1')
    # data_range = sheet.get_data_range()
    # values = data_range.get_values()
    # print(type(values))

# # create a connection to the specified Google Sheet
#     google_client = gspread.service_account(CREDENTIALS)
#     # scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     # creds = ServiceAccountCredentials.from_json_keyfile_dict(create_keyfile_dictionary(), scope)
#     worksheet = google_client.open(requested_sheet).sheet1
#     return worksheet
