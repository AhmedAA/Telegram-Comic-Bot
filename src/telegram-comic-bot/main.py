import sys
import asyncio
import telepot
import os
import time
import comicvine
from telepot.async.delegate import per_inline_from_id, create_open

from pprint import pprint

#############################################
#              Handler                      #
#############################################
class InlineHandler(telepot.async.helper.InlineUserHandler):
    def __init__(self, seed_tuple, timeout):
        super(InlineHandler, self).__init__(seed_tuple, timeout)
        self._answerer = telepot.async.helper.Answerer(self.bot)

    def on_inline_query(self, msg):
        def compute_answer():
            query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
            print(self.id, ':', 'Inline Query:', query_id, from_id, query_string)

            articles = [{'type': 'article',
                             'id': 'abc', 'title': query_string, 'message_text': query_string}]

            return articles

        self._answerer.answer(msg, compute_answer)

    def on_chosen_inline_result(self, msg):
        result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
        print(self.id, ':', 'Chosen Inline Result:', result_id, from_id, query_string)


#############################################
#              token/bot setup              #
#############################################
if len(sys.argv) < 3:
    print("Need a path to a file with valid tokens!")
    sys.exit(0)

token_path = sys.argv[1]

try:
    with open(token_path) as f:
        TOKEN = f.read().splitlines()[0]
except Exception:
    print("Point me to a proper file!")

print(TOKEN)
# Initialise the bot
bot = telepot.async.DelegatorBot(TOKEN, [(
    per_inline_from_id(),
    create_open(InlineHandler, timeout=10),
)])
loop = asyncio.get_event_loop()

loop.create_task(bot.message_loop())
print('Listening, shhhh')

# run forevs <3
loop.run_forever()
