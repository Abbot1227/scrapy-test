from typing import Any

from scrapy import Spider
from scrapy.http import Response

from urls.itemsloaders import WikiMineItemsLoader
from urls.items import MiningItem

#from llama-test import get_data


class ThiessSpider(Spider):
    name = "thiess"
    allowed_domains = ["thiess.com"]
    start_urls = ["https://thiess.com/projects?region=indonesia"]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        for a in response.css('a.color-inherit'):
            loader = WikiMineItemsLoader(item=MiningItem(), response=response)
            loader.add_value('name', a.css('::text').get())

            # Relative url
            url = a.css('::attr(href)').get()
            url = response.urljoin(url)
            loader.add_value('source', url)

            yield response.follow(url=url, callback=self.parse_mining, meta={'loader': loader})

    def parse_mining(self, response):
        loader = response.meta['loader']
        location = response.css('h3.all-caps:contains("Location") + span::text').get()
        location = location.split(', ')
        loader.add_value('location', location[0])
        loader.add_value('province', location[1])
        loader.add_value('company', response.css('h3.all-caps:contains("Client") + span::text').get(default=''))
        loader.add_value('contractor', self.start_urls[0])
        loader.add_value('products', response.css('h3.all-caps:contains("Commodities") + a span::text').get(default=''))
        loader.add_value('financial_year', response.css('h3.all-caps:contains("Duration") + span::text').get(default=''))

        text = response.css('div.color-dark p::text').getall()
        text = ' '.join(text)

        data = get_data(text)

        yield loader.load_item()
