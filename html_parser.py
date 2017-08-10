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
MAX_ITERATION = 10000

"""
class Webpage(object):
    def __init__(self, link, title, date, content):
        self.link = link
        self.b_title = title
        self.date = date
        self.b_content = content
"""

def space_to_dash(string):
    # print(string)
    new_string = []
    # string = string.split('')
    for char in string:
        if char == ' ':
            new_string.append('_')
        else:
            new_string.append(char)
    new_string = ''.join(new_string)
    return new_string

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
        html = response.read()
    except:
        print("error opening: " + url)
        error_log.write(url + '\n')
        error_log.close()
        return None

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
                     link_visited=isVisited.init()):
    target_url = link_queue.get()
    if target_url in link_visited or target_url in stoplist:
        return link_queue, link_visited
    # html = open('test.html', encoding='utf8').read()
    print(target_url)
    html = load_html(target_url)
    link_visited[target_url] = True

    try:
        soup = BeautifulSoup(html, 'html.parser')
    except:
        return link_queue, link_visited

    # get date
    date = None
    try:
        time_stamp = int(soup.find(id='news-time')['data-val'])/1000
        date = datetime.datetime.fromtimestamp(time_stamp)
        # time is scaled at seconds
    except:
        try:
            raw_date = soup.find(id='pubtime_baidu')['content']
            date = datetime.datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%S+08:00")
        except:
            try:
                raw_date = soup.find(id='pubtime_baidu').string
                date = datetime.datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S")
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
        try:
            descendants = article.descendants
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
        except:
            pass
    # parsing finished

    for raw_link in soup.find_all('a'):
        filtered_addtolist(raw_link.get('href'), link_queue, link_visited)

    page = Webpage(target_url, byte_title, date, byte_content)
    date_filename = space_to_dash(str(date))
    database.save(date_filename, byte_content)
    print(date_filename)
    return link_queue, link_visited


if __name__ == '__main__':
    while True:
        link_queue = QueueManager.list_init()
        link_visited = isVisited.init()
        for iter_count in tqdm(range(MAX_ITERATION)):
            link_queue, link_visited\
                = parse_an_article(link_queue, link_visited)
        print("now start saving")
        QueueManager.list_save(link_queue)
        isVisited.save(link_visited)
        print("saving complete")
        while True:
            user_input = input("continue?\n(y/n)")
            if user_input == 'y':
                break
            if user_input == 'n':
                exit(0)
