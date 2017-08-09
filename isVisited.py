import json
import os

visited_filename = 'visited.json'

def init():
    if os.path.isfile(visited_filename):
        visited = json.load(open(visited_filename))
    else:
        visited = {}
    return visited

def save(dict):
    print ("now starts saving visitied list")
    json.dump(dict, open(visited_filename, 'w'))
    print ("saving visitied list finished")