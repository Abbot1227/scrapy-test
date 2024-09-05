from typing import Iterable, Any
import scrapy
import json
from scrapy import Request
from scrapy.http import Response


class ContractorsGermanySpider(scrapy.Spider):
    name = 'contractors_germany'

    custom_settings = {'FEED_URI': 'today%(name)s_%(batch_time)s.json',
                       'FEED_FORMAT': 'json',
                       }

    def start_requests(self) -> Iterable[Request]:
        with open('results_by_germany.json', 'r') as f:
            contractors = json.load(f)
            for contractor in contractors:
                if contractor["url"] == "":
                    continue
                yield scrapy.Request(url=contractor["url"], callback=self.parse, meta={'data': contractor})

    def parse(self, response: Response, **kwargs: Any) -> Any:
        contractor = response.meta['data']
        revenue = response.xpath('//td[a[contains(text(), "Umsatz")]]/following-sibling::td[1]/text()').getall()
        if revenue is None or len(revenue) == 0:
            return
        contractor['revenue'] = revenue
        yield contractor
