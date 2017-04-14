from urllib.parse import urlencode
import pymongo
import requests
from lxml.rtree import XMLSyntaxError
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq
from config import *

client = pymongo.MongoClient(MONGO_URL)
db = client(MONGO_DB)

base_url = 'http://weixin.sogou.com/weixin?'

headers = {
    'Cookie': 'CXID=98186070CBE49E8CEA5E6E713B507C68; SUV=009F178C78ECA36258AFE4C7C9718880; SEID=000000001527860A4311A6E800020AEB; ABTEST=0|1495091299|v1; JSESSIONID=aaaj87UqYU1IVhkBrOzWv; wuid=AAHZ0ADRGAAAAAqRGn3YJQAAAAA=; usid=AlVX4wYSLaRW_J7K; weixinIndexVisited=1; SUID=62A3EC784D6C860A581E0472000E81C0; ad=6lllllllll2YoMaXlllllV6uKiylllllWnh0Ykllll9lllllpqxlw@@@@@@@@@@@; SNUID=9C5E1186FEF8AD1985B28FA2FEC898A3; IPLOC=CN4401; sct=6'
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

proxy = None

def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def get_html(url, count=1):
    print('正在爬取', url)
    print('重试次数', count)
    global proxy
    if count >= MAX_COUNT:
        print('重试次数太多')
        return None
    try:
        if proxy:
            proxies = {
                'http': 'http://' + proxy
            }
            response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            # 代理
            print('触发 302，使用代理')
            proxy = get_proxy()
            if proxy:
                print('使用代理', proxy)
                return get_html(url)
            else:
                print('获取代理失败')
                return None
    except ConnectionError as e:
        print('错误信息', e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url, count)

def get_index(keyword, page):
    data = {
        'query': keyword,
        'type': 2,
        'page': page
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html

def parse_index(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('href')

def get_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def parse_detail(html):
    try:
        doc = pq(html)
        title = doc('.rich_media_title').text()
        content = doc('rich_media_content').text()
        date = doc('#post-date').text()
        nickname = doc('#js-profile_qrcode > div > strong').text()
        wechat = doc('#js-profile_qrcode > div > p:nth-child(3) > span').text()
        return {
            'title': title,
            'content': content,
            'date': date,
            'nickname': nickname,
            'wechat': wechat
        }
    except XMLSyntaxError:
        return None

def save_to_mongo(date):
    if db['articles'].update({'title': data['title']}, {'$set': data}, True):
        print('保存到 MongoDB：', data['title'])
    else:
        print('保存到 MongoDB 失败', data['title'])

def main():
    for page in range(1, 101):
        html = get_index(KEYWORD, page)
        if html:
            article_urls = parse_index(html)
            for article_url in article_urls:
                article_html = get_detail(article_url)
                if article_html:
                    article_data = parse_detail(article_html)
                    print(article_data)
                    if article_data:
                        save_to_mongo(article_data)

if __name__ == '__main__':
    main()
