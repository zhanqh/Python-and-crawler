import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

if __name__ == '__main__':
    # response = requests.get('http://toutiao.com/group/6425513144877449473/')
    # print(response.text)
    url = 'http://toutiao.com/group/6425513144877449473/'
    print(url[:7]+'www.'+url[7:])