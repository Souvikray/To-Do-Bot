import requests
import json
import time
import urllib
from DatabaseWork import BotDB

#instantiate the BotDB class to use its methods
db = BotDB()
# token provided by Telegram
TOKEN = "47*******:***********************************"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

# get response from URL
def get_url(url):
    response = requests.get(url)
    content = response.content.decode('utf8')
    return content

# get JSON from URL
def get_json_from_url(url):
    content = get_url(url)
    # load JSON from string
    js = json.loads(content)
    return js

# acknowledge every message received by the bot
def get_updates(offset=None):
    # initiate a new check every 100 seconds
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    ## returns the highest id which is the latest update id
    return max(update_ids)

def handle_updates(updates):
    # loop through the 'result' list
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            # send text to respective users using chat id
            chat = update["message"]["chat"]["id"]
            # get the items list for a particular user
            items = db.get_items(chat)
            if text == "/done":
                # construct the keyboard containing the items
                keyboard = construct_keyboard(items)
                # ask user what item they want to delete and pass the keyboard
                send_message("Select an item you want to delete",chat,keyboard)
            #start the conversation with a little tutorial
            elif text == "/start":
                send_message("Welcome!I am your personal to-do reminder!Add work that you want me to store."
                             "When you complete a work,type '/done' to delete the work or works.",chat)
            # ensure commands are not treated as items and added to the list
            elif text.startswith("/"):
                continue
            elif text in items:
                # the user signals the bot that the particular work is done
                db.delete_item(text,chat)
                items = db.get_items(chat)
                keyboard = construct_keyboard(items)
                # give the user an option to delete multiple items if they want to
                send_message("Item deleted\nSelect if you want to delete another item",chat,keyboard)
            else:
                # add item to the list along with chat id
                db.add_item(text,chat)
                items = db.get_items(chat)
            # display each item in a new line
            message = "\n".join(items)
            send_message(message,chat)
        except KeyError:
            pass

def construct_keyboard(items):
    # we create a keyboard which has one item as button per row
    keyboard = [[item] for item in items]
    # we create a dictionary where we pass keyboard as value to "keyboard" and ensure it only appears once per operation
    reply_markup = {"keyboard":keyboard,"one_time_keyboard":True}
    # we turn the JSON into a string as this is the format Telegram expects
    return json.dumps(reply_markup)

#send message to the user
def send_message(text,chat_id,reply_markup=None):
    # encodes special characters like +,& since they have special meanings in the context of URL's
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text,chat_id)
    # if there are items in the keyboard (in other words if there are items in the list)
    if reply_markup:
        # we pass an additonal argument to the URL that involves passing the keyboard
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

def main():
    # connect to the table containing items
    db.setup()
    # before the conversation begins
    last_update_id = None
    while True:
        # print("Getting updates")
        updates = get_updates(last_update_id)
        # if a conversation has been initiated between bot and user otherwise 'result' will be an empty list
        if len(updates["result"]) > 0:
            # we are telling telegram which id we are expecting and not which id we have seen
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        # the loop will run every 0.5 seconds to save on resource consumption
        time.sleep(0.5)

if __name__ == '__main__':
    main()

