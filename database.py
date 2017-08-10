import shelve
import os

database_filename = 'database'
dataKey = 'webpages_database'

def save(name, content):
    # if os.path.isfile(database_filename):
    #     old_list = shelve.open(database_filename)[dataKey]
    # else:
    #     old_list = []
    # print("now start saving data")
    # old_list.extend(content_list)
    # # json.dump(old_list, open(database_filename, 'w'))
    # shelve.open(database_filename)[dataKey] = old_list
    # print("saving data finished")
    dir_name = 'contents/'
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    if name is None:
        return
    if content == "":
        return
    file = shelve.open(dir_name + name, flag='c')
    file[dataKey] = content
    file.close()