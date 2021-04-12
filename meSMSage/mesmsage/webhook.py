"""Run a server to receive SMS messages."""

import os
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


def start_ngrok():
    from twilio.rest import Client
    from pyngrok import ngrok

    url = ngrok.connect(5000).public_url
    print(" * Tunnel URL:", url)
    client = Client()
    client.incoming_phone_numbers.list(
        phone_number=os.environ.get("TWILIO_PHONE_NUMBER")
    )[0].update(sms_url=url + "/bot")


# print("Here")
# load_dotenv()

# if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
#     start_ngrok()
# app = Flask(__name__)


@app.route("/bot", methods=["POST"])
def bot():
    user = request.values.get("From", "")
    resp = MessagingResponse()
    resp.message(f"Hello, {user}, thank you for your message!")
    return str(resp)


def main():
    """Start servers."""
    load_dotenv()
    # if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
    start_ngrok()
    app.run(debug=True, use_reloader=False)


if __name__ == "__main__":
    print("Something")
    main()
