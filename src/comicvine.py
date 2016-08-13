import sys
import Levenshtein
import datetime
import pymongo

def queryAll ( query ):
    client = pymongo.MongoClient("mongodb://mongo:27017")
    db = client.comics

    print("INFO: Querying", datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

    joined =  list(db.characters.find()) #roughly 108k elements
    joined += list(db.teams.find())      #roughly  60k elements
    joined += list(db.storyarcs.find())  #roughly  21k elements

    print("INFO: sorting", datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

    return sorted(joined, key=lambda k: (nameSort( query, k ), issueSort( k )))[:50]

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
        return 0 - character.get('count_of_issue_appearances')
    return 0

