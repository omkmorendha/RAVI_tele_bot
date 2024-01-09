import os
import pymysql
import boto3
import json
from telebot import TeleBot, types
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
RDS_HOST = os.environ.get("RDS_HOST")
RDS_USER = os.environ.get("RDS_USER")
RDS_PASSWORD = os.environ.get("RDS_PASSWORD")
RDS_PORT = int(os.environ.get("RDS_PORT"))
RDS_DATABASE = os.environ.get("RDS_DATABASE")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")

bot = TeleBot(BOT_TOKEN)
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


with open("messages.json", "r") as json_file:
    strings = json.load(json_file)


class User:
    def __init__(self, message):
        self.attributes = {}
        users[message.from_user.id] = self

    def M1(self, message):
        markup = types.InlineKeyboardMarkup(row_width=1)
        message_txt = strings.get("M1message", "")
        button1 = types.InlineKeyboardButton(
            strings.get("S1message", ""), callback_data="S1"
        )
        button2 = types.InlineKeyboardButton(
            strings.get("S2message", ""), callback_data="S2"
        )
        button3 = types.InlineKeyboardButton(
            strings.get("S3message", ""), callback_data="S3"
        )

        markup.add(button1, button2, button3)
        bot.send_message(message.chat.id, message_txt, reply_markup=markup)

    def M2(self, message):
        markup = types.InlineKeyboardMarkup()
        message_txt = strings.get("M2message", "")
        button1 = types.InlineKeyboardButton(
            strings.get("S4message", ""), callback_data="S4"
        )
        button2 = types.InlineKeyboardButton(
            strings.get("S5message", ""), callback_data="S5"
        )
        button3 = types.InlineKeyboardButton(
            strings.get("S6message", ""), callback_data="S6"
        )
        button4 = types.InlineKeyboardButton(
            strings.get("S7message", ""), callback_data="S7"
        )
        button5 = types.InlineKeyboardButton(
            strings.get("S8message", ""), callback_data="S8"
        )
        button6 = types.InlineKeyboardButton(
            strings.get("edit_message", ""), callback_data="start"
        )
        
        markup.add(button1, button2, button3, button4, button5, button6)
        bot.send_message(message.chat.id, message_txt, reply_markup=markup)

    def M3(self, message):
        markup = types.InlineKeyboardMarkup()
        message_txt = strings.get("M3message", "")
        button1 = types.InlineKeyboardButton(
            strings.get("S9message", ""), callback_data="S9"
        )
        button2 = types.InlineKeyboardButton(
            strings.get("S10message", ""), callback_data="S10"
        )
        button3 = types.InlineKeyboardButton(
            strings.get("edit_message", ""), callback_data="S1"
        )
        button4 = types.InlineKeyboardButton(
            strings.get("restart_message", ""), callback_data="start"
        )
        markup.add(button1, button2, button3, button4)
        bot.send_message(message.chat.id, message_txt, reply_markup=markup)
    
    def M4(self, message):
        markup = types.InlineKeyboardMarkup()
        message_txt = strings.get("M4message", "")
        button1 = types.InlineKeyboardButton(
            strings.get("S11message", ""), callback_data="S11"
        )
        button2 = types.InlineKeyboardButton(
            strings.get("S12message", ""), callback_data="S12"
        )
        button3 = types.InlineKeyboardButton(
            strings.get("S13message", ""), callback_data="S13"
        )
        button4 = types.InlineKeyboardButton(
            strings.get("edit_message", ""), callback_data="M3"
        )
        button5 = types.InlineKeyboardButton(
            strings.get("restart_message", ""), callback_data="start"
        )
        
        markup.add(button1, button2, button3, button4, button5)
        bot.send_message(message.chat.id, message_txt, reply_markup=markup)
    
    def M5(self, message):
        markup = types.InlineKeyboardMarkup()
        message_txt = strings.get("M5message", "")
        button1 = types.InlineKeyboardButton(
            strings.get("S14message", ""), callback_data="S14"
        )
        button2 = types.InlineKeyboardButton(
            strings.get("S15message", ""), callback_data="S15"
        )
        button3 = types.InlineKeyboardButton(
            strings.get("S16message", ""), callback_data="S16"
        )
        button4 = types.InlineKeyboardButton(
            strings.get("S17message", ""), callback_data="S17"
        )
        button5 = types.InlineKeyboardButton(
            strings.get("edit_message", ""), callback_data="M4"
        )
        button6 = types.InlineKeyboardButton(
            strings.get("restart_message", ""), callback_data="start"
        )
        
        markup.add(button1, button2, button3, button4, button5, button6)
        bot.send_message(message.chat.id, message_txt, reply_markup=markup)
    
    def M6(self, message):
        inline_markup = types.InlineKeyboardMarkup()
        message_txt = strings.get("M6message", "")
        
        button1 = types.InlineKeyboardButton(
            strings.get("edit_message", ""), callback_data="M5"
        )
        button2 = types.InlineKeyboardButton(
            strings.get("restart_message", ""), callback_data="start"
        )

        inline_markup.add(button1, button2)

        reply_markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        direct_button1 = types.KeyboardButton("Direct Input 1")
        direct_button2 = types.KeyboardButton("Direct Input 2")
        reply_markup.add(direct_button1, direct_button2)

        bot.send_message(message.chat.id, message_txt, reply_markup=inline_markup)
        bot.send_message(message.chat.id, strings.get("choose_options", ""), reply_markup=reply_markup)
        
        self.current_state = "M6"
    
    def M7(self, message):
        inline_markup = types.InlineKeyboardMarkup()
        message_txt = strings.get("M7message", "")
        
        button1 = types.InlineKeyboardButton(
            strings.get("edit_message", ""), callback_data="M6"
        )
        button2 = types.InlineKeyboardButton(
            strings.get("restart_message", ""), callback_data="start"
        )

        inline_markup.add(button1, button2)

        reply_markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        direct_button1 = types.KeyboardButton("Direct Input 1")
        direct_button2 = types.KeyboardButton("Direct Input 2")
        reply_markup.add(direct_button1, direct_button2)

        bot.send_message(message.chat.id, message_txt, reply_markup=inline_markup)
        bot.send_message(message.chat.id, strings.get("choose_options", ""), reply_markup=reply_markup)
        
        self.current_state = "M7"
    
    def M8(self, message):
        markup = types.InlineKeyboardMarkup()
        message_txt = strings.get("M8message", "")
        button1 = types.InlineKeyboardButton(
            strings.get("S18message", ""), callback_data="S18"
        )
        button2 = types.InlineKeyboardButton(
            strings.get("S19message", ""), callback_data="S19"
        )
        button3 = types.InlineKeyboardButton(
            strings.get("S20message", ""), callback_data="S20"
        )
        button4 = types.InlineKeyboardButton(
            strings.get("S21message", ""), callback_data="S21"
        )
        button5 = types.InlineKeyboardButton(
            strings.get("S22message", ""), callback_data="S22"
        )
        button6 = types.InlineKeyboardButton(
            strings.get("edit_message", ""), callback_data="M4"
        )
        button7 = types.InlineKeyboardButton(
            strings.get("restart_message", ""), callback_data="start"
        )
        
        markup.add(button1, button2, button3, button4, button5, button6, button7)
        bot.send_message(message.chat.id, message_txt, reply_markup=markup)
    
    def M9(self, message):
        pass

    def save_to_database(self):
        conn = pymysql.connect(
            host=RDS_HOST,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database=RDS_DATABASE,
            port=RDS_PORT,
        )

        try:
            with conn.cursor() as cursor:
                columns = ", ".join(self.attributes.keys())
                values = ", ".join(["%s"] * len(self.attributes))
                sql = f"INSERT INTO user_data ({columns}) VALUES ({values})"
                cursor.execute(sql, tuple(self.attributes.values()))
            conn.commit()
        finally:
            conn.close()


def redirect_to_user(chat_id_to_redirect):
    redirect_message = strings.get("redirect_message", "")
    bot.send_message(chat_id_to_redirect, redirect_message, parse_mode="markdown")


@bot.message_handler(commands=["start", "restart"])
def send_messages(message):
    new_user = User(message)
    new_user.M1(message)

# Message handler for direct input
@bot.message_handler(func=lambda message: hasattr(message, 'text'))
def handle_direct_input(message):
    user_instance = users.get(message.from_user.id, None)

    if user_instance and hasattr(user_instance, 'current_state'): 
        if user_instance.current_state == "M6":
            user_instance.attributes["Area_of_Residence"] = message.text
            user_instance.current_state = None
            user_instance.M7(message)
        
        elif user_instance.current_state == "M7":
            user_instance.attributes["Violating_Organisation"] = message.text
            user_instance.current_state = None
            user_instance.M8(message)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user_instance = users[call.message.chat.id]
    
    if call.data == "S1":
        user_instance.M2(call.message)
    
    elif call.data == "S2":
        user_instance.M9(call.message)
    
    elif call.data == "S3":
        redirect_to_user(call.message.chat.id)
    
    elif call.data in ["S4", "S5", "S6", "S7", "S8"]:
        user_instance.attributes["Violence"] = strings.get(call.data + "message", "")
        user_instance.M3(call.message)
    
    elif call.data in ["S9", "S10"]:
        user_instance.attributes["Testimony_for"] = strings.get(call.data + "message", "")
        user_instance.M4(call.message)
    
    elif call.data in ["S11", "S12", "S13"]:
        user_instance.attributes["Gender"] = strings.get(call.data + "message", "")
        user_instance.M5(call.message)
    
    elif call.data in ["S14", "S15", "S16", "S17"]:
        user_instance.attributes["Age"] = strings.get(call.data + "message", "")
        user_instance.M6(call.message)
    
    elif call.data in ["S18", "S19", "S20", "S21", "S22"]:
        user_instance.attributes["Type_of_violation"] = strings.get(call.data + "message", "")
        print(user_instance.attributes)
        user_instance.M9(call.message)
        
    elif call.data == "start":
        user_instance.M1(call.message)
    
    elif call.data == "M3":
        user_instance.M3(call.message)
        
    elif call.data == "M4":
        user_instance.M4(call.message)
    
    elif call.data == "M5":
        user_instance.M5(call.message)
    
    elif call.data == "M6":
        user_instance.M6(call.message)
    
    elif call.data == "M7":
        user_instance.M7(call.message)
    
    elif call.data == "M8":
        user_instance.M8(call.message)
    
    elif call.data == "M9":
        user_instance.M9(call.message)

if __name__ == "__main__":
    users = {}
    bot.polling()