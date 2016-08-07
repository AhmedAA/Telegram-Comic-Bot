import sys
import json
import requests
import comicvine

# Point to a txt file with hero names to query and populate DB with.
# In our case, it should be /misc/hero_list.txt

try:
    with open(sys.argv[1]) as f:
        names = f.read().splitlines()
except Exception:
    print("Point me to a proper file!")

print(names)

for character in names:
    comicvine.queryAll(character)
