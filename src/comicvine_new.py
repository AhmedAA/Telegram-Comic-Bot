import sys
import json
import requests
import redis
import Levenshtein
import datetime

def queryAll ( query ):
    names = getFromRedis( names )

    characters = sorted(names, key=lambda k: Levenshtein.distance( k, query ))

    result = []
    for character in characters[:49]:
        result.append( getFromRedis( character ))
    return result

def getFromRedis( charName ):
    r = redis.StrictRedis(host="redis", port=6379, db=0)
    retrieved = r.get(charName)
    if (not retrieved):
        return []
    print("INFO: Retreiving from Redis", datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    return json.loads( retrieved.decode('utf-8') )
