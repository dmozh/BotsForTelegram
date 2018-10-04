import threading, asyncio
import types
from create_helper import credentials, sql_requests, SearchVideo
import requests, datetime, json
import psycopg2
from pytube import YouTube

# This class is main logic for my bot
class BotHandler:
    def __init__(self, input_msg, chat_id, user_name, user_fname, user_id, date):
        self.input_msg = input_msg
        self.chat_id = chat_id
        self.user_name = user_name
        self.user_fname = user_fname
        self.user_id = user_id
        self.date = date

        self.requested_audio=None
        self.audio = None
        self.audio_duration = None
        self.audio_title = None
        self.audio_performer = None

    async def send_audio(self):

        search_result = SearchVideo.youtube_search(self.audio)
        link = "https://www.youtube.com/watch?v=" + search_result
        yt = YouTube(link)
        print(yt.streams.filter(only_audio=True).all())
        audio_stream = yt.streams.filter(only_audio=True).first()

        file_id = self.select_audio(yt.title, link)
        if file_id != "":
            params = {'chat_id': self.chat_id,
                      'audio': file_id,
                      'duration': self.audio_duration,
                      # 'title': self.audio_title,
                      'performer': self.audio_performer
                      }
            response = requests.post(credentials.ROOT_URL + 'sendAudio', data=params)

            return response.json()

        else:
            self.audio_duration = yt.length
            self.audio_performer = yt.title
            self.audio_title = yt.title
            buffer = audio_stream.stream_to_buffer()

            #
            # files = {'audio': open('C:\\Users\\dmozh\\Desktop\\FunMode-uhoju.mp3', 'rb')}
            files = {'audio': buffer.getbuffer()}

            # files = {'photo': open('C:\\Users\\dmozh\\Desktop\\1.jpg', 'rb')}

            params = {'chat_id': self.chat_id,
                      'duration': self.audio_duration,
                      # 'title': self.audio_title,
                      'performer': self.audio_performer
                      }

            response = requests.post(credentials.ROOT_URL + 'sendAudio', data=params, files = files)
            # response = requests.post(credentials.ROOT_URL + 'sendPhoto', data=params, files=files)

            json_result = response.json()
            file_id = json_result['result']['audio']['file_id']
            print('fileid', json_result['result']['audio']['file_id'])
            print(json_result)
            self.insert_audio(file_id, self.audio_performer, link)

            return json_result

        # return json_result

    def send_msg(self, text='i wait your question'):
        params = {'chat_id': self.chat_id, 'text': text}
        response = requests.post(credentials.ROOT_URL + 'sendMessage', json=params)
        return response.json()

    # In this method i processing input msg
    # In the future i will use RE for more flexible processing msg

    # @asyncio.coroutine
    async def handle(self):
        if 'Hi' in self.input_msg:
            if self.user_name == "":
                self.send_msg("Hi " + self.user_fname)
            self.send_msg("Hi " + self.user_name)
        elif '!test' in self.input_msg.lower():
            self.audio = self.input_msg[6:len(self.input_msg)]
            print("Requested audio:", self.audio)

            self.send_msg("Отправка песни может занять несколько минут"+"\n"
                          +"Пожалуйста подождите"+"\n"
                          +"Все последующие сообщения или запросы обработаются в порядке очерди.")
            #

            await self.send_audio()
            self.send_msg("Приятного прослушивания")
            # thread = threading.Thread(target=self.send_audio)
            # thread.start()


    #SQLs methods
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

        cursor.execute(sql_requests.INSERT_MSG, (self.user_id, self.input_msg, date))

        connection.commit()
        # Close communication with the database
        cursor.close()
        connection.close()

    @staticmethod
    def insert_audio(audio_id, audio_name, audio_link):
        connection = psycopg2.connect(credentials.DB_CRED)
        # Open a cursor to perform database operations
        cursor = connection.cursor()

        cursor.execute(sql_requests.INSERT_AUDIO, (audio_id, audio_name, audio_link))

        connection.commit()
        # Close communication with the database
        cursor.close()
        connection.close()

    @staticmethod
    def select_audio(name, link):
        connection = psycopg2.connect(credentials.DB_CRED)
        # Open a cursor to perform database operations
        cursor = connection.cursor()
        sql_params = "audio_name = " + "'" + name + "'" + " and audio_link = " + "'" + link + "'" +";"
        cursor.execute(sql_requests.SELECT_AUDIO+sql_params)
        try:
            result = cursor.fetchone()[0]
        except TypeError:
            result = ""
        connection.commit()
        # Close communication with the database
        cursor.close()
        connection.close()

        return result