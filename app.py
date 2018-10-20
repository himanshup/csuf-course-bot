from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request
from pymessenger.bot import Bot
import os

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)


@app.route("/", methods=['GET', 'POST'])
def receive():
    if request.method == 'GET':
        # If GET check if the request was made from Facebook
        token = request.args.get("hub.verify_token")
        return verify_token(token)
    else:
        # If POST request get the message that was sent
        data = request.get_json()
        for entry in data['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        msg = message['message'].get('text')
                        send_message(
                            recipient_id, 'This might take a while...')
                        send_message(recipient_id, msg)
                    else:
                        send_message(
                            recipient_id, 'Invalid, please enter a valid course (e.g. cpsc 121)')

    return 'message received', 200


def verify(token):
    if token == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'invalid verify token'


def send(id, message):
    bot.send_text_message(id, message)


if __name__ == '__main__':
    app.run()
