# -*- coding: utf-8 -*-
import codecs
import json,datetime
from scrapy.exceptions import DropItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TutorialPipeline(object):

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line.decode("unicode_escape"))
        return item
class NewbiePipeline(object):
    def prcess_item(self,item,spider):
        return item
class RunoobPipeline(object):

    def process_item(self, item, spider):

        if 'id' in item.fields and 'text' in item.fields:
              if len(item['id']) == len(item['text']):
                 for index in range(0,len(item['id'])):
                     re = item['id'][index] + ":" + item['text'][index]
                     item['result'].append(re)
            # item['text'] = item['id'] + item['text']
        elif 'link' in item.fields or 'desc' in item.fields or 'title' in item.fields:
            print("ok")
        else:
            raise DropItem("there is no id configed in %s" % item)
        return item
class JsonWriterPipeline(object):
    time = datetime.datetime.today().strftime("%Y-%m-%d")

    def open_spider(self,spider):
        spider_name = spider.name
        self.file = open(spider_name+'.json','w')
    def close_spider(self,spider):
        self.file.close()
    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False)+'\n'
        self.file.write(line)
        return item
