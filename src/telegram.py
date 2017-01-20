import sys
import telepot
import os
import time
import comicvine

from telepot.delegate import per_inline_from_id, create_open, pave_event_space

#############################################
#              Handler                      #
#############################################
class InlineHandler(telepot.helper.InlineUserHandler, telepot.helper.AnswererMixin):
    def __init__(self, *args, **kwargs):
        super(InlineHandler, self).__init__(*args, **kwargs)

    def on_inline_query(self, msg):
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        if len(query_string) < 3:
            return

        def compute_answer():
            count = 0
            articles = []
            for character in comicvine.queryAll(query_string)[:50]:
                try:
                    count += 1
                    article = {
                        'type': 'article',
                        'id': str(count),
                        'title': character['name'],
                        'thumb_url': character['image']['medium_url'],
                        'description': character['deck'][:199],
                        'input_message_content': {
                            'parse_mode': 'Markdown',
                            'message_text':
                                "[%s](%s)\n%s...\n[Checkout more here](%s)" % (
                                    character['name'],
                                    character['image']['medium_url'],
                                    character['deck'][:1000],
                                    character['site_detail_url'])
                            },
                        'url': character['site_detail_url']
                        }

                    articles.append( article );
                except:
                    next
            return articles

        self.answerer.answer(msg, compute_answer)

    def on_chosen_inline_result(self, msg):
        from pprint import pprint
        pprint(msg)
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
bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_inline_from_id(), create_open, InlineHandler, timeout=30),
])

# run forevs <3
bot.message_loop(run_forever='Listening ...')
