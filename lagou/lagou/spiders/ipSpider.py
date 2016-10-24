import scrapy
import json
from lagou.items import IPItem

class IPSpider(scrapy.Spider):
	name = "ip"
	allowed_domains = ["http://www.xicidaili.com"]
	start_urls = [
		"http://www.xicidaili.com/nn",
		"http://www.xicidaili.com/wn"
	]

	def parse(self, response):
		IPaddr = response.xpath('//tr[@class="odd"]/td[2]/text()').extract()
		Ports = response.xpath('//tr[@class="odd"]/td[3]/text()').extract()
		for i in range(len(IPaddr)):
			item = IPItem()
			item['ip'] = IPaddr[i]
			item['port'] = Ports[i]
			yield item
