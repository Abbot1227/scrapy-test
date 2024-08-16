import scrapy
import json
from scrapy import Request
from scrapy.http import Response
from itemadapter import ItemAdapter

class ContractorsSpider(scrapy.Spider):
    name = 'contractors_async'

    custom_settings = {
        'FEED_URI': '%(name)s_%(batch_time)s.json',
        'FEED_FORMAT': 'json',
        'ITEM_PIPELINES': {
            'urls.pipelines.UrlsPipeline': 300,
        }
    }

    def start_requests(self):
        with open('by_country.json', 'r') as f:
            contractors = json.load(f)
            for contractor in contractors:
                yield {'contractor': contractor}

    def parse(self, response: Response, **kwargs):
        pass
