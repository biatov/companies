import scrapy

from ..items import RubricsItem

import json
from functools import reduce


class RubricsSpider(scrapy.Spider):
    name = 'get_sub_rubrics'

    allowed_domains = ['2gis.ru']

    start_urls = ['https://catalog.api.2gis.ru/2.0/catalog/rubric/list?parent_id=0&region_id=32&locale=ru_RU&sort=popularity&fields=items.rubrics&key=rutnpt3272']

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())

        item = RubricsItem()
        rubrics_data = list(map(lambda j: list(map(lambda i: i['id'], j['rubrics'])), json_response['result']['items']))
        item['id_sub_rubric'] = list(filter(None, reduce(lambda x, y: x + y, rubrics_data)))
        yield item
