"""Run a Webhook server to receive SMS messages from Twilio."""

import os

from dotenv import load_dotenv

from flask import Flask, request
from gevent.pywsgi import WSGIServer
from pyngrok import ngrok

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from mesmsage import constants


app = Flask(__name__)


def start_ngrok():
    """Start the local ngrok service and then update the WebHook configuration in Twilio."""
    url = ngrok.connect(constants.webhooks.Port).public_url
    print(" * Tunnel URL:", url)
    client = Client()
    client.incoming_phone_numbers.list(
        phone_number=os.environ.get(constants.environment.Twilio_Phone_Number)
    )[0].update(sms_url=url + constants.webhooks.Route)


@app.route(constants.webhooks.Route, methods=[constants.webhooks.Method])
def bot():
    """Receive a webhook response from the Twilio service, including all details about the message."""
    user = request.values.get("From", "")
    resp = MessagingResponse()
    resp.message(f"Hello, {user}, thank you for your message!")
    return str(resp)


def main():
    """Start the local ngrok server and the WSGI server from gevent to receive webhooks."""
    load_dotenv()
    start_ngrok()
    http_server = WSGIServer(
        (constants.webhooks.No_Listener, constants.webhooks.Port), app
    )
    http_server.serve_forever()
