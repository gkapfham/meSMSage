"""Test the functions in the sms module."""

import os

import pytest

from unittest import mock

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from mesmsage import constants
from mesmsage import sms
from mesmsage.sms import client
from mesmsage import util


@pytest.mark.twilio
def test_send_single_message_real_twilio_constructed_client():
    """Ensure that it is possible to send the SMS message through Twilio service."""
    util.load_environment()
    internal_client = Client()
    twilio_phone_number = os.getenv(constants.environment.Twilio_Phone_Number)
    recipient_phone_number = os.getenv(constants.environment.Recipient_Phone_Number)
    sid = sms.send_message(
        internal_client,
        recipient_phone_number,
        twilio_phone_number,
        "Test: Sending Message Through Twilio",
    )
    assert sid is not None


@pytest.mark.twilio
def test_send_single_message_real_twilio_global_client():
    """Ensure that it is possible to send the SMS message through Twilio service."""
    twilio_phone_number = os.getenv(constants.environment.Twilio_Phone_Number)
    recipient_phone_number = os.getenv(constants.environment.Recipient_Phone_Number)
    sid = sms.send_message(
        client,
        recipient_phone_number,
        twilio_phone_number,
        "Test: Sending Message Through Twilio",
    )
    assert sid is not None


@mock.patch("mesmsage.sms.client.messages.create")
def test_send_single_message_mock_twilio(create_message_mock):
    """Ensure that it is possible to send the SMS message through a mocked Twilio service."""
    twilio_phone_number = os.getenv(constants.environment.Twilio_Phone_Number)
    recipient_phone_number = os.getenv(constants.environment.Recipient_Phone_Number)
    expected_sid = "SM87105da94bff44b999e4e6eb90d8eb6a"
    create_message_mock.return_value.sid = expected_sid
    sid = sms.send_message(
        client,
        recipient_phone_number,
        twilio_phone_number,
        "Test: Sending Message Through Twilio",
    )
    assert create_message_mock.called is True
    assert sid is not None
    assert sid == expected_sid


@mock.patch("mesmsage.sms.client.messages.create")
def test_send_single_message_mock_twilio_exception(create_message_mock, caplog):
    """Ensure that incorrectly sending the SMS message through a mocked Twilio service will create logging output."""
    twilio_phone_number = os.getenv(constants.environment.Twilio_Phone_Number)
    recipient_phone_number = os.getenv(constants.environment.Recipient_Phone_Number)
    error_message = f"Unable to create record: The 'To' number {twilio_phone_number} is not a valid phone number."
    status = 500
    uri = "/Accounts/ACXXXXXXXXXXXXXXXXX/Messages.json"
    create_message_mock.side_effect = TwilioRestException(
        status, uri, msg=error_message
    )
    sid = sms.send_message(
        client,
        recipient_phone_number,
        twilio_phone_number,
        "Test: Sending Message Through Twilio",
    )
    assert sid is None
    assert error_message in caplog.text
    assert constants.messages.Sms_Did_Not_Work in caplog.text
