# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os
import sys
from scrapy.exceptions import DropItem

def to_str(t, n):
    if not t[4*n+3]:
        return t[4*n+4]
    else:
        return t[4*n+4] + ' ' + t[4*n+3]

def to_str4(t, n):
    if not t[4*n+4]:
        return t[4*n+5]
    else:
        return t[4*n+5] + ' ' + t[4*n+4]

def key(t, n):
    ret = t[4*n+2]
    if u'其中' in ret:
        ret = ret[3:]
    return ret

def key4(t, n):
    ret = t[4*n+3]
    if u'其中' in ret:
        ret = ret[3:]
    return ret

class YnszxcPipeline(object):
    def process_item(self, item, spider):
        lineDict = dict(item)
        t = []
        t.append(self.parse_table1(lineDict['table1']))
        t.append(self.parse_table2(lineDict['table2']))
        t.append(self.parse_table3(lineDict['table3']))
        t.append(self.parse_table4(lineDict['table4']))
        t.append(self.parse_table5(lineDict['table5']))
        t.append(self.parse_table6(lineDict['table6']))
        t.append(self.parse_table7(lineDict['table7']))
        t.append(self.parse_table8(lineDict['table8']))
        t.append(self.parse_table9(lineDict['table9']))
        t.append(self.parse_table10(lineDict['table10']))

        for i in range(len(t)):
            k = "table" + str(i+1)
            lineDict.pop(k)
            lineDict[t[i]['name']] = t[i]['table']

        filename = "result/ynszxc.json"
        reload(sys)
        sys.setdefaultencoding('utf-8')
        with open(filename, 'a') as f:
            line = json.dumps(lineDict, ensure_ascii=False) + '\n'
            f.write(line)
            f.close()
        return item

    def parse_table1(self, t):
        ret = {}
        d = {}
        ret['name'] = t[0][2:]
        for n in range(5):
            d[key(t, n)] = to_str(t, n)

        d1 = {}
        d1['total'] = to_str(t, 5)

        level1 = ''
        n = 6
        while n < 22:
            if key(t, n)[0].isdigit():
                level1 = key(t, n)[2:]
                d1[level1] = {}
                d1[level1]['total'] = to_str(t, n)
                # special case for 2.林地面积
                if key(t, n)[0] == '2':
                    d1[level1][to_str(t, n+1)] = to_str(t, n+2)
                    n += 3
                    level2 = key(t, n)
                    d1[level1][level2] = {}
                    d1[level1][level2]['total'] = to_str(t, n)
                    d1[level1][level2][key(t, n+1)] = to_str(t, n+1)
                    d1[level1][level2][key(t, n+2)] = to_str(t, n+2)
                    n += 2

            else:
                d1[level1][key(t, n)] = to_str(t, n)

            n += 1      

        d[key(t, 5)] = d1
        d[key(t, 22)] = to_str(t, 22)
        
        ret['table'] = d
        return ret
    
    def parse_table2(self, t):
        ret = {}
        d = {}
        ret['name'] = t[0][2:]
        for n in range(3):
            d[key(t, n)] = to_str(t, n)
        d[key(t, 3)] = {}
        d[key(t, 3)]['total'] = to_str(t, 3)
        d[key(t, 3)][key(t, 4)] = to_str(t, 4)

        level1 = ''
        n = 5
        while n < 20:
            pos = key(t, n).find('：')
            if not pos == -1:
                level1 = key(t, n)[:pos]
                d[level1] = {}
                d[level1][key(t, n)[pos+1:]] = to_str(t, n)

            else:
                if u'民族' in key(t, n):
                    level2 = key(t, n)
                    d[level1][level2] = {}
                    d[level1][level2]['total'] = to_str(t, n)
                    for i in range(n+1, 15, 2):
                        d[level1][level2][to_str(t, i)] = to_str(t, i+1)
                    
                    n = i + 2
                    d[level1][level2][key(t, n)] = to_str(t, n)
                else:
                    d[level1][key(t, n)] = to_str(t, n)

            n += 1
        
        ret['table'] = d
        return ret
        pass

    def parse_table3(self, t):
        ret = {}
        d = {}
        ret['name'] = t[0][2:]
        
        d1 = {}
        d1['total'] = to_str(t, 0)
        
        level1 = ''
        n = 1
        while n < 19:
            if key(t, n)[0].isdigit():
                level1 = key(t, n)[2:]
                d1[level1] = {}
                d1[level1]['total'] = to_str(t, n)
                # special case for 6.
                if key(t, n)[0] == '6':
                    d1[level1][key(t, n+1)] = to_str(t, n+1)
                    n += 2
                    level2 = key(t, n)
                    d1[level1][level2] = {}
                    d1[level1][level2]['total'] = to_str(t, n)
                    level3 = key(t, n+1)
                    d1[level1][level2][level3] = {}
                    d1[level1][level2][level3]['total'] = to_str(t, n+1)
                    for i in range(n+2, n+4):
                        d1[level1][level2][level3][key(t, i)[2:]] = to_str(t, i)
                    n = i
            else:
                d1[level1][key(t, n)] = to_str(t, n)

            n += 1

        d[key(t, 0)] = d1
        for n in range(19, 22):
            d[key(t, n)] = to_str(t, n)
        
        ret['table'] = d
        return ret
        pass


    def parse_table4(self, t):
        ret = {}
        d = {}
        ret['name'] = t[0][2:]

        level1 = ''
        for n in range(16):
            pos = key(t, n).find('：')
            if not pos == -1 and not 'a' in key(t, n):
                level1 = key(t, n)[:pos]
                d[level1] = {}
                d[level1][key(t, n)[pos+1:]] = to_str(t, n)
            else:
                d[level1][key(t, n)] = to_str(t, n)

        n += 1
        while n < 33:
            pos = key4(t, n).find('：')
            if not pos == -1:
                level1 = key4(t, n)[:pos]
                d[level1] = {}
                d[level1][key4(t, n)[pos+1:]] = to_str4(t, n)
            else:
                # special case for row 79
                if n == 24:
                    d[level1][key4(t, n)] = {}
                    d[level1][key4(t, n)]['total'] = to_str4(t, n)
                    d[level1][key4(t, n)][key4(t, n+1)] = to_str4(t, n+1)
                    n += 1
                else:
                    d[level1][key4(t, n)] = to_str4(t, n)

            n += 1

        ret['table'] = d
        return ret
        pass

    def parse_table5(self, t):
        ret = {}
        d = {}
        ret['name'] = t[0][2:]

        level1 = ''
        n = 0
        while n < 24:
            pos = key(t, n).find('：')
            if not pos == -1:
                level1 = key(t, n)[:pos]
                d[level1] = {}
                # special case for line 98
                if n == 10:
                    level2 = key(t, n)[pos+1:]
                    for n in range(10, 14, 2):
                        d[level1][level2] = {}
                        d[level1][level2]['total'] = to_str(t, n)
                        d[level1][level2][key(t, n+1)] = to_str(t, n+1)
                        level2 = key(t, n+2)
                    n += 1
                else:
                    d[level1][key(t, n)[pos+1:]] = to_str(t, n)
            else:
                d[level1][key(t, n)] = to_str(t, n)

            n += 1

        ret['table'] = d
        return ret
        pass

    def parse_table6(self, t):
        ret = {}
        d = {}
        ret['name'] = t[0][2:]
        for n in range(4):
            d[key(t, n)] = to_str(t, n)

        ret['table'] = d
        return ret
        pass

    def parse_table7(self, t):
        ret = {}
        d = {}
        ret['name'] = t[0][2:]

        n = 0
        while n < 14:
            if n == 11:
                d[key(t, n)] = {}
                d[key(t, n)]['total'] = to_str(t, n)
                d[key(t, n)][key(t, n+1)] = to_str(t, n+1)
                n += 1
            else:
                d[key(t, n)] = to_str(t, n)

            n += 1


        ret['table'] = d
        return ret
        pass

    def parse_table8(self, t):
        ret = {}
        d = {}
        ret['name'] = t[0][2:]

        level1 = ''
        n = 0
        for n in range(13):
            pos = key(t, n).find('：')
            if not pos == -1:
                level1 = key(t, n)[:pos]
                d[level1] = {}
                d[level1][key(t, n)[pos+1:]] = to_str(t, n)
            else:
                d[level1][key(t, n)] = to_str(t, n)

        for n in range(13, 17, 2):
            level2 = key(t, n)
            d[level1][level2] = {}
            d[level1][level2]['total'] = to_str(t, n)
            d[level1][level2][key(t, n+1)] = to_str(t, n+1)

        ret['table'] = d
        return ret
        pass

    def parse_table9(self, t):
        ret = {}
        d = {}
        ret['name'] = t[0][2:]
        for n in range(5):
            d[key(t, n)] = to_str(t, n)

        d[key(t, 5)] = {}
        d[key(t, 5)]['total'] = to_str(t, 5)
        d[key(t, 5)][key(t, 6)] = to_str(t, 6)

        ret['table'] = d
        return ret
        pass

    def parse_table10(self, t):
        ret = {}
        d = {}
        ret['name'] = t[0][2:]

        for n in range(2):
            v = t[2*n+2]
            pos = v.find('：')
            d[v[:pos]] = v[pos+1:]

        ret['table'] = d
        return ret
        pass


class DuplicatesPipeline(object):
    def __init__(self):
        self.villages = []
        filename = "result/ynszxc.json"
        if os.path.exists(filename):
            f = open(filename, 'r')
            line = f.readline()
            while line:
                lineItem = json.loads(line)
                self.villages.append(lineItem['v_id'])
                line = f.readline()        

    def process_item(self, item, spider):
        if item['v_id'] in self.villages:
            raise DropItem("Duplicate item found: %s" % item['village'])
        else:
            self.villages.append(item['v_id'])
            return item



