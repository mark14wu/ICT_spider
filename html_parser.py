# -*- coding: utf-8 -*-
import bs4
from bs4 import BeautifulSoup
import urllib.request
import sys
import os
from queue import Queue

# get the contents
# target_url = sys.argv[1]
link_list = Queue()
link_visited = {}
stoplist = ["javascript:void(0)"]
error_log = open("error.log", 'a')
website_list = ["sohu.com"]

def load_html(url):
    try:
        response = urllib.request.urlopen(url)
    except:
        print("error opening" + target_url)
        error_log.write(target_url + '\n')
        return None

    html = response.read()
    return html

def filtered_addtolist(link):
    if link not in stoplist and \
       link not in link_visited and \
       link[:4] == 'http':
            for website in website_list:
                if website in link:
                    #link_list.put(link)
                    print (link)
                    return

def parse_an_article(target_url=""):
#    html = load_html(target_url)
    link_visited[target_url] = True

    # this statement only for test
    html = open('test.html', encoding='utf8').read()
    # statement over

    soup = BeautifulSoup(html, 'html.parser')

    byte_title = soup.title.string.encode('utf8')
    articles = soup.find_all('article')
    article = articles[0]

    content = ""

    for string in article.strings:
        content += string

    for link in soup.find_all('a'):
        filtered_addtolist(link.get('href'))

    byte_content = content.encode('utf8')

parse_an_article()
error_log.close()
#sys.stdout.buffer.write(byte_content)
