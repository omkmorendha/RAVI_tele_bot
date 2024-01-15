# Telegram Bot for Data Collection
This Python script implements a Telegram bot for collecting data from users. The bot is designed to guide users through a series of questions and collect information related to different categories. This is a multilingual telegram bot that supports both English and Farsi, so women can report human rights violation for themselves or others.

For data storage and database handling, S3 and Amazon RDS was used, and then it was hosted on the AWS EC2 service.

## Prerequisites
Make sure you have the following dependencies installed:

- Python (>= 3.6)
- Telebot
- Pymysql
- Boto3
- Requests
- python-dotenv

## Setup
1. Clone the repository:
```
https://github.com/omkmorendha/RAVI_tele_bot
```
2. Install dependencies:
```
pip install telebot pymysql boto3 requests python-dotenv
```
3. Create a .env file in the project directory and add the following environment variables:
```
BOT_TOKEN=<your_telegram_bot_token>
AWS_ACCESS_KEY_ID=<your_aws_access_key_id>
AWS_SECRET_ACCESS_KEY=<your_aws_secret_access_key>
RDS_HOST=<your_rds_host>
RDS_USER=<your_rds_user>
RDS_PASSWORD=<your_rds_password>
RDS_PORT=<your_rds_port>
RDS_DATABASE=<your_rds_database>
S3_BUCKET_NAME=<your_s3_bucket_name>
```
4. Create the required JSON files (messages_eng.json and messages_farsi.json) with the necessary message strings for different languages.
5. Run the script
```
python main.py
```
