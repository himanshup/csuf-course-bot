from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request
from pymessenger.bot import Bot
from scrape import checkAvailability
import os

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)


@app.route("/", methods=['GET', 'POST'])
def receive():
    if request.method == 'GET':
        # If GET check if the request was made from Facebook
        token_sent = request.args.get("hub.verify_token")
        return verify(token_sent)
    else:
        # If POST request get the message that was sent
        data = request.get_json()
        for entry in data['entry']:
            messaging = entry['messaging']
            for message in messaging:
                if message.get('message'):
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        msg = message['message'].get('text')
                        send(
                            recipient_id, 'This might take a while...')
                        getMessage(recipient_id, msg)
                    else:
                        send(
                            recipient_id, 'Invalid, please enter a valid course (e.g. cpsc 121)')

    return 'message received', 200


def verify(token):
    if token == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'invalid verify token'


def getMessage(id, message):
    messages = msg.split(' ')
    subject = messages[0]
    course = messages[1]
    response = checkAvailability(subject.upper(), course)
    send(id, response)


def send(id, msg):
    bot.send_text_message(id, msg)
    return 'message sent'


if __name__ == '__main__':
    app.run()
