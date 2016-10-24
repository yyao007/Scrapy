# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst


class YnszxcItem(scrapy.Item):
    # define the fields for your item here like:
    v_id = scrapy.Field(output_processor=TakeFirst())
    year = scrapy.Field(output_processor=TakeFirst())
    city = scrapy.Field(output_processor=TakeFirst())
    county = scrapy.Field(output_processor=TakeFirst())
    town = scrapy.Field(output_processor=TakeFirst())
    village = scrapy.Field(output_processor=TakeFirst())
    table1 = scrapy.Field(input_processor=MapCompose(unicode.strip))
    table2 = scrapy.Field(input_processor=MapCompose(unicode.strip))
    table3 = scrapy.Field(input_processor=MapCompose(unicode.strip))
    table4 = scrapy.Field(input_processor=MapCompose(unicode.strip))
    table5 = scrapy.Field(input_processor=MapCompose(unicode.strip))
    table6 = scrapy.Field(input_processor=MapCompose(unicode.strip))
    table7 = scrapy.Field(input_processor=MapCompose(unicode.strip))
    table8 = scrapy.Field(input_processor=MapCompose(unicode.strip))
    table9 = scrapy.Field(input_processor=MapCompose(unicode.strip))
    table10 = scrapy.Field(input_processor=MapCompose(unicode.strip))

    pass
