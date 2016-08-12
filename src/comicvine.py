import sys
import json
import requests
import Levenshtein
import datetime
import pymongo

def queryAll ( query ):
    client = pymongo.MongoClient("mongodb://mongo:27017")
    db = client.comics

    print("INFO: Querying", datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

    characters = db.characters.find()
    teams = db.teams.find()
    storyarcs = db.storyarcs.find()

    print("INFO: sorting", datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

    characters  = sorted(characters, key=lambda k: (characterNameSort( query, k ), issueSort( k )))
    teams       = sorted(teams, key=lambda k: (nameSort( query, k ), issueSort( k )))
    storyarcs   = sorted(storyarcs, key=lambda k: (nameSort( query, k ), issueSort( k )))

    print("INFO: returning", datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

    return characters[:10] + teams[:5] + storyarcs[:5] + characters[11:25] + teams[6:10] + storyarcs[6:10]

def characterNameSort( key, character ):
    length = Levenshtein.distance(key, character['name'])
    if character.get('real_name'):
        n = Levenshtein.distance(key, character['real_name'])
        length = n if n < length else length
    if character.get('aliases'):
        for alias in character['aliases'].split():
            n = Levenshtein.distance(key, alias)
            length = n if n < length else length
    if character.get('real_name'):
        for alias in character['real_name'].split():
            n = Levenshtein.distance(key, alias)
            length = n if n < length else length
    return length

def nameSort( key, character ):
    length = Levenshtein.distance(key, character['name'])
    if character.get('real_name'):
        n = Levenshtein.distance(key, character['real_name'])
        length = n if n < length else length
    if character.get('aliases'):
        for alias in character['aliases'].split():
            n = Levenshtein.distance(key, alias)
            length = n if n < length else length
    return length

def issueSort( character ):
    if (character.get('count_of_issue_appearances')):
        return 1 - character.get('count_of_issue_appearances')
    return 0