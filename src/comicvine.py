import sys
import datetime
import pymongo
import difflib

mongoconn = "mongodb://objective-telegrambot-4069108:27017"
def queryAll ( query ):
    client = pymongo.MongoClient(mongoconn)
    db = client.comics

    print("INFO: CV querying", datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

    joined =  list(db.characters.find()) #roughly 108k elements
    joined += list(db.teams.find())      #roughly  60k elements
    joined += list(db.storyarcs.find())  #roughly  21k elements

    print("INFO: CV sorting", datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    
    result = difflib.get_close_matches(query, joined, n=50, cutoff=0.6)
    
    print("INFO: CV finished", datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

    return result

def sortByName( needle, haystack):
    return []