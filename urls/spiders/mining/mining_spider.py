from typing import Any

from scrapy import Spider
from scrapy.http import Response

from urls.itemsloaders import WikiMineItemsLoader
from urls.items import MiningItem


class MiningSpider(Spider):
    name = "mining"
    allowed_domains = ["www.fareast.gold"]
    start_urls = ['']

    def parse(self, response: Response, **kwargs: Any) -> Any:
        loader = WikiMineItemsLoader(item=MiningItem(), response=response)
        loader.add_value('name', response.css('list-item-content h2::text').get())

        url = response.css('div.list-item-content a::attr(href)').get()
        url = response.urljoin(url)

        loader.add_value('source', url)

        yield response.follow(url=url, callback=self.parse_mining, meta={'loader': loader})

    def parse_mining(self, response):
        loader = response.meta['loader']
        # Area in ha
        loader.add_value('area', response.css('div.image-subtitle li:nth-child(3) p.sqsrte-small::text').get())