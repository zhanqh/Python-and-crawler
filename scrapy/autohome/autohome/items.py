# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

class SeriesItem(scrapy.Item):
    series_id = scrapy.Field(
        input_processor=MapCompose(lambda v: v.strip("/")),
        output_processor=TakeFirst()
    )
    series_name = scrapy.Field(output_processor=TakeFirst())

class ModelItem(scrapy.Item):
    model_id = scrapy.Field(
        input_processor=MapCompose(lambda v: v[6:v.find("#")-1]),
        output_processor=TakeFirst()
    )
    model_name = scrapy.Field(output_processor=TakeFirst())
    series_id = scrapy.Field(output_processor=TakeFirst())
    series_name = scrapy.Field(output_processor=TakeFirst())