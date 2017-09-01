import scrapy

from ..items import DblgisItem


class SimpleSpider(scrapy.Spider):
    name = 'simple'
    allowed_domains = ['www.cy-pr.com']
    start_urls = ['https://www.cy-pr.com/tools/browser/']

    def parse(self, response):
        item = DblgisItem()
        item['ua'] = response.xpath('.//table[@class="tablesorter tal"]/tbody')[1].xpath('.//tr')[1].xpath('.//td')[1].xpath('text()').extract_first()
        item['country'] = response.xpath('.//table[@class="tablesorter tal"]/tbody')[0].xpath('.//tr')[2].xpath('.//td')[1].xpath('text()').extract_first()
        yield item
