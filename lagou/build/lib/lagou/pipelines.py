# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os
import sys

class LagouPipeline(object):
    def process_item(self, item, spider):
        lineDict = dict(item)
        filename = spider.name + ".json"
        reload(sys)
        sys.setdefaultencoding('utf-8')
        with open(filename, 'a') as f:
            line = json.dumps(lineDict, ensure_ascii=False) + '\n'
            f.write(line)
            f.close()
        
        return item

