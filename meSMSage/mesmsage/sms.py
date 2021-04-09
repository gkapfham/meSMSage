"""Create and send SMS messages using Twilio."""

import logging
import os

from typing import Dict

import phonenumbers  # type: ignore

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from mesmsage import constants

TWILIO_PHONE_NUMBER = os.getenv(constants.environment.Twilio_Phone_Number)
DEFAULT_FROM_NUMBER = TWILIO_PHONE_NUMBER


def send_message(client, to_number, from_number, message):
    """Send a message using the global Twilio client."""
    logger = logging.getLogger(constants.logging.Rich)
    try:
        sent_message = client.messages.create(
            to=to_number, from_=from_number, body=message
        )
    except TwilioRestException as e:
        logger.error("Sending SMS with Twilio did not work: " + str(e))
        return
    return sent_message.sid


def send_messages(message_dictionary: Dict[str, str]) -> str:
    """Use the Twilio client to send all of the messages in the provided dictionary."""
    client = Client()
    twilio_phone_number = os.getenv(constants.environment.Twilio_Phone_Number)
    twilio_phone_number_parsed = phonenumbers.parse(twilio_phone_number, "US")
    twilio_phone_number_e164 = phonenumbers.format_number(
        twilio_phone_number_parsed, phonenumbers.PhoneNumberFormat.E164
    )
    for phone_number_to, message in message_dictionary.items():
        phone_number_parsed = phonenumbers.parse(phone_number_to, "US")
        phone_number_e164 = phonenumbers.format_number(
            phone_number_parsed, phonenumbers.PhoneNumberFormat.E164
        )
        send_message(client, phone_number_e164, twilio_phone_number_e164, message)
