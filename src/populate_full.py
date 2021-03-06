import sys
import json
import requests
import time
import progressbar
from pymongo import MongoClient

from math import pow

with open(sys.argv[1]) as f:
    TOKEN = f.read().splitlines()[0]

mongoconn = "mongodb://objective-telegrambot-4069108:27017"

def request( resource, offset=0 ) :
    base = 'http://comicvine.gamespot.com/api/'+ resource +'/?api_key=' + TOKEN
    headers = {'User-Agent': 'telegram-bot'}
    params = {'format': 'json', 'offset': offset}

    for attempt in range(5):
        try:
            r = requests.get(url=base, params=params, headers=headers)
            return r
        except:
            print("sleeping, then trying again later")
            time.sleep(min(15, pow(2, attempt)) * 5) #5, 10, 20, 40, 75 secs
        else:
            break

print("CHARACTERS:")

r = request( 'characters' )
total = json.loads(r.text)['number_of_total_results']
offset = 0
bar = progressbar.ProgressBar(max_value=total)
while offset < total:
    r = request( 'characters',  offset)
    characters = json.loads(r.text)['results']
    offset += json.loads(r.text)['number_of_page_results']
    bar.update(offset)

    characters = [k
                for k
                in characters
                if k.get('description')    and len( k.get('description') ) > 2
                and k.get('publisher')
                and k.get('deck')          and len( k.get('deck') ) > 2
                and k.get('name')          and len( k.get('name') ) > 2
    ]

    for character in characters:
        character['_id'] = character.get('id')
        client = MongoClient(mongoconn)
        db = client.comics
        result = db.characters.insert_one( character)


print("TEAMS:")

r = request( 'teams' )
total = json.loads(r.text)['number_of_total_results']
offset = 0
bar = progressbar.ProgressBar(max_value=total)
while offset < total:
    r = request( 'teams',  offset)
    teams = json.loads(r.text)['results']
    offset += json.loads(r.text)['number_of_page_results']
    bar.update(offset)

    teams = [k
                for k
                in teams
                if k.get('description')    and len( k.get('description') ) > 2
                and k.get('publisher')
                and k.get('deck')          and len( k.get('deck') ) > 2
                and k.get('name')          and len( k.get('name') ) > 2
    ]

    for team in teams:
        team['_id'] = team.get('id')
        client = MongoClient(mongoconn)
        db = client.comics
        result = db.teams.insert_one( team)

print("STORY ARCS:")

r = request( 'story_arcs' )
total = json.loads(r.text)['number_of_total_results']
offset = 0
bar = progressbar.ProgressBar(max_value=total)
while offset < total:
    r = request( 'story_arcs',  offset)
    story_arcs = json.loads(r.text)['results']
    offset += json.loads(r.text)['number_of_page_results']
    bar.update(offset)

    story_arcs = [k
                for k
                in story_arcs
                if k.get('description')    and len( k.get('description') ) > 2
                and k.get('publisher')
                and k.get('deck')          and len( k.get('deck') ) > 2
                and k.get('name')          and len( k.get('name') ) > 2
    ]

    for story_arc in story_arcs:
        story_arc['_id'] = story_arc.get('id')
        client = MongoClient(mongoconn)
        db = client.comics
        result = db.storyarc.insert_one( story_arc)