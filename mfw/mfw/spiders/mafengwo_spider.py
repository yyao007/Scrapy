# -*- coding: utf-8 -*-
import scrapy
import ast
from mfw.items import MfwItem 
from bs4 import BeautifulSoup

class MafengwoSpiderSpider(scrapy.Spider):
    name = "mafengwo"
    allowed_domains = ["http://www.mafengwo.cn"]
    start_urls = (
        'http://www.mafengwo.cn/mdd',
    )

    def parse(self, response):
        intl = response.xpath('//div[1]/div/dl[@class="item"]/dd/ul/li/a')
        
        for j in intl:
            urlStr = str(j.xpath('@href').extract()[0])
            urlId = filter(str.isdigit, urlStr)
            prefix = "http://www.mafengwo.cn/mdd/citylist/"
            url = prefix + urlId + ".html"
            
            country = j.xpath('text()').extract()[0].strip()
            url_jd = "http://www.mafengwo.cn/jd/" + urlId + "/gonglve.html"
            
            yield scrapy.Request(url, callback=self.parse_citylist, dont_filter = True)
            yield scrapy.Request(url_jd, callback=lambda response, country=country: self.parse_jd(response,country), dont_filter = True)
        
        # url = "http://www.mafengwo.cn/mdd/citylist/10448.html"
        # yield scrapy.Request(url, callback=self.parse_citylist, dont_filter = True)

        pass

    def parse_citylist(self, response):
        pages = response.xpath('//span[@class="count"]/text()').extract()    
        ID = filter(str.isdigit, response.url)    
        asciiStr = pages[0].encode("utf-8")
        count = int(filter(str.isdigit, asciiStr))
        
        if count == 0:
            return
        else: 
            country = response.xpath('//div[@class="drop"]/span/a/text()').extract()[0]
            for i in range(1,count+1):
                yield scrapy.FormRequest(url="http://www.mafengwo.cn/mdd/base/list/pagedata_citylist", formdata={"mddid":ID, "page":str(i)}, callback=lambda response, country=country: self.parse_city(response,country), method="POST", dont_filter=True)

        pass

    def parse_city(self, response, country):
        htmlDict = ast.literal_eval(response.body)
        htmlStr = htmlDict['list']
        html = self.toHTMLString(htmlStr)
        soup = BeautifulSoup(html, 'lxml')
        urls = soup.find_all('div',class_="img")
        
        for u in urls:
            url = u.a['href']
            cityID = filter(str.isdigit, url)
            cityURL = "http://www.mafengwo.cn/jd/" + cityID + "/gonglve.html"
            
            yield scrapy.Request(cityURL, callback=lambda response, country=country: self.parse_jd(response,country), dont_filter = True)

        pass

    def parse_jd(self, response, country):
        urls = response.xpath('//div[@class="list"]/ul/li/a/@href').extract()
        for i in urls:
            ending = str(i)
            attrURL = "http://www.mafengwo.cn" + ending

            yield scrapy.Request(attrURL, callback=lambda response, country=country: self.parse_poi(response,country), dont_filter = True)

        pass

    def parse_poi(self, response, country):
        item = MfwItem()
        item['ID'] = int(filter(str.isdigit, response.url))
        item['country'] = country
        item['dest'] = response.xpath('//div[@class="item"][2]/div/span/a/text()').extract()[0]
        item['attraction'] = response.xpath('//div[@class="s-title"]/h1/text()').extract()[0]
        item['description'] = self.getDesc(response)
        item['reviewCount'] = self.getCount(response)
        item['latitude'] = self.getLatLong(response, "lat")
        item['longitude'] = self.getLatLong(response, "long")
        item['been'] = response.xpath('//span[@class="pa-num"]/text()').extract()[1]
        return item
        
        pass

    

    def getDesc(self, response):
        descList = response.xpath('//dl[@class="intro"]/dt/p/span/text()').extract()
        if len(descList) == 0:
            desc = ""
        else:
            desc = descList[0]

        return desc

    def getCount(self, response):
        count = response.xpath('//li[@data-scroll="commentlist"]/a/em/text()').extract()
        if len(count) == 0:
            reviewCount = 0
        else:
            reviewCount = int(count[0])

        return reviewCount

    def getLatLong(self, response, latorlong):
        jsContent = response.xpath('//script[@type="text/javascript"][1]/text()').extract()[0]
        begin = jsContent.find('{')
        end = jsContent.find('}')
        jsStr = jsContent[begin:end+1]
        jsDict = ast.literal_eval(jsStr)

        if latorlong == "lat":
            return jsDict['lat']
        elif latorlong == "long":
            return jsDict['lng']
        else:
            return 0

    def toHTMLString(self, htmlStr):
        HTML = ""
        for c in htmlStr:           
            if c == '\\':
                pass
            else:
                HTML += c

        return HTML;
    


