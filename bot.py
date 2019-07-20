#!/usr/bin/env python
import random

import requests
import telebot
from telebot import types
from telebot.types import Message
API_KEY = '3c8fb4cea87c794c8826e40711728821'
TOKEN = '955654661:AAF03ANN_nt2DCO3LaobM7kp5p1QdyVZbm4'
STICKER_ID = 'CAADAgADoAkAAnlc4gmdV_dExyul8wI'

bot = telebot.TeleBot(TOKEN)






@bot.message_handler(commands=['basla', 'komek'])
def command_handler(message: Message):
    bot.send_message(message.chat.id, "sikdir")



@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def hava_durumu(message):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&units=metric&APPID=3c8fb4cea87c794c8826e40711728821'

    json_data = requests.get(url).json()

    bot.reply_to(message, json_data['main']['temp'])

    return


@bot.message_handler(content_types=['sticker'])
def send_sticker(message: Message):
    bot.send_sticker(message.chat.id, STICKER_ID)

@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'Result', types.InputTextMessageContent('Result message.'))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)


bot.polling()
