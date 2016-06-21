import sys
import json
import requests
from math import pow
from time import sleep

try:
    with open(sys.argv[2]) as f:
        TOKEN = f.read().splitlines()[0]
except Exception:
    print("Point me to a proper file!")

BASE = 'http://api.comicvine.com/search/?api_key='+ TOKEN +'&format=json'

def __restCall (url):
    for attempt in range(5):
        try:
            r = requests.get(url)
            return r
        except:
            sleep(min(15, pow(2, attempt)) * 5) #5, 10, 20, 40, 75 secs
        else:
            break

def queryAll ( charName ):
    url = BASE + "&query="+ charName +"&limit=50"
    r = __restcall(url)
    characters = json.loads(r.json())

    #sort characters on name with levenstein

    return characters
