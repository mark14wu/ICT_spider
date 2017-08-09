import json
import os

database_filename = 'data.json'

def init():
    client = MongoClient()
    page_db = client['webpages_db']
    pages = page_db['webpages']
    return client, page_db, pages

def save(content_list):
    if os.path.isfile(database_filename):
        old_list = json.load(open(database_filename))
    else:
        old_list = []
    print("now start saving data")
    old_list.extend(content_list)
    json.dump(old_list, open(database_filename, 'w'))
    print("saving data finished")