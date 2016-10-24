# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os
import sys
from scrapy.exceptions import DropItem

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

class IPPipeline(object):
    def process_item(self, item, spider):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        line = item['ip'] + ":" + item['port'] + '\n'
        filename = spider.name + ".txt"
        f = open(filename, 'a')
        f.write(line)
        f.close()
        return item


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['ip'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['ip'])
            return item
