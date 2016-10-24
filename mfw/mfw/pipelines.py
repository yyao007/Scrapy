# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os
import sys
from scrapy.exceptions import DropItem

class MfwPipeline(object):
    def process_item(self, item, spider):
        # lineItem = item.items()
        # lineItem.sort()
        lineDict = dict(item)
        filename = "result/mafengwo_new.json"
        reload(sys)
        sys.setdefaultencoding('utf-8')
        with open(filename, 'a') as f:
            line = json.dumps(lineDict, ensure_ascii=False) + '\n'
            f.write(line)
            f.close()
        return item

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = []
        filename = "result/mafengwo_new.json"
        f = open(filename, 'r')
        line = f.readline()
        while line:
            lineItem = json.loads(line)
            self.ids_seen.append(lineItem['ID'])
            line = f.readline()        

    def process_item(self, item, spider):
        if item['ID'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item['ID'])
        else:
            self.ids_seen.append(item['ID'])
            return item

