from typing import Any

from scrapy import Spider
from scrapy.http import Response

from urls.items import WaterItem
from urls.itemsloaders import WaterItemsLoader


class BetaWaterSpider(Spider):
    name = "beta_water"
    allowed_domains = ["beta.co.id"]
    start_urls = ["https://beta.co.id/portfolio-project/"]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        for div in response.css('div.wp-block-column-is-layout-flow'):
            name = div.css('h3::text').get()
            if name is None:
                continue
            loader = WaterItemsLoader(item=WaterItem(), selector=div)
            loader.add_value('name', name)

            location = div.css('table tr td + td::text').get()
            location = location.split(', ')
            loader.add_value('province', location[-1])
            location = ', '.join(location[0:len(location)-2])
            loader.add_value('location', location)

            loader.add_value('source', response.url)
            loader.add_value('year_announced', div.css('table tr:nth-child(2) td + td::text').get())
            for tr in div.css('table'):
                if tr.css('td::text').get() == 'Kapasitas':
                    loader.add_value('capacity', tr.css('td + td::text').get())
                elif tr.css('td::text').get() == 'Klien':
                    loader.add_value('owner', tr.css('td + td::text').get())

            yield loader.load_item()
