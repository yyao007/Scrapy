import scrapy
import json
from lagou.items import LagouItem

class LagouSpider(scrapy.Spider):
    name = "lg"
    allowed_domains = ["http://www.lagou.com/"]
    url_prefix = "http://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&first=false&pn="
    keyword = "kd=%E7%88%AC%E8%99%AB%E5%B7%A5%E7%A8%8B%E5%B8%88"
    urls=[]
    for i in range(1,24):
        url = url_prefix + str(i) + '&' + keyword
        urls.append(url)

    start_urls = urls

    def parse(self, response):
        pages = json.loads(response.body)
        for i in pages["content"]["positionResult"]["result"]:
            item = LagouItem()
            item['positionName'] = i["positionName"]
            item['positionId'] = i["positionId"]
            item['education'] = i["education"]
            item['city'] = i["city"]
            item['district'] = i["district"]
            item['createTime'] = i['createTime']
            item['companyFullName'] = i["companyFullName"]
            item['companyShortName'] = i["companyShortName"]
            item['companyId'] = i["companyId"]
            item['companySize'] = i["companySize"]
            item['workYear'] = i["workYear"]
            item['jobNature'] = i['jobNature']
            item['financeStage'] = i["financeStage"]
            item['logo'] = i["companyLogo"]
            item['field'] = i["industryField"]
            item['companyLabel'] = i["companyLabelList"]
            item['salary'] = i["salary"]
            item['businessZones'] = i["businessZones"]
            item['advantage'] = i["positionAdvantage"]

            newURL = "http://www.lagou.com/jobs/" + str(item['positionId']) + ".html"
            request = scrapy.Request(newURL, callback=self.parse_jobs, dont_filter=True)
            request.meta['item'] = item
            
            yield request
            #print item['location']
            

    def parse_jobs(self, response):
        desc = response.xpath('//dd[@class="job_bt"]/p/text()').extract()
        location = self.getAddress(response)
        
        item = response.meta['item']
        #item = LagouItem()
        item['description'] = desc
        item['location'] = location.strip()
        print item['location']
        
        return item

    def getAddress(self, response):
        location1 = response.xpath('//div[@class="work_addr"]/text()').extract()
        location2 = response.xpath('//dl[@class="job_company"]/dd/div/text()').extract()
        if len(location1) == 4:
            location = location1[3]
        elif len(location1) == 3:
            location = location1[2]
        elif len(location1) == 0 and len(location2) > 0:
            location = location2[0]
        else:
            location = ""
        
        return location
