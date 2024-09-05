from email.policy import default

from scrapy import Spider

from urls.itemsloaders import WikiItemsLoader
from urls.items import WikiSpiderItem


class WikiSpider(Spider):
    name = 'wiki'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_power_stations_in_Indonesia']

    def parse(self, response):
        for table in response.css('table.wikitable'):
            capacity_index = None
            header = table.css('tr th')
            for i, th in enumerate(header):
                if th.css('::text').get() == 'Installed capacity':
                    capacity_index = i + 1 # +1 nth-child first element is 1
                    break

            if capacity_index is None:
                self.logger.error('Cannot find capacity index')
                return

            for row in table.css('tr')[1:]:
                loader = WikiItemsLoader(item=WikiSpiderItem(), selector=row)
                loader.add_value('name', row.css('td:nth-child(1) a::text').get())
                loader.add_value('location', row.css('td:nth-child(4) a::text').get())
                loader.add_value('capacity', row.css(f'td:nth-child({capacity_index})::text').get())

                sublocation_1 = row.css('td:nth-child(2)::text').get(default='')
                sublocation_2 = row.css('td:nth-child(3) a::text').get(default='')

                loader.add_value('sublocation', sublocation_1 + ' ' + sublocation_2)

                yield loader.load_item()
