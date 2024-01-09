import os
import pymysql
import boto3
import json
from telebot import TeleBot, types
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
RDS_HOST = os.environ.get('RDS_HOST')
RDS_USER = os.environ.get('RDS_USER')
RDS_PASSWORD = os.environ.get('RDS_PASSWORD')
RDS_PORT = int(os.environ.get('RDS_PORT'))
RDS_DATABASE = os.environ.get('RDS_DATABASE')
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

bot = TeleBot(BOT_TOKEN)
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


with open('messages.json', 'r') as json_file:
    strings = json.load(json_file)


class User:
    user_attributes = {}
    
    def __init__(self, message):
        if not self.user_attributes == {}:
            self.user_attributes = {
                'user_id': message.from_user.id
            }
    
    def M1(self, message):
        markup = types.InlineKeyboardMarkup(row_width=2)
        message_txt = strings.get("M1message", "")
        button1 = types.InlineKeyboardButton(strings.get("S1message", ""), callback_data="S1")
        button2 = types.InlineKeyboardButton(strings.get("S2message", ""), callback_data="S2")
        button3 = types.InlineKeyboardButton(strings.get("S3message", ""), callback_data="S3")

        markup.add(button1, button2, button3)
        bot.send_message(message.chat.id, message_txt, reply_markup=markup)
    
    def M2(self):
        pass
    
    def M9(self):
        pass
    
    def save_to_database(self):
        conn = pymysql.connect(
        host=RDS_HOST,
        user=RDS_USER,
        password=RDS_PASSWORD,
        database=RDS_DATABASE,
        port=RDS_PORT
        )

        try:
            with conn.cursor() as cursor:
                columns = ', '.join(self.attributes.keys())
                values = ', '.join(['%s'] * len(self.attributes))
                sql = f"INSERT INTO user_data ({columns}) VALUES ({values})"
                cursor.execute(sql, tuple(self.attributes.values()))
            conn.commit()
        finally:
            conn.close()

def redirect_to_user(chat_id_to_redirect):
    redirect_message = strings.get("redirect_message", "")
    
    # Using parse_mode='markdown' to enable the hyperlink
    bot.send_message(chat_id_to_redirect, redirect_message, parse_mode='markdown')

@bot.message_handler(commands=['start', 'restart'])
def send_messages(message):
    new_user = User(message)
    new_user.M1(message)
    
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user_instance = User(call.message)
    if call.data == "S1":
        user_instance.M2()
    elif call.data == "S2":
        user_instance.M9()
    elif call.data == "S3":
        redirect_to_user(call.message.chat.id)
    
if __name__ == '__main__':
    bot.infinity_polling()