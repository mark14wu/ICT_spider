import sys
from bs4 import BeautifulSoup
import urllib.request
import datetime
import json
import shelve
target_url = sys.argv[1]
html = urllib.request.urlopen(target_url).read()
soup = BeautifulSoup(html, 'html.parser')
# time_stamp = int(soup.find(id='news-time')['data-val'])/1000
# print(time_stamp)
# date = datetime.datetime.fromtimestamp(time_stamp)
raw_date = soup.find(id='pubtime_baidu').string
# date = datetime.datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%S+08:00")
date = datetime.datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S")
print(date)
# date = datetime.datetime.strptime("2017-08-08T22:32:43+08:00", "%Y-%m-%dT%H:%M:%S+08:00")
# print (str(date))
# byte_content = ""
# try:
#     article = soup.find('article')
#     for string in article.strings:
#         byte_content += string
#         # byte_content += '\n'
#     # byte_content = byte_content.encode('utf8')
# except:
#     article = soup.find(itemprop='articleBody')
#     for tag in article.descendants:
#         if tag.name == 'p':
#             # byte_content += tag.string
#             try:
#                 byte_content += tag.string
#             except:
#                 try:
#                     byte_content += tag.br.string
#                 except:
#                     pass
#             byte_content += '\n'
# json.dump(date.strftime(), open('test.json', 'w'))
# database_filename = 'database'
# dataKey = 'webpages_database'
# print("now start saving data")
# shelve.open(database_filename)[dataKey] = date
# print("saving data finished")
# print(date)
# print(byte_content)
