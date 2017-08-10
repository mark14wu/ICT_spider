import sys
from bs4 import BeautifulSoup
import urllib.request
import datetime
target_url = sys.argv[1]
html = urllib.request.urlopen(target_url).read()
soup = BeautifulSoup(html, 'html.parser')

# raw_date = soup.find(id='pubtime_baidu')['content']
# date = datetime.datetime.strptime("2017-08-08T22:32:43+08:00", "%Y-%m-%dT%H:%M:%S+08:00")

byte_content = ""
try:
    article = soup.find('article')
    for string in article.strings:
        byte_content += string
        # byte_content += '\n'
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
            # byte_content += '\n'

# print(date)
print(byte_content)

# sys.stdout.buffer.write(byte_content.encod)
