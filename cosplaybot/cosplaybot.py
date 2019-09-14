#!/usr/bin/python

import telebot
import random
#import requests
from skimage import io
import cv2

API_TOKEN = 'your_bot_token_here'
list  = ["Канон","Не канон"]
bot = telebot.TeleBot(API_TOKEN)

choiceSaver = set()

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "hello there")

@bot.message_handler(content_types=['photo'])
def image_handler(message):
    file_id = message.photo[-1].file_id
    file_id_str = str(file_id)
    file_info = bot.get_file(file_id)
    image_url = 'https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path)
    #fileResponse = requests.get()
    #if(fileResponse.status_code != 200):
    #    return
    image = io.imread(image_url)
    if(image is None):
        return
    
    img_hash_str = image_hash_calculator(image)

    if(img_hash_str is None):
        return

    if(img_hash_str not in choiceSaver):
        choiceSaver.add(img_hash_str)
        bot.reply_to(message, random.choice(list))

def image_hash_calculator(image):
    measured_image_size = 128
    minimal_image_size = measured_image_size*2
    if(image.shape[0] < minimal_image_size or image.shape[1] < minimal_image_size):
        return None
    #r,g,b = cv2.split(image)
    #img_bgr = cv2.merge([b,g,r])
    monoimage = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    bluredimage = cv2.blur(monoimage, (32,32))
    miniimage = cv2.resize(bluredimage, (measured_image_size, measured_image_size), interpolation=cv2.INTER_AREA)
    cv2.imshow("ololo", miniimage)
    cv2.waitKey(0)
    t = cv2.img_hash_PHash.create()
    return str(t.compute(miniimage))

bot.polling()
