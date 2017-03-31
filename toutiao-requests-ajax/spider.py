import json
import re
from urllib.parse import urlencode
from json.decoder import JSONDecodeError
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import requests
from config import *
import pymongo
import os
from hashlib import md5
from multiprocessing import Pool

# connect=False 为关闭多进程报 warning
client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]

def get_page_index(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 3
    }
    url = 'http://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错')
        return None

def parse_page_index(html):
    try:
        data = json.loads(html)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('article_url')
    except JSONDecodeError:
        pass

def get_page_detail(url):
    try:
        # 若不加 www 前缀子域会产生重定向错误
        response = requests.get(url[:7]+'www.'+url[7:])
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as e:
        print('请求详情页出错', url)
        print(e)
        return None

def parse_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    # print(title)
    images_pattern = re.compile('var gallery = (.*?);',re.S)
    result = re.search(images_pattern, html)
    if result:
        try:
            data = json.loads(result.group(1))
            if data and 'sub_images' in data.keys():
                sub_images = data.get('sub_images')
                images = [item.get('url') for item in sub_images]
                for image in images:
                    download_image(image)
                return {
                    'title': title,
                    'url': url,
                    'image': images
                }
        except JSONDecodeError:
            pass

def download_image(url):
    print('Downloading', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except ConnectionError:
        return None

def save_image(content):
    # 对图像文件进行 md5 取直作为文件名，防止重复存储图像
    file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
    print(file_path)
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()

def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('写入 mongodb 数据库成功', result)
        return True
    return False

def main(offset):
    html = get_page_index(offset, KEYWORD)
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html, url)
            if result: save_to_mongo(result)


if __name__ == '__main__':
    # main()
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()