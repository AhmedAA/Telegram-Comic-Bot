import telepot
import sys
import os
import time

def handle(msg):
    print("herpderp")




# token/bot setup
if len(sys.argv) < 2:
    print("Need a path to a file with a valid token!")
    sys.exit(0)

token_path = sys.argv[1]

try:
    with open(token_path) as f:
        TOKEN = f.read().splitlines()[0]
except Exception:
    print("Point me to a proper file!")

print(token)
bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print("Listening, shhhh")

while 1:
    time.sleep(10)
