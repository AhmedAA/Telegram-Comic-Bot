import sys
import asyncio
import telepot
import os
import time
import comicvine

from telepot.delegate import per_inline_from_id, create_open

from pprint import pprint

#############################################
#              Handler                      #
#############################################
class InlineHandler(telepot.helper.UserHandler):
    def __init__(self, seed_tuple, timeout):
        super(InlineHandler, self).__init__(seed_tuple, timeout, flavors=['inline_query', 'chosen_inline_result'])
        self._answerer = telepot.helper.Answerer(self.bot)

    def on_inline_query(self, msg):
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        print(self.id, ':', 'Inline Query:', query_id, from_id, query_string)

        def compute_answer():
            count = 0
            articles = []
            characters =  comicvine.queryAll( query_string )
            for character in characters[:50]:
                try:
                    count += 1
                    article = {
                        'type': 'article',
                        'id': str(count),
                        'title': character['name'],
                        'thumb_url': character['image']['medium_url'],
                        'description': character['deck'][:199],
                        'parse_mode': 'Markdown',
                        'message_text': character['deck'][:450],
                            # "[#{character['name']}](#{character['image']['medium_url']})\n" \
                            # "#{character['deck'][0, 450][0..-2]}...\n" \
                            # "[Checkout more here](#{character['site_detail_url']})",
                        }

                    articles.append( article );
                except:
                    next
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
bot = telepot.DelegatorBot(TOKEN, [(
    per_inline_from_id(),
    create_open(InlineHandler,
                timeout=10))
                ])

print('Listening, shhhh')

# run forevs <3
bot.message_loop(run_forever=True)
