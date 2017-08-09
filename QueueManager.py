from queue import Queue
import json
import os

jsonfile_name = 'linklist.json'

def list_init():
    link_queue = Queue()
    if os.path.isfile(jsonfile_name):
        link_list = json.load(open(jsonfile_name).read())
        for link in link_list:
            link_queue.put(link)
    else:
        link_queue.put('http://news.sohu.com/')
    return link_queue

def list_save(link_queue):
    link_list = []
    while True:
        try:
            link_list.append(link_queue.get_nowait())
        except:
            break
    print("now start saving queue list")
    json.dump(link_list, open(jsonfile_name, 'w'))
    print("saving queue list finished")