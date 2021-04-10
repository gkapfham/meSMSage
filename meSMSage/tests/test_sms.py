"""Test the functions in the sms module."""

import os

import pytest

from twilio.rest import Client

from mesmsage import constants
from mesmsage import sms
from mesmsage import util


@pytest.mark.twilio
def test_send_single_message_real_twilio():
    """Ensure that a worksheet is returned for an existing sheet."""
    util.load_environment()
    client = Client()
    twilio_phone_number = os.getenv(constants.environment.Twilio_Phone_Number)
    recipient_phone_number = os.getenv(constants.environment.Recipient_Phone_Number)
    sid = sms.send_message(
        client,
        recipient_phone_number,
        twilio_phone_number,
        "Test: Sending Message Through Twilio",
    )
    assert sid is not None
