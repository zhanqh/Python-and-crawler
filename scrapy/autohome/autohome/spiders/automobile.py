# -*- coding: utf-8 -*-

import json
import string
from scrapy import Request
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import parse_qs, urlencode, urlparse
from autohome.items import ModelItem, SeriesItem

class AutomobileSpider(CrawlSpider):
    name = "automobile"
    allowed_domains = ["www.autohome.com.cn"]

    start_urls = [
        "http://www.autohome.com.cn/grade/carhtml/" + x + ".html"
        for x in string.ascii_uppercase if x not in "EIUV"
    ]

    rules = (
        Rule(LinkExtractor(allow=("/\d+/#",)), callback="parse_item"),
    )

    def parse(self,response):
        params = {
            "url": response.url,
            "status": response.status,
            "headers": response.headers,
            "body": response.body,
        }

        response = HtmlResponse(**params)

        return super().parse(response)

    def parse_item(self, response):
        sel = response.css("div.path")

        loader = ItemLoader(item=SeriesItem(), selector=sel)
        loader.add_css("series_id", "a:last-child::attr(href)")
        loader.add_css("series_name", "a:last-child::text")

        series = loader.load_item()
        print(series)

        # 即将销售 & 在售
        for sel in response.css("div.interval01-list-cars-infor"):
            loader = ItemLoader(item=ModelItem(), selector=sel)
            loader.add_css("model_id", "a::attr(href)")
            loader.add_css("model_name", "a::text")
            loader.add_value("series_id", series['series_id'])
            loader.add_value("series_name", series['series_name'])

            yield loader.load_item()

        # 停售
        url = "http://www.autohome.com.cn/ashx/series_allspec.ashx"

        years = response.css(".dropdown-content a::attr(data)")

        for year in years.extract():
            qs = {
                "y": year,
                "s": series["series_id"]
            }

            yield Request(url + "?" + urlencode(qs), self.stop_sale)

    def stop_sale(self, response):
        qs = parse_qs(urlparse(response.url).query)

        body = json.loads(response.body_as_unicode())

        for spec in body["Spec"]:
            yield {
                "model_id": str(spec["Id"]),
                "model_name": str(spec["Name"]),
                "series_id": str(qs["s"][0]),
            }