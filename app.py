import random
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)

ACCESS_TOKEN = 'EAADgKyefUVgBADfuFA7oacTa82giKVhtMPqjljc0gAYTi2zcFB3esphOhRUYpZBwQnFdgZCg20WDTSzgdMPbh6xPwY8bsjJDiSjLyg17YZCrEpDOswL9nNVMwS0XnDZABXtRavwtvjBUErZAi0g4gLhoWcuz02EJTFxOkXgHtV262NGfaatrQ'
VERIFY_TOKEN = 'YOUR_VERIFY_TOKEN'

bot = Bot(ACCESS_TOKEN)


@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args['hub.verify_token']
        return verify_fb_token(token_sent)
    else:
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = get_message()
                    send_message(recipient_id, response_sent_text)
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
        return "Message Processed"


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args['hub.challenge']
    else:
        return 'Invalid verification token'


def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return 'Success'


def get_message():
    sample_responses = ["Потрясающе!", "Я вами горжусь!", "Продолжайте в том же духе!",
                        "Лучшее, что я когда-либо видел!", "Валера, это ты?"]
    return random.choice(sample_responses)


if __name__ == '__main__':
    app.run()
