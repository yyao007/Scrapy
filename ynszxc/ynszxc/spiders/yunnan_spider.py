# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from ynszxc.items import YnszxcItem

class YunnanSpiderSpider(scrapy.Spider):
    name = "yn"
    allowed_domains = ["http://www.ynszxc.gov.cn/"]
    start_urls = (
        'http://www.ynszxc.gov.cn/S1/',
    )

    def parse(self, response):
        county_list = response.xpath('//ul[@class="menu"]/li/ul/li/a/@href').extract()
        # county_list = response.xpath('//ul[@class="menu"]/li[6]/ul/li/a/@href').extract()
        for c in county_list:
            url = response.urljoin(c)
            yield scrapy.Request(url, callback=self.parse_county, dont_filter=True)

        pass

    def parse_county(self, response):
        town_list = response.xpath('//div[@class="colcont"]/div/li/a/@href').extract()
        for t in town_list:
            url = response.urljoin(t)
            yield scrapy.Request(url, callback=self.parse_town, dont_filter=True)

        pass

    def parse_town(self, response):
        village_list = response.xpath('//ul[@class="newsline"]/div/a/@href').extract()
        for v in village_list:
            url = response.urljoin(v)
            # url += "RL/2010.shtml"
            yield scrapy.Request(url, callback=self.parse_village, dont_filter=True)

        pass

    def parse_village(self, response):
        chart = response.xpath('//div[@id="button"]/a[2]/@href').extract()[0]
        url = response.urljoin(chart)
        yield scrapy.Request(url, callback=self.parse_table, dont_filter=True)
        pass

    def parse_table(self, response):
        level = response.xpath('//div[@id="nav"]/a/text()').extract()
        v_url = response.xpath('//div[@id="nav"]/a/@href').extract()[4]
        v_id = v_url[v_url.rfind('S'): -1]
        year = response.xpath('//p/text()').extract()[0].split()[1]
        l = ItemLoader(item=YnszxcItem(), response=response)
        l.add_value('year', year)
        l.add_value('city', level[1])
        l.add_value('county', level[2])
        l.add_value('town', level[3])
        l.add_value('village', level[4])
        l.add_value('v_id', v_id)
        for i in range(2, 12):
            xpath = '//table[' + str(i) + ']/tr/td/text()'
            table = 'table' + str(i-1)
            l.add_xpath(table, xpath)
        
        return l.load_item()


