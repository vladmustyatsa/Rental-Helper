import telebot
import threading
import json
from time import sleep
from loguru import logger
from config import TOKEN
from parser import get_all_flatlinks

bot = telebot.TeleBot(TOKEN)
delay = 30  # in seconds



@bot.message_handler(commands=['start'])
def start_message(message): 

    id = message.from_user.id
    with open('ids.json', 'r') as file:
        ids = json.load(file)
    
    if id not in ids:
        ids.append(id)
        with open('ids.json', 'w') as file:
            json.dump(ids, file)
        logger.debug('New user has joined!')
        bot.send_message(id, 'Hi!\nUse /ping to check if I work')

@bot.message_handler(commands=['ping'])
def ping(message):
    bot.send_message(message.from_user.id, "I'm here!")

def check_website():
    logger.debug('Started checking...')
    while True:
        logger.debug('Getting all flatlinks...')
        all_links = get_all_flatlinks()
        logger.debug('Got it!')
        #print(all_links)
        with open('flats.json', 'r') as file:
            saved_links = json.load(file)
        if set(all_links) - set(saved_links):
            logger.debug(f'New link(s) found')
            new_links = list(set(all_links) - set(saved_links))
            #logger.debug(new_links)
            with open('flats.json', 'w') as file:
                json.dump(all_links, file)
            logger.debug('Writed to flats.json from all_links')
            with open('ids.json', 'r') as file:
                ids = json.load(file)
            for id in ids:
                bot.send_message(id, 'New available flat(s)!')
                for link in new_links:
                    bot.send_message(id, link)
        else:
            with open('flats.json', 'w') as file:
                json.dump(all_links, file)
            logger.debug('No link found')

        sleep(delay)


t = threading.Thread(target=check_website)
t.start()

while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except:
        sleep(10)