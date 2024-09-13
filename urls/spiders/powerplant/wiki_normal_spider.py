from email.policy import default

from scrapy import Spider

from urls.itemsloaders import WikiItemsLoader
from urls.items import WikiSpiderItem


class WikiSpider(Spider):
    name = 'wiki_normal'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_power_stations_in_Indonesia']

    def parse(self, response):
        # Traverse through all powerplant types saving them
        for header in response.css('div.mw-heading'):
            plant_type = header.css('h3::text').get()

            #table = header.css('~ table.wikitable')
            table = header.xpath('following-sibling::table[contains(@class, "wikitable")][1]')
            capacity_index = None
            header = table.css('tr th')

            # Traverse through table headers to find the index of the capacity column
            for i, th in enumerate(header):
                if th.css('::text').get() == 'Installed capacity':
                    capacity_index = i + 1 # +1 nth-child first element is 1
                    break

            # Traverse through all rows to save powerplant data
            for row in table.css('tr')[1:]:
                loader = WikiItemsLoader(item=WikiSpiderItem(), selector=row)
                name = row.css('td:nth-child(1) a::text').get()
                if name is None:
                    name = row.css('td:nth-child(1)::text').get()
                loader.add_value('name', name)
                loader.add_value('capacity', row.css(f'td:nth-child({capacity_index})::text').get())
                loader.add_value('location', row.css('td:nth-child(4) a::text').get())
                loader.add_value('plant_type', plant_type)

                # First one is settlement and second one is district
                sublocation_1 = row.css('td:nth-child(2)::text').get(default='')
                sublocation_2 = row.css('td:nth-child(3) a::text').get(default='')

                loader.add_value('sublocation', sublocation_1 + ' ' + sublocation_2)

                yield loader.load_item()
