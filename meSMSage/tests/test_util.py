"""Test cases for the util module."""

import os

from mesmsage import util


def test_dotenv_creates_environment():
    """Ensure that the use of dotenv creates expected environment variables."""
    util.load_environment()
    key = "SHEETFU_CONFIG_TYPE"
    value = os.getenv(key)
    assert value == "service_account"
