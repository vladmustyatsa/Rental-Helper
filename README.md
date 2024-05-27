# Rental-Helper

Rental-Helper is a Telegram bot that was developed in March 2022 to make it easier to find an apartment in Western Ukraine.
Its programming code had to be written in a very short period, that's why the quality isn't the best. In the last commit(2024) some minor updates
were carried out to make the code look a bit nicer. Also, webhooks were added which were used to deploy the bot on Heroku in 2022, but weren't added to the repository at first.

The bot uses [dom.ria.com](https://dom.ria.com) as the source of rental advertisements. 

## Usage
In order to use Rental Helper, first of all, you need to create a virtual environment using ```virtualenv``` and install all dependencies from ```requirements.txt```

Then you need to configure the bot, use ```config.json``` for this:
```json
{
    "TOKEN" : "token-generated-by-BotFather",
    "WEBHOOK" : "http://...",
    "CITIES" : "city1_name;citi2_name",
    "DEVELOPING_MODE" : true/false
}
```
More in detail:
1. Create a bot using BotFather and paste the generated token into the corresponding field
2. Generate a webhook and paste it in ```config.json```, the easiest way is to use ```ngrok```
3. Enter cities which you want to monitor as it's shown above
4. Set ```DEVELOPING_MODE``` to ```true```
5. Start the bot:
   ```python
   python3 bot.py
   ```
After starting the bot on your device using the command ```/start```, you will be connected to Rental Helper and be able to get all new rental advertisements 
automatically without needing to make a request by hand.

## Some changes
Since 2022 _dom.ria.com_ has been changed, so Rental Helper(its parser module) is 
no longer compatible with the current version of _dom.ria.com_, but the main functionality still works and you can test it. 
In order to do that, you can use ```test.py``` — a small Flask app that just hosts a webpage similar to the version of _dom.ria.com_ from 2022(raw HTML without CSS, Javascript, 
and other things):
```python3
python3 test.py
```
```URL_TEMPLATE``` should be set to ```'http://localhost:8888/{}/{}'``` which is done by default in the last commit.```CITIES``` can be set to any string, it doesn't matter in this testing procedure.
To simulate the posting of new advertisements, you can delete(after the initial parsing) some link from ```flats.json```and wait a bit(set ```delay``` to a smaller number to wait less).
You should get a notification about the advertisement corresponding to the deleted link, which was perceived by the bot as newly posted.

## Using another source of advertisements
Rental Helper can be used to monitor any website with rental advertisements(from a technical point of view — any website with any content).
The only thing you have to change is its parser module(concretely ```get_all_flatlinks``` function), but its implicit input data type and output data type should remain
the same: it gets a string(name of a city), and returns a list of links of all rental advertisements found regarding this city(it would be a good idea to make the typing implicit using 
```typing``` module). 
Also, a different ```URL_TEMPLATE```
must be used according to the source of advertisements. For example, the appropriate ```URL_TEMPLATE``` for the version of _dom.ria.com_ from 2022 is commented in 
```config.py```.

## Deployment
To deploy Rental Helper, set ```DEVELOPING_MODE``` to ```false```. Then you can easily deploy it using e.g. Heroku. Don't forget to change the webhook to the one
provided by your hosting service.


