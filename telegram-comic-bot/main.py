import telepot
import sys
import os
import time

from pprint import pprint

def on_chat_message(msg):
    pprint(msg)
    print(msg['from']['id'])
    bot.sendMessage(msg['from']['id'], "Stay a while, and listen!")

def on_inline_query(msg):
    print("inline herp derp")

def on_chosen_inline_result(msg):
    print("chosen inline herpderp")



###################
# token/bot setup #
###################
if len(sys.argv) < 2:
    print("Need a path to a file with a valid token!")
    sys.exit(0)

token_path = sys.argv[1]

try:
    with open(token_path) as f:
        TOKEN = f.read().splitlines()[0]
except Exception:
    print("Point me to a proper file!")

print(TOKEN)
# Initialise the bot
bot = telepot.Bot(TOKEN)

# What type of message do we have?
bot.message_loop({'chat': on_chat_message,
                  #'callback_query': on_callback_query,
                  'inline_query': on_inline_query,
                  'chosen_inline_result': on_chosen_inline_result})

print("Listening, shhhh")

# run forevs <3
while 1:
    time.sleep(10)
