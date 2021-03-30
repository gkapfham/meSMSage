"""Test the functions in the sheet module."""

from meSMSage import sheet

from gspread import exceptions

import pytest


def test_connect_to_existing_sheet():
    """Ensure that a worksheet is returned for an existing sheet."""
    googlesheet_exists = "meSMSage-volunteer-contact-schedule-sheet"
    worksheet = sheet.connect(googlesheet_exists)
    assert worksheet is not None


def test_connect_to_not_existing_sheet():
    """Ensure that a worksheet is not returned for a not existing sheet."""
    with pytest.raises(exceptions.SpreadsheetNotFound):
        googlesheet_exists = "meSMSage-volunteer-contact-schedule-sheet-NONE"
        worksheet = sheet.connect(googlesheet_exists)
        assert worksheet is None
