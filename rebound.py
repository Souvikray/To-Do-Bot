import requests
import json
import time
import urllib

# token provided by Telegram
TOKEN = "47*******:***********************************"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode('utf8')
    return content

# get JSON from URL
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

# acknowledge every message received by the bot
def get_updates(offset=None):
    # initiate a new check every 100 seconds
    url = URL + "getUpdates?timeout=100"
    # url = URL + "getUpdates"
    if offset:
        url += "&offset={}".format(offset)
        # url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    # returns the highest id which is the latest update id
    return max(update_ids)

# echo all the messages received by the bot to the user
def echo_all(updates):
    # loop through the 'result' list
    for update in updates["result"]:
        try:
            # get the text
            text = update["message"]["text"]
            # get the chat id
            chat = update["message"]["chat"]["id"]
            send_message(text,chat)
        except Exception as e:
            print(e)

'''
#get the last chat id and the text sent to the bot
def get_last_chat_id_and_text(updates):
    no_of_updates = len(updates["result"])
    last_update = no_of_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text,chat_id)
'''

#send message to the user
def send_message(text,chat_id):
    #encodes special characters like +,& since they have special meanings in the context of URL's
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text,chat_id)
    get_url(url)

def main():
    #before the conversation begins
    last_update_id = None
    while True:
        print("Getting updates")
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            #we are telling telegram which id we are expecting and not which id we have seen
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()

