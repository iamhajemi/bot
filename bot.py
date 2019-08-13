#!/usr/bin/env python
import random
import time, re, telebot, random, csv
from PIL import Image, ImageDraw
from io import BytesIO
import shutil
import urllib
import requests
from telebot import types
import urllib.request, json
import lxml.html
import data

from gtts import gTTS
from telebot import types
import requests
import telebot
from telebot import types
from telebot.types import Message
API_KEY = '3c8fb4cea87c794c8826e40711728821'
TOKEN = '955654661:AAF03ANN_nt2DCO3LaobM7kp5p1QdyVZbm4'
STICKER_ID = 'CAADAgADoAkAAnlc4gmdV_dExyul8wI'
last_fm_api ='4e1e7afe67b798635f35f5338d0a2cf6'

url = 'http://api.apixu.com/v1/current.json?key=e3a09040c84c4ca3849123159190908&q='
bot = telebot.TeleBot(TOKEN)
counter =0

# Using the ReplyKeyboardMarkup class
# It's constructor can take the following optional arguments:
# - resize_keyboard: True/False (default False)
# - one_time_keyboard: True/False (default False)
# - selective: True/False (default False)
# - row_width: integer (default 3)
# row_width is used in combination with the add() function.
# It defines how many buttons are fit on each row before continuing on the next row.

suallar = ['Turkiyenin paytaxti hansi seherdir?',"Azerbaycanin paytaxti ahnsi seherdir",'Islandiyanin paytaxti hansi sherdir']
cavablar = [['Ankara','Istanbul','Izmir','Antalya'],['Ankara','Baku','Izmir','Antalya'],['Ankara','Istanbul','Reykyavik','Antalya'],]
duzguncavablar = [0,1,2]

def sual_counter(message):
    global counter

    counter += 1


def sual_duzelt(message,sual,a,b,c,d):
    global counter
    reply_variant = types.ReplyKeyboardMarkup(True, True)
    reply_variant.row(a, b)
    reply_variant.row(c, d)
    bot.send_message(message.chat.id, sual, reply_markup=reply_variant)

    sual_counter(message)




def cavab_dal():
    cavab = types.ReplyKeyboardMarkup(True, True)
    cavab.row('basla', 'dala qayit')
    return cavab



@bot.message_handler(commands=['start'])
def send_welcome(message):
    cavab = types.ReplyKeyboardMarkup(True, True)
    cavab.row('basla', 'dala qayit')
    bot.send_message(message.chat.id, "Sual Cavab oyununa xos gelmisiz.Oyuna baslamaq ucun baslaya basin",
                     reply_markup=cavab)
    @bot.message_handler(content_types=['text'])
    def sual_ver(message):
        global counter

        if message.text == 'basla' and counter == 0:
            sual_duzelt(message,suallar[counter],cavablar[counter][0],cavablar[counter][1],cavablar[counter][2],cavablar[counter][3])



        elif message.text == cavablar[counter-1][duzguncavablar[counter-1]] and counter !=0:
            print(counter)
            if counter < len(suallar):
                sual_duzelt(message, suallar[counter], cavablar[counter][0], cavablar[counter][1], cavablar[counter][2],
                        cavablar[counter][3])
            elif  counter == len(suallar):
                bot.send_message(message.chat.id, 'Tebrikler qalib geldiniz\nYeniden oynamaq ucun baslaya basin', reply_markup=cavab_dal())
                counter=0
        elif message.text != cavablar[counter-1][duzguncavablar[counter-1]] and counter !=0:
            bot.send_message(message.chat.id,'Teessuf ki meglub oldunuz.\nYeniden baslamaq ucun baslaya basin', reply_markup=cavab_dal())
            counter = 0





@bot.message_handler(commands=['weather'])
def hava_gonder(message):
    a = message.text.split()
    print(a)
    res = requests.get(url+a[1])
    jsondata= res.json()
    print(jsondata)
    bot.send_message(message.chat.id, jsondata['current']["temp_c"])


@bot.message_handler(commands=['it'])
def itsekiligonder(message):
    url = 'https://random.dog/woof.json'
    request = requests.get(url).json()
    dog_url = request['url']
    print(dog_url)
    bot.send_photo(message.chat.id, dog_url)

@bot.message_handler(commands=['ses'])
def sese_cevir(message):
    mesaj = message.text
    mesaj=mesaj[5::]
    print(mesaj)
    tts = gTTS(mesaj, lang='tr')
    tts.save('hello.mp3')
    audio = open('$HOME/hello.mp3', 'rb')
    bot.send_audio(message.chat.id, audio)



@bot.message_handler(commands=['lastfm'])
def albom_tap(message):
    mesaj = message.text
    mesaj=mesaj[8::]
    print(mesaj)
    url = f'http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist={mesaj}&api_key={last_fm_api}&format=json'
    albumname = []
    res = requests.get(url).json()
    for album in res['topalbums']['album']:
        albumname.append(album['image'][3]['#text'])
    print(albumname)

    for albumsekili in albumname:
        if albumsekili != '':
            bot.send_message(message.chat.id, albumsekili)
        print(len(albumname))


@bot.message_handler(commands=['news'])
def xeberler(message):
    url = ('https://newsapi.org/v2/top-headlines?'
           'country=tr&'
           'apiKey=3f235d2b44d14f088ab584eb399e2c73')
    response = requests.get(url).json()
    titles = ''
    for title in response['articles']:
        time.sleep(5)
        bot.send_message(message.chat.id, title['title'] + '\n'+ title['url'])





@bot.message_handler(commands=['test'])
def xeberler(message):
    bot.send_message(message.chat.id, "salamun alaykum")



# @bot.message_handler(commands=['porngif'])
# def send_photo(message):
# 	arg = message.text.split(" ")
# 	resource = urllib.request.urlopen("http://www.gifporntube.com/gifs/"+str(arg[1])+".html")
# 	content =  resource.read().decode(resource.headers.get_content_charset())
# 	urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+([/a-z_0-9]*.mp4)', content)
# 	print("http://www.gifporntube.com"+urls[0]+ "  arg:"+str(arg[1]))
# 	markdown = "[.](http://www.gifporntube.com"+str(urls[0])+")"
# 	bot.send_message(message.chat.id, markdown, parse_mode="Markdown")


#@bot.message_handler(func = lambda message: True)
# def send_welcome(message: Message):
#     global counter
#     if message.from_user.username == 'nullzeronull':
# 	    bot.reply_to(message, "sen ureysen")
#     elif message.from_user.username == 'h12345678980' and counter==0:
#         bot.reply_to(message, 'Salam' + " " + message.from_user.first_name + " Sen sox icive bir deyqe soz verende danisarsan it")
#         counter +=1
#     elif counter == 1:
#         bot.reply_to(message, 'ala get sikdir')
#         counter += 1
#     elif counter==2:
#         bot.reply_to(message, 'cavab vermeyecem sene uje')
#     if message.text == 'bagisla':
#         bot.reply_to(message,"yaxsi barisdiq")
#         counter=0





#Salamlar




bot.polling()


