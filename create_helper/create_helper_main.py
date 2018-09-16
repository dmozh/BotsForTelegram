import requests
import subprocess
from create_helper import bot_handler, credentials
from flask import Flask, request, jsonify
import threading
import json


app = Flask(__name__)

#set tonnel for access on local web server
def set_tonel():
    # add thread for process
    t = threading.Thread(target=start_ngrok)
    # t.daemon = True
    t.start()

#start subprocess
def start_ngrok():
    subprocess.run(credentials.NGROK_URL)
    # print(subprocess.run(credentials.NGROK_URL))

#get url for setting a webhook
def get_url_link():
    event = threading.Event()
    event.wait(2)
    url=''
    #try parse
    try:
        api_url = 'http://127.0.0.1:4040/api/tunnels'
        response = requests.get(api_url)
        parsed = json.loads(response.text)
        if parsed['tunnels'][1]['proto']=='http':
            url = parsed['tunnels'][0]['public_url']
        else:
            url = parsed['tunnels'][1]['public_url']
    except IndexError:
        print('index error')
        get_url_link()

    return url

#setting webhook
def set_webhook():
    url = get_url_link()
    print(url)
    req = requests.post(credentials.ROOT_URL+'setWebhook?url='+url)
    print(req.status_code,  '\n',
          req.text)



#main method
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        msg = r['message']['text']

        handler = bot_handler.BotHandler(msg, chat_id)
        handler.handler()

        return jsonify(r)
    return 'It is very-very bad('


if __name__ == '__main__':
    set_tonel()
    set_webhook()
    app.run()