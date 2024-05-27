import os
import telebot
import threading
import json
from time import sleep
from loguru import logger
from flask import Flask, request
from config import TOKEN, CITIES, DEVELOPING_MODE, WEBHOOK
from rental_parser import get_all_flatlinks

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
delay = 60  # in seconds


@bot.message_handler(commands=['start'])
def start_message(message): 
    # Check if a user has already connected to the bot
    id = message.from_user.id
    with open('ids.json', 'r') as file:
        ids = json.load(file)
    
    '''
    Save UserID in order to be able to send new announcements to them automatically
    '''
    if id not in ids: 
        ids.append(id)
        with open('ids.json', 'w') as file:
            json.dump(ids, file)
        logger.debug('New user has joined!')
        bot.send_message(id, 'Hi!\nUse /ping to check if I am working')

@bot.message_handler(commands=['ping'])
def ping(message):
    bot.send_message(message.from_user.id, "I'm here!")

def check_website():
    '''
    A function that looks for new announcements, send them to users and save them
    '''
    sleep(10)
    logger.info('Started checking...')
    while True:
        try:
            with open('flats.json', 'r') as file:
                saved_links = json.load(file)
            with open('ids.json', 'r') as file:
                ids = json.load(file)

            for city in CITIES:
                logger.info(f'Getting all {city.upper()} flatlinks...')
                all_city_links = get_all_flatlinks(city)
                logger.info(f'Got it!')

                if set(all_city_links) - set(saved_links.get(city, [])):
                    logger.info(f'New link(s) found')
                    new_links = list(set(all_city_links) - set(saved_links.get(city, [])))

                    
                    for id in ids:
                        bot.send_message(id, f'New available flat(s) in {city.capitalize()}!')
                        for link in new_links:
                            bot.send_message(id, link)

                    updated_links = saved_links.copy()
                    updated_links[city] = all_city_links
                    with open('flats.json', 'w') as file:
                        json.dump(updated_links, file)
                    logger.info('Recorded to flats.json')
                else:
                    logger.info('No new link was found')
                
            sleep(delay)
        except BaseException as e:
            logger.error(e)




@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    logger.info('Request to bot arrived')
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200



bot.remove_webhook()
sleep(5)


if WEBHOOK[-1] != '/':
    bot.set_webhook(url=WEBHOOK +'/'+ TOKEN)
else:
    bot.set_webhook(url=WEBHOOK + TOKEN)


# Create a thread to look for new announcements continuously 
t = threading.Thread(target=check_website)
t.start()

if __name__ == "__main__":
    if DEVELOPING_MODE:
        logger.info('DEVELOPING MODE is on')
    logger.info('Starting server...')
    server.run(host='127.0.0.1' if DEVELOPING_MODE else '0.0.0.0', port=int(os.environ.get('PORT', 5000)))

