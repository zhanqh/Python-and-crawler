from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

def news(url, n = None):
    f = open('news.txt', 'w')

    news = urlopen(url)
    newsObj = BeautifulSoup(news.read(), "html.parser")
    newsList = newsObj.find('div', {'class': 'c_news'}).findAll('a')
    f.write('☆ 第1页 ☆\n')
    for new in newsList:
        f.write(new.get_text() + ' ☛ ' + re.findall('[0-9]{8}', new.attrs['href'])[0] + '\n')
    pagesList = newsObj.find('div', {'class': 'listpages'}).findAll('a')

    m = 1
    while True:
        m = m + 1
        if n != None:
            if m > n:
                print('break')
                break
        if int(re.findall('[0-9]+', pagesList[-1].attrs['href'])[0]) - 1 == int(re.findall('[0-9]+', pagesList[-2].attrs['href'])[0]):
            print('done')
            break
        news = urlopen('http://em.scnu.edu.cn' + pagesList[-1].attrs['href'])
        newsObj = BeautifulSoup(news.read(), "html.parser")
        newsList = newsObj.find('div', {'class': 'c_news'}).findAll('a')
        f.write('\n☆ 第' + str(m) + '页 ☆\n')
        for new in newsList:
            f.write(new.get_text() + ' ☛ ' + re.findall('[0-9]{8}', new.attrs['href'])[0] + '\n')
        pagesList = newsObj.find('div', {'class': 'listpages'}).findAll('a')

    f.close()


# f = open('news.txt', 'w')

# news = urlopen('http://em.scnu.edu.cn/xueyuanxinwen/index.html')
# newsObj = BeautifulSoup(news.read(), "html.parser")

# newsList = newsObj.find('div', {'class': 'c_news'}).findAll('a')
# f.write('☆ 第1页 ☆\n')
# for new in newsList:
#     f.write(new.get_text() + ' ☛ ' + re.findall('[0-9]{8}', new.attrs['href'])[0] + '\n')

# pagesList = newsObj.find('div', {'class': 'listpages'}).findAll('a')

# m = 0
# while True:
#     m = m + 1
#     if m > 3:
#         print('break')
#         break
#     if int(re.findall('[0-9]+', pagesList[-1].attrs['href'])[0]) - 1 == int(re.findall('[0-9]+', pagesList[-2].attrs['href'])[0]):
#         print('done')
#         break
#     news = urlopen('http://em.scnu.edu.cn' + pagesList[-1].attrs['href'])
#     newsObj = BeautifulSoup(news.read(), "html.parser")
#     newsList = newsObj.find('div', {'class': 'c_news'}).findAll('a')
#     f.write('\n☆ 第' + str(n + 1) + '页 ☆\n')
#     for new in newsList:
#         f.write(new.get_text() + ' ☛ ' + re.findall('[0-9]{8}', new.attrs['href'])[0] + '\n')
#     pagesList = newsObj.find('div', {'class': 'listpages'}).findAll('a')

# f.close()
