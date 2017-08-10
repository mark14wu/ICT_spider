# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import datetime
import QueueManager
import isVisited
import database
from tqdm import tqdm

stoplist = ["javascript:void(0)"]
website_list = ["news.sohu.com"]
MAX_ITERATION = 1000

"""
class Webpage(object):
    def __init__(self, link, title, date, content):
        self.link = link
        self.b_title = title
        self.date = date
        self.b_content = content
"""


def Webpage(link, byte_title, date, byte_content):
    page = {}
    page['link'] = link
    page['byte_title'] = byte_title
    page['date'] = date
    page['byte_content'] = byte_content
    return page


def load_html(url):
    error_log = open("error.log", 'a')
    try:
        response = urllib.request.urlopen(url)
    except:
        print("error opening: " + url)
        error_log.write(url + '\n')
        error_log.close()
        return None

    html = response.read()
    error_log.close()
    return html


# this"fil...add..." function is under construction!
def filtered_addtolist(link, link_queue, link_visited):
    try:
        http_flag = (link[:4] == 'http')
    except:
        http_flag = False
    if link not in stoplist and \
                    link not in link_visited and \
            http_flag:
        for website in website_list:
            if website in link:
                link_queue.put(link)
                # print (link)
                return


def parse_an_article(link_queue=QueueManager.list_init(),
                     link_visited=isVisited.init(),
                     content_list=[]):
    target_url = link_queue.get()
    # html = open('test.html', encoding='utf8').read()
    html = load_html(target_url)
    link_visited[target_url] = True

    try:
        soup = BeautifulSoup(html, 'html.parser')
    except:
        return link_queue, link_visited, content_list

    # get date
    date = None
    try:
        time_stamp = soup.find(id='news-time')['data-val']/1000
        date = datetime.datetime.fromtimestamp(time_stamp)
        # time is scaled at seconds
    except:
        try:
            raw_date = soup.find(id='pubtime_baidu')['content']
            date = datetime.datetime.strptime("2017-08-08T22:32:43+08:00", "%Y-%m-%dT%H:%M:%S+08:00")
        except:
            pass
    byte_title = soup.title.string

    # now parsing the body part
    byte_content = ""
    try:
        article = soup.find('article')
        for string in article.strings:
            byte_content += string
        # byte_content = byte_content.encode('utf8')
    except:
        article = soup.find(itemprop='articleBody')
        for tag in article.descendants:
            if tag.name == 'p':
                # byte_content += tag.string
                try:
                    byte_content += tag.string
                except:
                    try:
                        byte_content += tag.br.string
                    except:
                        pass
                byte_content += '\n'
    # parsing finished

    for raw_link in soup.find_all('a'):
        filtered_addtolist(raw_link.get('href'), link_queue, link_visited)

    page = Webpage(target_url, byte_title, date, byte_content)
    content_list.append(page)
    return link_queue, link_visited, content_list


if __name__ == '__main__':
    link_queue = QueueManager.list_init()
    link_visited = isVisited.init()
    content_list = []
    while True:
        for iter_count in tqdm(range(MAX_ITERATION)):
            link_queue, link_visited, content_list \
                = parse_an_article(link_queue, link_visited, content_list)
        print("now start saving")
        QueueManager.list_save(link_queue)
        isVisited.save(link_visited)
        database.save(content_list)
        print("saving complete")
        while True:
            user_input = input("continue?\n(y/n)")
            if user_input == 'y':
                break
            if user_input == 'n':
                exit(0)
