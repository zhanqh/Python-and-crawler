# -*- coding: utf-8 -*-
import scrapy
from emscnu.items import NewsItem, DetailsItem
from scrapy.loader import ItemLoader


class EmnewsSpider(scrapy.Spider):
    name = "emnews"
    allowed_domains = ["em.scnu.edu.cn"]
    urls = ['http://em.scnu.edu.cn/xueyuanxinwen/'+str(x)+'.html' for x in range(2,3)]
    start_urls = ['http://em.scnu.edu.cn/xueyuanxinwen/index.html'] + urls

    def parse(self, response):
        if response.status is 200:
            print(response.url + '  ✔︎')
            news = NewsItem()
            details = DetailsItem()

            resource = response.css('div.c_news ul li')
            for li in resource:
                news['title'] = li.css('a::text').extract_first()
                details['date'] = li.css('span::text').extract_first()[1:-1]
                if li.css('a::attr(href)').extract_first().find('http') is -1:
                    details['url'] = 'http://em.scnu.edu.cn' + li.css('a::attr(href)').extract_first()
                else:
                    details['url'] = li.css('a::attr(href)').extract_first()
                news['details'] = details
                yield news
        else:
            print('Response Error')
            self.logger.error('Response Error')
