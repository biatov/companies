# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class DblgisPipeline(object):

    def process_item(self, item, spider):
        with open('firms/%s.json' % item['all_item'][0]['name'], 'w') as data:
            json.dump(item['all_item'], data, ensure_ascii=False)
        return item
