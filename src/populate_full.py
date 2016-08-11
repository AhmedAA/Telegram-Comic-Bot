import sys
import json
import requests
import datetime
import redis

try:
    with open(sys.argv[2]) as f:
        TOKEN = f.read().splitlines()[0]
except Exception:
    print("Point me to a proper file!")

def request( resource ) :
    base = 'http://comicvine.gamespot.com/api/'+ resource +'/?api_key=' + TOKEN
    headers = {'User-Agent': 'telegram-bot'}
    params = {'format': 'json'}

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
characters = json.loads(r.text)['results']
characters = [k
            for k
            in characters
            if k.get('description')    and len( k.get('description') ) > 2
            and k.get('publisher')
            and k.get('deck')          and len( k.get('deck') ) > 2
            and k.get('name')          and len( k.get('name') ) > 2
]

for character in characters:
    r = redis.StrictRedis(host="redis", port=6379, db=0)
    print(character.get('name'), datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    r.set(character.get('name'), json.dumps(character))

print("TEAMS:")

r = request( 'teams' )
teams = json.loads(r.text)['results']
teams = [k
            for k
            in characters
            if k.get('description')    and len( k.get('description') ) > 2
            and k.get('publisher')
            and k.get('deck')          and len( k.get('deck') ) > 2
            and k.get('name')          and len( k.get('name') ) > 2
]

for team in teams:
    r = redis.StrictRedis(host="redis", port=6379, db=0)
    print(team.get('name'), datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    r.set(team.get('name'), json.dumps(teams))