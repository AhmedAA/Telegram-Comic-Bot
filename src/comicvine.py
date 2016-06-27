import sys
import json
import requests
import redis
import Levenshtein

from math import pow
from time import sleep

try:
    with open(sys.argv[2]) as f:
        TOKEN = f.read().splitlines()[0]
    ip = sys.argv[3]
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
    characters = getFromRedis(charName)
    if not (characters):

        params = {'format': 'json', 'query': charName}
        r = __restCall(params)

        # print('PRINTING:')
        # print(params)
        # print(r.url)
        # print(r.status_code)

        characters = json.loads(r.text)['results']

        characters = [k
                    for k
                    in characters
                    if k.get('description')    and len( k.get('description') ) > 2
                    and k.get('publisher')     and len( k.get('publisher') ) > 2
                    and k.get('resource_type') and len( k.get('resource_type') ) > 2
                    and k.get('deck')          and len( k.get('deck') ) > 2
                    and k.get('name')          and len( k.get('name') ) > 2
        ]

        #sort characters on name with levenshtein
        characters = sorted(characters, key=lambda k: Levenshtein.distance(charName, k['name']))

        putInRedis(charName, characters)
    #print(type(characters))
    return characters

def getFromRedis( charName ):
    r = redis.StrictRedis(host=ip, port=6379, db=0)
    retrieved = r.get(charName)
    if (not retrieved):
        return []
    print("Retreiving from Redis")
    return json.loads( retrieved.decode('utf-8') )


def putInRedis( charName, jsonObject ):
    print("Inserting into Redis")
    local = jsonObject
    r = redis.StrictRedis(host=ip, port=6379, db=0)
    r.set(charName, json.dumps(local))
