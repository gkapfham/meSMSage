"""Run a Webhook server to receive SMS messages from Twilio."""

import os

from datetime import datetime
from logging import Logger

from flask import Flask, request
from gevent.pywsgi import WSGIServer
from pyngrok import ngrok

from rich.console import Console

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from mesmsage import constants
from mesmsage import sheets

app = Flask(__name__)

response_sheet = None


def start_ngrok(logger: Logger, console: Console) -> None:
    """Start the local ngrok service and then update the WebHook configuration in Twilio."""
    url = ngrok.connect(constants.webhooks.Port).public_url
    console.print("Started the ngrok service")
    console.print(f"--> Tunnel URL for ngrok: {url}")
    client = Client()
    client.incoming_phone_numbers.list(
        phone_number=os.environ.get(constants.environment.Twilio_Phone_Number)
    )[0].update(sms_url=url + constants.webhooks.Route)
    console.print("Added ngrok tunnel the Twilio messaging webhook entry")


@app.route(constants.webhooks.Route, methods=[constants.webhooks.Method])
def bot():
    """Receive a webhook response from the Twilio service, including all details about the message."""
    user = request.values.get("From", "")
    message = request.values.get("Body", "")
    resp = MessagingResponse()
    timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    response = f"Hello, {user}, thank you for your message!"
    resp.message(response)
    new_response = {
        "Timestamp": timestamp,
        "Individual Phone Number": user,
        "Message": message,
        "Response": response
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
