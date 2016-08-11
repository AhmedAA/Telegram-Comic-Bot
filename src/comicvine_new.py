import sys
import json
import requests
import Levenshtein
import datetime
import pymongo

def queryAll ( query ):
    client = pymongo.MongoClient("mongodb://mongo:27017")
    db = client.comics

    cursor = db.teams.find({"name": "Avengers"}).sort([
        ("name", pymongo.ASCENDING)
    ])

    for document in cursor:
        print(document)


    # names = getFromRedis( names )

    # characters = sorted(names, key=lambda k: Levenshtein.distance( k, query ))

    result = []
    # for character in characters[:49]:
    #     result.append( getFromRedis( character ))
    return cursor
