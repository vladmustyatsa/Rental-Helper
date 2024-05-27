import json

with open('config.json', 'r') as file:
    parameters = json.load(file)
    TOKEN = parameters["TOKEN"]
    CITIES = parameters["CITIES"].split(';')
    DEVELOPING_MODE = parameters["DEVELOPING_MODE"]
    WEBHOOK = parameters["WEBHOOK"] 

#URL_TEMPLATE = 'https://dom.ria.com/uk/arenda-kvartir/{}/?page={}'
# Use url template below to test the bot
URL_TEMPLATE = 'http://localhost:8888/{}/{}' 
