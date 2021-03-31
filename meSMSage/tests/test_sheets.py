"""Test the functions in the sheets module."""

from sheetfu import model

from googleapiclient import errors

from meSMSage import sheets

import pytest


def test_connect_to_existing_sheet():
    """Ensure that a worksheet is returned for an existing sheet."""
    googlesheet_id_exists = "1ujmuIJy1NPhasIF4tnRSae0033hwa9g0wul5Ii2NwZU"
    sheet = sheets.connect_to_sheet(googlesheet_id_exists)
    assert sheet is not None
    assert type(sheet) is model.Sheet


def test_connect_to_not_existing_sheet():
    """Ensure that a worksheet is not returned for a not existing sheet."""
    with pytest.raises(errors.HttpError):
        googlesheet_id_exists = "1ujmuIJy1NPhasIF4tnRSae0033hwa9g0wul5Ii2NwZU-WRONG"
        sheet = sheets.connect_to_sheet(googlesheet_id_exists)
        assert sheet is not None
        assert type(sheet) is model.Sheet
