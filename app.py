#gpt 4 NEW 123server HABR https://habr.com/ru/companies/amvera/articles/829592/

import openai
import telebot
import logging
import os
import time
from openai import OpenAI

client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY")
)
bot = telebot.TeleBot('7252971102:AAFmEtvdlp7nA-LVhpGH3pYnOUb0BhKFfC4')

log_dir = os.path.join(os.path.dirname(__file__), 'ChatGPT_Logs')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(filename=os.path.join(log_dir, 'error.log'), level=logging.ERROR,
                    format='%(levelname)s: %(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет!\nЯ ChatGPT 4.0 Telegram Bot\U0001F916\nЗадай мне любой вопрос и я постараюсь на него ответиь')

#def generate_response(prompt):
#        completion = openai.chat.completions.create(
#            model="gpt-4",
#            messages=[
#                {"role": "user", "content": prompt}
#            ]
#        )
#        return completion.choices[0].message.content
def generate_response(prompt):
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
	model="gpt-4o",
    )
    return response.choices[0].message.content.strip()


@bot.message_handler(commands=['bot'])
def command_message(message):
    prompt = message.text
    response = generate_response(prompt)
    bot.reply_to(message, text=response)


@bot.message_handler(func = lambda _: True)
def handle_message(message):
    prompt = message.text
    response = generate_response(prompt)
    bot.send_message(chat_id=message.from_user.id, text=response)


print('ChatGPT Bot is working')

while True:
    try:
        bot.polling()
    except (telebot.apihelper.ApiException, ConnectionError) as e:
        logging.error(str(e))
        time.sleep(5)
        continue