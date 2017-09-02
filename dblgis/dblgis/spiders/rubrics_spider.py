import scrapy

from ..items import RubricsItem

import json
from functools import reduce


class RubricsSpider(scrapy.Spider):
    name = 'firms'

    allowed_domains = ['2gis.ru']

    start_urls = ['https://catalog.api.2gis.ru/2.0/catalog/rubric/list?parent_id=0&region_id=32&locale=ru_RU&sort=popularity&fields=items.rubrics&key=rutnpt3272']

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        rubrics_data = list(map(lambda j: list(map(lambda i: i['id'], j['rubrics'])), json_response['result']['items']))
        id_sub_rubrics = list(filter(None, reduce(lambda x, y: x + y, rubrics_data)))
        for id_sub in id_sub_rubrics[0:2]:
            api_sub_rubrics = 'https://catalog.api.2gis.ru/2.0/catalog/marker/search?page=1&page_size=10000&rubric_id=%s&region_id=32&locale=ru_RU&key=rutnpt3272' % id_sub
            yield scrapy.Request(api_sub_rubrics, callback=self.parse_sub)

    def parse_sub(self, response):
        json_response = json.loads(response.body_as_unicode())
        id_buildings = list(map(lambda i: i['id'].split('_')[0], json_response['result']['items']))
        full_list_buildings = id_buildings
        for id_build in full_list_buildings[0:1]:
            api_building_data = 'https://catalog.api.2gis.ru/2.0/catalog/branch/get?id=%s&fields=items.name_ex&key=rutnpt3272' % id_build
            yield scrapy.Request(api_building_data, callback=self.parse_item)

    def parse_item(self, response):
        json_response = json.loads(response.body_as_unicode())
        item = RubricsItem()

        def collect_data(building):
            firm = dict()
            no_data = '-'
            try:
                firm['name'] = building['name_ex']['primary']
            except:
                firm['name'] = no_data
            try:
                try:
                    address_comment = building['address_comment']
                    firm['address'] = '{}, {}'.format(building['address_name'], address_comment)
                except KeyError:
                    firm['address'] = building['address_name']
            except:
                firm['address'] = no_data
            try:
                firm['phone'] = ', '.join(list(filter(None, map(lambda i: i['value'] if i['type'] == 'phone' else '', building['contact_groups'][0]['contacts']))))
            except:
                firm['phone'] = no_data
            return firm

        item['all_item'] = list(map(collect_data, json_response['result']['items']))
        yield item
