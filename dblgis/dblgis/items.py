# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DblgisItem(scrapy.Item):
    ua = scrapy.Field()
    country = scrapy.Field()


class RubricsItem(scrapy.Item):
    all_item = scrapy.Field()
