"""Test cases for the util module."""

import os

from mesmsage import util


def test_dotenv_creates_environment():
    """Ensure that the use of dotenv creates expected environment variables."""
    util.load_environment()
    key = "SHEETFU_CONFIG_TYPE"
    value = os.getenv(key)
    assert value == "service_account"


def test_reindent_short_string():
    """Ensure that a short re-indented string exists after function call."""
    message = "hello"
    reindented_message = util.reindent(message)
    assert reindented_message is not None
    assert reindented_message == "    hello"


def test_reindent_two_word_string():
    """Ensure that a short two-word re-indented string exists after function call."""
    message = "hello world"
    reindented_message = util.reindent(message)
    assert reindented_message is not None
    assert reindented_message == "    hello world"


def test_create_printable_dictionary_single_key():
    """Ensure that the creation of a printable dictionary works correctly."""
    dictionary = {"Gregory": ["Task One", "Task Two"]}
    printable_dictionary = util.get_printable_dictionary_list(dictionary)
    assert printable_dictionary is not None
    assert "Gregory" in printable_dictionary
    assert "Task One" in printable_dictionary
    assert "Task Two" in printable_dictionary
