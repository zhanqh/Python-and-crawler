import scrapy


class QuotesSpider(scrapy.Spider):
    name = "test"
    start_urls = [
        'https://www.whatismybrowser.com/'
    ]

    def parse(self, response):
        print(response.css('div.corset div.string-major::text').extract_first())