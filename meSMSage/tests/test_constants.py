"""Tests for the constants module."""

import pytest

from mesmsage import constants

CANNOT_SET_CONSTANT_VARIABLE = "cannot_set_constant_variable"


def test_dataframes_constant_defined():
    """Check correctness for the variables in the dataframes constant."""
    assert constants.dataframes.Index == "index"
    assert constants.dataframes.List == "list"


def test_dataframes_constant_cannot_redefine():
    """Check cannot redefine the variables in the environment constant."""
    with pytest.raises(AttributeError):
        constants.dataframes.Index = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.dataframes.List = CANNOT_SET_CONSTANT_VARIABLE


def test_environment_constant_defined():
    """Check correctness for the variables in the environment constant."""
    assert constants.environment.Recipient_Phone_Number == "RECIPIENT_PHONE_NUMBER"
    assert constants.environment.Twilio_Phone_Number == "TWILIO_PHONE_NUMBER"


def test_environment_constant_cannot_redefine():
    """Check cannot redefine the variables in the environment constant."""
    with pytest.raises(AttributeError):
        constants.environment.Recipient_Phone_Number = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.environment.Twilio_Phone_Number = CANNOT_SET_CONSTANT_VARIABLE


def test_files_constant_defined():
    """Check correctness for the variables in the files constant."""
    assert constants.files.Env == ".env"


def test_files_constant_cannot_redefine():
    """Check cannot redefine the variables in the files constant."""
    with pytest.raises(AttributeError):
        constants.files.Env = CANNOT_SET_CONSTANT_VARIABLE


def test_locations_constant_defined():
    """Check correctness for the variables in the locations constant."""
    assert constants.locations.Us == "US"


def test_locations_constant_cannot_redefine():
    """Check cannot redefine the variables in the locations constant."""
    with pytest.raises(AttributeError):
        constants.locations.Us = CANNOT_SET_CONSTANT_VARIABLE


def test_logging_constant_defined():
    """Check correctness for the variables in the logging constant."""
    assert constants.logging.Debug == "DEBUG"
    assert constants.logging.Info == "INFO"
    assert constants.logging.Warning == "WARNING"
    assert constants.logging.Error == "ERROR"
    assert constants.logging.Critical == "CRITICAL"
    assert constants.logging.Default_Logging_Level == "ERROR"
    assert constants.logging.Format == "%(message)s"
    assert constants.logging.Rich == "Rich"


def test_logging_constant_cannot_redefine():
    """Check cannot redefine the variables in the logging constant."""
    with pytest.raises(AttributeError):
        constants.logging.Debug = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.logging.Info = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.logging.Warning = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.logging.Error = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.logging.Critical = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.logging.Critical = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.logging.Default_Logging_Level = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.logging.Format = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.logging.Rich = CANNOT_SET_CONSTANT_VARIABLE


def test_markers_constant_defined():
    """Check correctness for the variables in the markers constant."""
    assert constants.markers.All_Individuals == "All Individuals"
    assert constants.markers.Empty == b""
    assert constants.markers.Indent == "  "
    assert constants.markers.In_A_File == "in a file"
    assert constants.markers.Newline == "\n"
    assert constants.markers.Nothing == ""
    assert constants.markers.Space == " "


def test_markers_constant_cannot_redefine():
    """Check cannot redefine the variables in the markers constant."""
    with pytest.raises(AttributeError):
        constants.markers.All_Individuals = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.markers.Empty = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.markers.Indent = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.markers.In_A_File = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.markers.Newline = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.markers.Nothing = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.markers.Space = CANNOT_SET_CONSTANT_VARIABLE


def test_progress_constant_defined():
    """Check correctness for the variables in the dataframes constant."""
    assert constants.progress.Small_Step == 0.2
    assert constants.progress.Medium_Step == 0.4
    assert constants.progress.Large_Step == 0.6


def test_progress_constant_cannot_redefine():
    """Check cannot redefine the variables in the environment constant."""
    with pytest.raises(AttributeError):
        constants.progress.Small_Step = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.progress.Medium_Step = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.progress.Large_Step = CANNOT_SET_CONSTANT_VARIABLE


def test_sizes_constant_defined():
    """Check correctness for the variables in the dataframes constant."""
    assert constants.sizes.First == 0
    assert constants.sizes.Singleton == 1
    assert constants.sizes.Tab == 4


def test_sizes_constant_cannot_redefine():
    """Check cannot redefine the variables in the environment constant."""
    with pytest.raises(AttributeError):
        constants.progress.First = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.progress.Singleton = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.progress.Tab = CANNOT_SET_CONSTANT_VARIABLE


def test_sheets_constant_defined():
    """Check correctness for the variables in the dataframes constant."""
    assert constants.sheets.Default == "Sheet1"
    assert constants.sheets.Name == "Individual Name"
    assert constants.sheets.Name_Prompt == "individual's name"
    assert constants.sheets.Number == "Individual Phone Number"


def test_sheets_constant_cannot_redefine():
    """Check cannot redefine the variables in the environment constant."""
    with pytest.raises(AttributeError):
        constants.sheetes.Default = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.sheets.Name = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.sheets.Name_Prompt = CANNOT_SET_CONSTANT_VARIABLE
    with pytest.raises(AttributeError):
        constants.sheets.Number = CANNOT_SET_CONSTANT_VARIABLE
