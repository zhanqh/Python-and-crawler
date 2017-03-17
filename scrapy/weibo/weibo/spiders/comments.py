# -*- coding: utf-8 -*-
import scrapy
import json
from weibo.items import WeiboItem

class CommentsSpider(scrapy.Spider):
    name = "comments"

    def start_requests(self):
        urls = []
        for i in range(1001,1002):
            urls.append('http://m.weibo.cn/api/comments/show?id=4087456787650507&page=' + str(i))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    # def start_requests(self):
    #     url = 'http://m.weibo.cn/api/comments/show?id=4087456787650507&page=2'

    #     Cookie = {
    #         "_T_WM": "f72011a149cf4528d4d66891299056ec", 
    #         "SCF": "AhCVRLcfk9GvyqL8T3zVWYAcCIq3Y7g4DUYi_1BeU1oUt6qP2McTe7MI8OkUQ1tnzOBjSBJaO_QNyVDcGz7y5Kg.", 
    #         "SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9W5JH.UGuHUvzUj7iwmR8EB.5JpX5o2p5NHD95QE1he4Shnp1Kn7Ws4Dqcjdi--Xi-ihiKy2i--Xi-ihiKy2i--Ri-24i-z4", 
    #         "H5_INDEX": "2", 
    #         "H5_INDEX_TITLE": "%E4%BC%8D%E4%BC%8D%E8%A9%B9", 
    #         "WEIBOCN_WM": "3349", 
    #         "H5_wentry": "H5", 
    #         "backURL": "http%3A%2F%2Fm.weibo.cn%2Fu%2F1618051664%3Fuid%3D1618051664%26extparam%3D%26luicode%3D10000011%26lfid%3D100103type%3D3%26q%3D%E5%A4%B4%E6%9D%A1%E6%96%B0%E9%97%BB", 
    #         "SUB": "_2A2511KuFDeRxGeRG6FsV-C_FwzyIHXVXNjXNrDV6PUJbkdBeLRnckW1CcD7zG__4OXdkyx6eiYmSiS-vzw..", 
    #         "SUHB": "0D-ENFn2mATz7w", 
    #         "SSOLoginState": "1490082773", 
    #         "M_WEIBOCN_PARAMS": "luicode%3D10000011%26lfid%3D1076031618051664"
    #     }
    #     yield scrapy.FormRequest(url,callback=self.parse)


    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
        item = WeiboItem()
        rep = json.loads(response.body_as_unicode())
        print(response.url + '  crawl done!')
        for data in rep['data']:
            item['comment_id'] = data['id']
            item['name'] = data['user']['screen_name']
            item['text'] = data['text']
            item['source'] = data['source']
            if 'reply_text' in data:
                item['reply_text'] = data['reply_text']
            else:
                item['reply_text'] = '-'
            s = data['text']
            if (s.find('@') != -1) & (s.find('</') != -1):
                item['reply_name'] = s[s.find('@')+1:s.find('</')]
            else:
                item['reply_name'] = '-'
            yield item
