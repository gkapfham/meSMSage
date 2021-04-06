"""Test the functions in the sheets module."""

from googleapiclient import errors
from sheetfu import model
from sheetfu.exceptions import SheetNameNoMatchError

from mesmsage import sheets
from mesmsage import util
from mesmsage.sheets import SheetNotFoundError

import pytest


def test_connect_to_existing_googlesheet():
    """Ensure that a worksheet is returned for an existing sheet."""
    util.load_environment()
    googlesheet_id_exists = "1ujmuIJy1NPhasIF4tnRSae0033hwa9g0wul5Ii2NwZU"
    sheet = sheets.connect_to_sheet(googlesheet_id_exists)
    assert sheet is not None
    assert type(sheet) is model.Sheet


def test_connect_to_not_existing_googlesheet():
    """Ensure that a worksheet is not returned for a not-existing Google sheet."""
    with pytest.raises(errors.HttpError):
        util.load_environment()
        googlesheet_id_exists = "1ujmuIJy1NPhasIF4tnRSae0033hwa9g0wul5Ii2NwZU-WRONG"
        _ = sheets.connect_to_sheet(googlesheet_id_exists)


def test_connect_to_not_existing_worksheet_in_valid_googlesheet():
    """Ensure that a sheet is not returned for a not-existing worksheet in a valid Google sheet."""
    with pytest.raises(SheetNameNoMatchError):
        util.load_environment()
        googlesheet_id_exists = "1ujmuIJy1NPhasIF4tnRSae0033hwa9g0wul5Ii2NwZU"
        _ = sheets.connect_to_sheet(
            googlesheet_id_exists, requested_sheet_name="SheetNotThere"
        )


def test_extract_dataframe_from_existing_googlesheet_and_existing_worksheet():
    """Ensure that it is possible to extract a Pandas dataframe from a Sheetfu sheet."""
    util.load_environment()
    googlesheet_id_exists = "1ujmuIJy1NPhasIF4tnRSae0033hwa9g0wul5Ii2NwZU"
    sheet = sheets.connect_to_sheet(googlesheet_id_exists)
    dataframe = sheets.extract_dataframe(sheet)
    assert dataframe is not None
    assert dataframe.ndim == 2
    assert dataframe.size == 640


def test_extract_dataframe_from_not_existing_sheet():
    """Ensure that trying to extract a Pandas dataframe from non-existent Sheetfu sheet does not work."""
    with pytest.raises(SheetNotFoundError):
        util.load_environment()
        _ = sheets.extract_dataframe(None)
