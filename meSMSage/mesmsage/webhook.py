"""Run a Webhook server to receive SMS messages from Twilio."""

import os

from datetime import datetime
from logging import Logger

from flask import Flask, request
from gevent.pywsgi import WSGIServer  # type: ignore
from pyngrok import ngrok  # type: ignore

from rich.console import Console

from twilio.rest import Client  # type: ignore
from twilio.twiml.messaging_response import MessagingResponse  # type: ignore

from mesmsage import configure
from mesmsage import constants
from mesmsage import nlp
from mesmsage import sheets

# create the Flask app that is run with the gevent WSGIServer
app = Flask(__name__)

response_sheet = None


def start_ngrok(logger: Logger, console: Console) -> None:
    """Start the local ngrok service and then update the WebHook configuration in Twilio."""
    logger.debug("Starting the ngrok service and registering it with Twilio")
    # use pyngrok to create a local ngrok service and then connect it
    # to the public ngrok server running in the ngrok public cloud
    url = ngrok.connect(constants.webhooks.Port).public_url
    console.print("Started the ngrok service")
    console.print(f"--> Tunnel URL for ngrok: {url}")
    # create a Twilio client using the defined environment variables
    # and then use this client to set the ngrok server's automatically
    # generated URL as the webhook URL in the Twilio service
    client = Client()
    client.incoming_phone_numbers.list(
        phone_number=os.environ.get(constants.environment.Twilio_Phone_Number)
    )[0].update(sms_url=url + constants.webhooks.Route)
    console.print("Added ngrok tunnel the Twilio messaging webhook entry")


@app.route(constants.webhooks.Route, methods=[constants.webhooks.Method])
def bot():
    """Receive a webhook response from the Twilio service, including all details about the message."""
    # create a logger
    logger = configure.configure_logging()
    # inspect the response received by the webhook and:
    # --> extract the phone number of the response creator
    user = request.values.get("From", "")
    # --> extract the message
    message = request.values.get("Body", "")
    # create a timestamp representing when webhook received the message
    timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    # calculate the intent scores for the message received from the user
    intent_scores_dictionary = nlp.calculate_intent_scores(message, True)
    # summarize the intent scores by finding the maximum score for each intent
    summarized_intent_scores_dictionary = nlp.summarize_intent_scores(
        intent_scores_dictionary
    )
    logger.debug(intent_scores_dictionary)
    logger.debug(summarized_intent_scores_dictionary)
    response, intent = nlp.create_response(summarized_intent_scores_dictionary)
    logger.debug(response)
    # create and send the response using the Twilio service
    resp = MessagingResponse()
    resp.message(response)
    # create a dictionary that represents the response that was
    # send back to the user and then log this response in a Google sheet
    new_response = {
        "Timestamp": timestamp,
        "Individual Phone Number": user,
        "Message": message,
        "Response": response,
        "Classified Intent": intent,
    }
    sheets.add_row(response_sheet, new_response)
    return str(resp)


def main(googlesheet_id: str, logger: Logger, console: Console) -> None:
    """Start the local ngrok server and the WSGI server from gevent to receive webhooks."""
    # start the ngrok reverse proxy service
    start_ngrok(logger, console)
    # connect to the Google sheet used for logging the response messages
    global response_sheet
    response_sheet = sheets.connect_to_sheet(googlesheet_id)
    # start the production WSGI server provided by gevent
    http_server = WSGIServer(
        (constants.webhooks.No_Listener, constants.webhooks.Port), app, log=logger
    )
    # configure the WSGI server from gevent to always continue to run and
    # receive webhook information from the Twilio service
    console.print("Run the WSGI server in a gevent loop")
    http_server.serve_forever()
