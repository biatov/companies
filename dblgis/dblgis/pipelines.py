# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from itertools import groupby
from os.path import exists


class DblgisPipeline(object):

    def process_item(self, item, spider):

        def more(isset_item, new_item):
            if isset_item:
                if isset_item['address'] != new_item['address']:
                    isset_item['address'] += '; %s' % new_item['address']
                if isset_data['phone'] != new_item['phone']:
                    isset_data['phone'] += '; %s' % type(new_item['phone'])
            return isset_item

        scrapy_data = item['all_item'][0]
        file_path = 'firms/%s.json' % scrapy_data['name']
        if exists(file_path):
            with open(file_path) as data_file:
                isset_data = json.load(data_file)
        else:
            isset_data = scrapy_data

        with open(file_path, 'w') as data:
            json.dump(more(isset_data, scrapy_data), data, ensure_ascii=False)
        return item
