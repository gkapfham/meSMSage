"""Tests for the constants module."""

import pytest

from mesmsage import constants

CANNOT_SET_CONSTANT_VARIABLE = "cannot_set_constant_variable"


def test_environment_constant_defined():
    """Check correctness for the variables in the environment constant."""
    assert constants.environment.Twilio_Phone_Number == "TWILIO_PHONE_NUMBER"


def test_environment_constant_cannot_redefine():
    """Check cannot redefine the variables in the environment constant."""
    with pytest.raises(AttributeError):
        constants.environment.Twilio_Phone_Number = CANNOT_SET_CONSTANT_VARIABLE


def test_files_constant_defined():
    """Check correctness for the variables in the environment constant."""
    assert constants.files.Env == ".env"


def test_files_constant_cannot_redefine():
    """Check cannot redefine the variables in the environment constant."""
    with pytest.raises(AttributeError):
        constants.files.Env = CANNOT_SET_CONSTANT_VARIABLE


def test_locations_constant_defined():
    """Check correctness for the variables in the environment constant."""
    assert constants.locations.Us == "US"


def test_locations_constant_cannot_redefine():
    """Check cannot redefine the variables in the environment constant."""
    with pytest.raises(AttributeError):
        constants.locations.Us = CANNOT_SET_CONSTANT_VARIABLE
