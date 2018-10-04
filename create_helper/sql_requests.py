SELECT_USERS = "SELECT * FROM users;"
SELECT_AUDIO = "SELECT file_id FROM audios WHERE "

INSERT_USER = "INSERT INTO users (user_id, user_name) VALUES (%s, %s)"
INSERT_MSG = "INSERT INTO msgs (user_id, msg_text, datetime) VALUES (%s, %s, %s)"
INSERT_AUDIO = "INSERT INTO audios (file_id, audio_name, audio_link) VALUES (%s, %s, %s)"