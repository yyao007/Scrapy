# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item, object):
    # define the fields for your item here like:
    positionName = scrapy.Field()
    positionId = scrapy.Field()
    education = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    createTime = scrapy.Field()
    companyFullName = scrapy.Field()
    companyShortName = scrapy.Field()
    companyId = scrapy.Field()
    companySize = scrapy.Field()
    workYear = scrapy.Field()
    jobNature = scrapy.Field()
    financeStage = scrapy.Field()
    logo = scrapy.Field()
    field = scrapy.Field() 
    companyLabel = scrapy.Field()
    salary = scrapy.Field()
    businessZones = scrapy.Field()
    advantage = scrapy.Field()
    description = scrapy.Field()
    location = scrapy.Field()

    def list(self):
        for name, value in vars(self).items():
            print value

class IPItem(scrapy.Item, object):
    ip = scrapy.Field()
    port = scrapy.Field()






