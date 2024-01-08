import os
import telebot
import pymysql
import boto3
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

bot = telebot.TeleBot(BOT_TOKEN)
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# Initialize MySQL connection to Amazon RDS
conn = pymysql.connect(
    host=RDS_HOST,
    user=RDS_USER,
    password=RDS_PASSWORD,
    database=RDS_DATABASE,
    port=RDS_PORT
)

#conn.execute() 
cursor = conn.cursor()

@bot.message_handler(commands=['start', 'restart'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")
    
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, "Invalid statement")


#bot.infinity_polling()