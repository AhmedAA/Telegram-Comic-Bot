import sys
import json
import requests
import redis
import Levenshtein
import datetime

from math import pow
from time import sleep

try:
    with open(sys.argv[2]) as f:
        TOKEN = f.read().splitlines()[0]
except Exception:
    print("Point me to a proper file!")

BASE = 'http://comicvine.gamespot.com/api/search/?api_key=' + TOKEN
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
        print("INFO: Calling ComicVine API", datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

        params = {'format': 'json', 'query': charName}
        r = __restCall(params)

        characters = json.loads(r.text)['results']

        characters = [k
                    for k
                    in characters
                    if k.get('description')    and len( k.get('description') ) > 2
                    and k.get('publisher')
                    and k.get('resource_type')
                    and k.get('deck')          and len( k.get('deck') ) > 2
                    and k.get('name')          and len( k.get('name') ) > 2

        ]
        putInRedis(charName, characters)

    #sort characters on name with levenshtein
    print("INFO: Sorting results", datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    characters = sorted(characters, key=lambda k: (characterNameSort( charName, k ), characterIssueSort( k )))

    print("INFO: Returning results", datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    return characters

def characterNameSort( key, character ):
    length = Levenshtein.distance(key, character['name'])
    if character.get('real_name'):
        n = Levenshtein.distance(key, character['real_name'])
        length = n if n < length else length
    if character.get('aliases'):
        for alias in character['aliases'].split():
            n = Levenshtein.distance(key, alias)
            length = n if n < length else length
    return length

def characterIssueSort( character ):
    if (character.get('count_of_issue_appearances')):
        return 1 - character.get('count_of_issue_appearances')
    return 0

def getFromRedis( charName ):
    r = redis.StrictRedis(host="redis", port=6379, db=0)
    retrieved = r.get(charName)
    if (not retrieved):
        return []
    print("INFO: Retreiving from Redis", datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    return json.loads( retrieved.decode('utf-8') )


def putInRedis( charName, jsonObject ):
    print("INFO: Inserting into Redis", datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    local = jsonObject
    r = redis.StrictRedis(host="redis", port=6379, db=0)
    r.set(charName, json.dumps(local))
