from typing import Any

from scrapy import Spider
from scrapy.http import Response

from urls.itemsloaders import WikiMineItemsLoader

from urls.items import MiningItem


class WikiMiningSpider(Spider):
    name = "wikimine"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ['https://en.wikipedia.org/wiki/Category:Bauxite_mines_in_Indonesia',
                  'https://en.wikipedia.org/wiki/Category:Coal_mines_in_Indonesia',
                  'https://en.wikipedia.org/wiki/Category:Copper_mines_in_Indonesia',
                  'https://en.wikipedia.org/wiki/Category:Diamond_mines_in_Indonesia',
                  'https://en.wikipedia.org/wiki/Category:Gold_mines_in_Indonesia',
                  'https://en.wikipedia.org/wiki/Category:Lead_and_zinc_mines_in_Indonesia',
                  'https://en.wikipedia.org/wiki/Category:Nickel_mines_in_Indonesia']

    def parse(self, response: Response, **kwargs: Any) -> Any:
        for a in response.css('div.mw-category-group a'):
            loader = WikiMineItemsLoader(item=MiningItem(), response=response)
            loader.add_value('name', a.css('::text').get())
            print(a.css('::text').get())

            url = a.css('::attr(href)').get()
            url = response.urljoin(url)
            loader.add_value('source', url)

            yield response.follow(url=url, callback=self.parse_mining, meta={'loader': loader})

    def parse_mining(self, response):
        loader = response.meta['loader']
        for table in response.css('table.vcard'):
            for tr in table.css('tr'):
                key = tr.css('th::text').get()
                if key == 'Location':
                    text = tr.css('td a::text').get()
                    if text is None:
                        text = tr.css('td::text').get()
                    loader.add_value('location', text)
                if key == 'Province':
                    text = tr.css('td a::text').get()
                    if text is None:
                        text = tr.css('td::text').get()
                    loader.add_value('province', text)
                if key == 'Products':
                    products = ''
                    for a in tr.css('td a'):
                        if a is not None:
                            products += a.css('::text').get() + '\n '
                    loader.add_value('products', products)
                if key == 'Production':
                    loader.add_value('production', tr.css('td li::text').getall())
                if key == 'Financial year':
                    loader.add_value('financial_year', tr.css('td::text').get())
                if key == 'Discovered':
                    loader.add_value('discovered', tr.css('td::text').get())
                if key == 'Opened':
                    loader.add_value('opened', tr.css('td::text').get())
                if key == 'Closed':
                    loader.add_value('closed', tr.css('td::text').get())
                if key == 'Year of acquisition':
                    loader.add_value('acquisition_year', tr.css('td::text').get())
                if key == 'Company':
                    loader.add_value('company', tr.css('td a::text').getall())
                if key == 'Website':
                    loader.add_value('website', tr.css('td a::attr(href)').get())
                if key == 'Area':
                    loader.add_value('area', tr.css('td::text').get())
                if key == 'Type':
                    loader.add_value('type', tr.css('td::text').get())
        yield loader.load_item()
