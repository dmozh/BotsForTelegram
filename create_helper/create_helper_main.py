import asyncio
import requests
import subprocess, multiprocessing
from create_helper import bot_handler, credentials, sql_requests
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
    event.wait(5)
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

        # thread = threading.Thread(target=action(r))
        # thread.start()
        if __name__ == "__main__":
            p = multiprocessing.Process(target=action, args=(r, ))
            p.start()
            p.join()

        #
        # sql_handle = bot_handler.SQLHandler(user_id, user_name, user_fname, msg, msg_date)
        # sql_handle.insert_user()
        # sql_handle.insert_msg()

        return jsonify(r)
    return 'It is very-very bad('

def action(r):
    chat_id = ""
    upd_date = ""
    user_id = ""
    user_fname = ""
    msg = ""
    try:
        chat_id = r['message']['chat']['id']  # get simple chat id and msg
        upd_date = r['message']['date']
        user_id = r['message']['from']['id']
        user_fname = r['message']['from']['first_name']
        msg = r['message']['text']
        # print(msg)
    except KeyError:
        try:
            chat_id = r['edited_message']['chat']['id']  # get text from edited msg
            upd_date = r['edited_message']['date']
            edit_date = r['edited_message']['edit_date']
            user_id = r['edited_message']['from']['id']
            user_fname = r['edited_message']['from']['first_name']
            msg = r['edited_message']['text']
            # print(msg)
        except KeyError:
            try:
                msg = r['message']['forward_from']['text']  # get text from forward msg
                # print(msg)
            except KeyError:
                try:
                    msg = r['message']['reply_to_message']['text']  # get text from reply
                except KeyError:
                    print("Another action")
    try:
        user_name = r['message']['from']['username']
    except KeyError:
        try:
            user_name = r['edited_message']['from']['username']
        except KeyError:
            print('User dont have @username')
            user_name = ""

    print(r)
    print(chat_id)
    print(user_id)
    print(user_name)
    print(user_fname)
    print(msg)

    chat_handle = bot_handler.BotHandler(msg, chat_id, user_name, user_fname, user_id, upd_date)
    loop = asyncio.ProactorEventLoop()  # only OS win32 system method
    asyncio.set_event_loop(loop)
    loop.run_until_complete(chat_handle.handle())


if __name__ == '__main__':
    set_tonel()
    set_webhook()
    app.run()
    # pass