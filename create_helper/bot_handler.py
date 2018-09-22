from create_helper import create_helper_main, credentials, sql_requests
import requests, datetime
import psycopg2


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
    def handle(self):
        if 'Hi' in self.input_msg:
            self.send_msg("Hi guest")



class SQLHandler:
    def __init__(self, user_id, user_name, msg, date):
        self.user_id = user_id
        self.user_name = user_name
        self.date = date
        self.msg = msg

    def insert_user(self):
        connection = psycopg2.connect(credentials.DB_CRED)
        # Open a cursor to perform database operations
        cursor = connection.cursor()
        try:
            cursor.execute(sql_requests.INSERT_USER, (self.user_id, self.user_name))

            connection.commit()
            # Close communication with the database
            cursor.close()
            connection.close()
        except psycopg2.IntegrityError:
            print("user is exist")
        finally:
            cursor.close()
            connection.close()


    def insert_msg(self):
        connection = psycopg2.connect(credentials.DB_CRED)
        # Open a cursor to perform database operations
        cursor = connection.cursor()

        date = datetime.datetime.fromtimestamp(
            int(self.date)).strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute(sql_requests.INSERT_MSG, (self.user_id, self.msg, date))

        connection.commit()
        # Close communication with the database
        cursor.close()
        connection.close()