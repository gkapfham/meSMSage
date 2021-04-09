"""Create and send SMS messages using Twilio."""

import logging
import os

from typing import Dict
from typing import List

import phonenumbers  # type: ignore

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from mesmsage import constants


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


def send_messages(message_dictionary: Dict[str, str]) -> List[str]:
    """Use the Twilio client to send all of the messages in the provided dictionary."""
    # create a client using those authentication variables found in environment variables
    client = Client()
    # create an empty list of the message SIDs that are returned from send_message
    sid_list = []
    # extract the Twilio phone number stored in the environment that will be the number
    # that is used to send the SMS messages. This number will appear in the messaging
    # app of the person who receives the SMS message. It was purchased through Twilio.
    twilio_phone_number = os.getenv(constants.environment.Twilio_Phone_Number)
    # ensure that the Twilio phone number is in the E164 international format:
    # https://support.twilio.com/hc/en-us/articles/223183008-Formatting-International-Phone-Numbers
    twilio_phone_number_parsed = phonenumbers.parse(
        twilio_phone_number, constants.locales.Us
    )
    twilio_phone_number_e164 = phonenumbers.format_number(
        twilio_phone_number_parsed, phonenumbers.PhoneNumberFormat.E164
    )
    # iterate through each of the {phone number, message} pairs inside of message_dictionary
    # and complete the following tasks:
    # 1. Convert the phone number to the E164 international format
    # 2. Use the send_message function in this module to send the message
    # 3. Collect the message SID in the list of SIDs for diagnostic purposes
    for phone_number_to, message in message_dictionary.items():
        phone_number_parsed = phonenumbers.parse(phone_number_to, constants.locales.Us)
        phone_number_e164 = phonenumbers.format_number(
            phone_number_parsed, phonenumbers.PhoneNumberFormat.E164
        )
        sid = send_message(client, phone_number_e164, twilio_phone_number_e164, message)
        sid_list.append(sid)
    # return the list of message SIDs for diagnostic purposes
    return sid_list
