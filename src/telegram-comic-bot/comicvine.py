import sys
import json
import requests
from math import pow
from time import sleep

try:
    with open(sys.argv[2]) as f:
        TOKEN = f.read().splitlines()[0]
except Exception:
    print("Point me to a proper file!")

BASE = 'http://comicvine.gamespot.com/api/search/?api_key='+ TOKEN
HEADERS = {'User-Agent': 'telegram-bot'}

def __restCall (params):
    for attempt in range(5):
        try:
            r = requests.get(url=BASE, params=params, headers=HEADERS)
            return r
        except:
            sleep(min(15, pow(2, attempt)) * 5) #5, 10, 20, 40, 75 secs
        else:
            break

def queryAll ( charName ):
    params = {'format': 'json', 'limit': '50', 'query': charName}
    r = __restCall(params)

    print('PRINTING:')
    print(params)
    print(r.url)
    print(r.status_code)

    characters = json.loads(r.text)['results']

    # Remove unwanted results

    characters = [k
                  for k
                  in characters
                  if k.get('description') != ''
                  and k.get('publisher') != ''
                  and k.get('resource_type') != ''
                  and k.get('deck') != '']

    print(characters)

    #sort characters on name with levenstein

    #return characters
