from create_helper import create_helper_main, credentials
import requests



# This class is main logic for my bot
class BotHandler:
    def __init__(self, input_msg, chat_id):
        self.input_msg = input_msg
        self.chat_id = chat_id

    def send_msg(self, text='i wait your question'):
        params = {'chat_id': self.chat_id, 'text': text}
        response = requests.post(credentials.ROOT_URL + 'sendMessage', json=params)
        return response.json()

    # In this method i processing input msg
    # In the future i will use RE for more flexible processing msg
    def handler(self):
        if 'Hi' in self.input_msg:
            self.send_msg("Hi guest")
