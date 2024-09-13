from scrapy import Spider

from urls.itemsloaders import WikiItemsLoader
from urls.items import WikiSpiderItem, CommonPowerSpiderItem


class WikiSpider(Spider):
    name = 'wiki'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_power_stations_in_Indonesia']

    def parse(self, response):
        j = -1
        type = ['Thermal', 'Thermal', 'Thermal', 'Geothermal', 'Hydroelectric', 'Pumped-storage hydroelectric', 'Wind', 'Solar']
        status = ['Operational', 'Proposed or under construction', 'Operational', 'Operational', 'Operational', 'Under construction or planned', 'Operational', 'In development']
        primary_fuel = ['Bituminous coal or lignite', 'Bituminous coal or lignite', 'Gas or liquid fuel', '', '', '', '', '']
        for table in response.css('table.wikitable'):
            j += 1

            capacity_index = None
            header = table.css('tr th')

            # Traverse through table headers to find the index of the capacity column
            for i, th in enumerate(header):
                if th.css('::text').get() == 'Capacity (MW)' or th.css('::text').get() == 'Installed capacity':
                    capacity_index = i + 1 # +1 nth-child first element is 1
                    break

            for row in table.css('tr')[1:]:
                loader = WikiItemsLoader(item=CommonPowerSpiderItem(), selector=row)
                name = row.css('td:nth-child(1) a::text').get()
                if name is None:
                    name = row.css('td:nth-child(1)::text').get()
                loader.add_value('name', name)
                loader.add_value('source', response.url)
                loader.add_value('capacity', row.css(f'td:nth-child({capacity_index})::text').get())
                loader.add_value('location', row.css('td:nth-child(3) a::text').get())
                # First one is settlement and second one is district
                sublocation_1 = row.css('td:nth-child(2)::text').get(default='')
                sublocation_2 = row.css('td:nth-child(3) a::text').get(default='')

                loader.add_value('sublocation', sublocation_1 + ' ' + sublocation_2)
                loader.add_value('plant_type', type[j])
                loader.add_value('primary_fuel', primary_fuel[j])
                loader.add_value('status', status[j])
                yield loader.load_item()
