from typing import Any

from scrapy import Spider
from scrapy.http import Response

from urls.itemsloaders import WikiMineItemsLoader
from urls.items import MiningItem


class MachmaonSpider(Spider):
    name = "machmaon"
    allowed_domains = ["www.macmahon.com.au"]
    start_urls = ["https://www.macmahon.com.au/about/our-projects/"]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        for div in response.css('div.cards__item'):
            loader = WikiMineItemsLoader(item=MiningItem(), response=response)
            loader.add_value('name', div.css('h2::text').get())
            loader.add_value('type', div.css('div.project__item--category::text').get())
            url = div.css('a::attr(href)').get()
            loader.add_value('source', url)
            loader.add_value('contractor', div.css('div.project__item--body--client::text').get())

            yield response.follow(url=url, callback=self.parse_mining, meta={'loader': loader})

    def parse_mining(self, response):
        loader = response.meta['loader']

        location = response.css('div.thumbnail-content__address p::text').get()
        if location is None:
            location = response.css('div.thumbnail-content__address::text').get()
            print('name: ', loader.get_output_value('name'))
        location = location.split(', ')
        if location[-1] != 'Indonesia':
            return None
        province = location[-2]
        loader.add_value('province', province)
        location = location[0]
        if province == location:
            location = 'Unknown'
        loader.add_value('location', location)

        loader.add_value('products', response.css('span.single-project__meta--label + span::text').get())
        info = response.css('span.single-project__information--item--title::text').getall()
        loader.add_value('project_value', info[0])
        loader.add_value('contract_duration', info[1])

        yield loader.load_item()
