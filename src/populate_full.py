import sys
import json
import requests
import datetime
import redis

from math import pow
from time import sleep

try:
    with open(sys.argv[2]) as f:
        TOKEN = f.read().splitlines()[0]
except Exception:
    print("Point me to a proper file!")

def request( resource, offset=0 ) :
    base = 'http://comicvine.gamespot.com/api/'+ resource +'/?api_key=' + TOKEN
    headers = {'User-Agent': 'telegram-bot'}
    params = {'format': 'json', 'offset': offset}

    for attempt in range(5):
        try:
            r = requests.get(url=base, params=params, headers=headers)
            return r
        except:
            sleep(min(15, pow(2, attempt)) * 5) #5, 10, 20, 40, 75 secs
        else:
            break

print("CHARACTERS:")

r = request( 'characters' )
total = json.loads(r.text)['number_of_total_results']
offset = 0
names = []
while offset <= total:
    r = request( 'characters',  offset)
    characters = json.loads(r.text)['results']
    offset += json.loads(r.text)['number_of_page_results']
    print(len(characters), offset, total)

    characters = [k
                for k
                in characters
                if k.get('description')    and len( k.get('description') ) > 2
                and k.get('publisher')
                and k.get('deck')          and len( k.get('deck') ) > 2
                and k.get('name')          and len( k.get('name') ) > 2
    ]
    for character in characters:
        names.append(character.get('name'))
        r = redis.StrictRedis(host="redis", port=6379, db=0)
        r.set(character.get('name'), json.dumps(character))

print("TEAMS:")

r = request( 'teams' )
total = json.loads(r.text)['number_of_total_results']
offset = 0
while offset <= total:
    r = request( 'teams',  offset)
    teams = json.loads(r.text)['results']
    offset += json.loads(r.text)['number_of_page_results']
    print(len(teams), offset, total)

    teams = [k
                for k
                in teams
                if k.get('description')    and len( k.get('description') ) > 2
                and k.get('publisher')
                and k.get('deck')          and len( k.get('deck') ) > 2
                and k.get('name')          and len( k.get('name') ) > 2
    ]
    for team in teams:
        names.append(team.get('name'))
        r = redis.StrictRedis(host="redis", port=6379, db=0)
        r.set(team.get('name'), json.dumps(teams))

print("STORY ARCS:")

r = request( 'story_arcs' )
total = json.loads(r.text)['number_of_total_results']
offset = 0
while offset <= total:
    r = request( 'story_arcs',  offset)
    story_arcs = json.loads(r.text)['results']
    offset += json.loads(r.text)['number_of_page_results']
    print(len(story_arcs), offset, total)

    story_arcs = [k
                for k
                in story_arcs
                if k.get('description')    and len( k.get('description') ) > 2
                and k.get('publisher')
                and k.get('deck')          and len( k.get('deck') ) > 2
                and k.get('name')          and len( k.get('name') ) > 2
    ]
    for arc in story_arcs:
        names.append(arc.get('name'))
        r = redis.StrictRedis(host="redis", port=6379, db=0)
        r.set(arc.get('name'), json.dumps(story_arcs))


print(len(names))
r = redis.StrictRedis(host="redis", port=6379, db=0)
r.set('names', json.dumps(names))