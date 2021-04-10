"""Create and send SMS messages using Twilio."""

import logging
import os

from typing import Dict
from typing import List

import phonenumbers  # type: ignore

from dotenv import load_dotenv

from twilio.base.exceptions import TwilioRestException  # type: ignore
from twilio.rest import Client  # type: ignore

from mesmsage import constants

# create a client using those authentication
# variables found in environment variables
load_dotenv()
client = Client()


def send_message(client: Client, to_number: str, from_number: str, message: str) -> str:
    """Send a message using the provided Twilio client."""
    logger = logging.getLogger(constants.logging.Rich)
    # send the message using the Twilio client object.
    # Note that the from_number must be a number that is
    # registered with Twilio; this means that you cannot
    # include any potential number for the from_ parameter
    try:
        sent_message = client.messages.create(
            to=to_number, from_=from_number, body=message
        )
    # something went wrong with sending the message, so log
    # it as an error that will be visible in the logging system
    except TwilioRestException as e:
        logger.error(constants.messages.Sms_Did_Not_Work + constants.markers.Space + str(e))
        return None
    # return the 34-character string that serves as the unique
    # identifier for this specific message sent through Twilio.
    # Note that an sid pre-pended with "SM" means that it was a
    # text message and with "MM" means that it was a media message
    return sent_message.sid


def send_messages(message_dictionary: Dict[str, str]) -> List[str]:
    """Use the Twilio client to send all of the messages in the provided dictionary."""
    # note that the client is created globally as part of this module
    # create an empty list of the message SIDs that are returned from send_message
    sid_list = []
    # extract the Twilio phone number stored in the environment that will be the number
    # that is used to send the SMS messages. This number will appear in the messaging
    # app of the person who receives the SMS message. It was purchased through Twilio.
    twilio_phone_number = os.getenv(constants.environment.Twilio_Phone_Number)
    # ensure that the Twilio phone number is in the E164 international format:
    # https://support.twilio.com/hc/en-us/articles/223183008-Formatting-International-Phone-Numbers
    twilio_phone_number_parsed = phonenumbers.parse(
        twilio_phone_number, constants.locations.Us
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
        phone_number_parsed = phonenumbers.parse(
            phone_number_to, constants.locations.Us
        )
        phone_number_e164 = phonenumbers.format_number(
            phone_number_parsed, phonenumbers.PhoneNumberFormat.E164
        )
        sid = send_message(client, phone_number_e164, twilio_phone_number_e164, message)
        sid_list.append(sid)
    # return the list of message SIDs for diagnostic purposes
    return sid_list
