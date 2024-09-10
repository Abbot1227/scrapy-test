from email.policy import default

from scrapy import Spider

from urls.items import GemWikiSpider, CommonPowerSpiderItem
from urls.itemsloaders import GemWikiItemsLoader
from urls.utils import find_powerplant_capacity


class GEMWikiSpider(Spider):
    name = 'gemwiki'
    allowed_domains = ['www.gem.wiki']
    start_urls = ['https://www.gem.wiki/Category:Coal_power_stations_in_Indonesia',
                  'https://www.gem.wiki/Category:Oil_%26_Gas_power_stations_in_Indonesia',
                  'https://www.gem.wiki/Category:Geothermal_power_plants_in_Indonesia',]
                  #'https://www.gem.wiki/Category:Solar_farms_in_Indonesia']

    def parse(self, response):
        for li in response.css('div.mw-category li'):
            loader = GemWikiItemsLoader(item=CommonPowerSpiderItem(), selector=li)

            loader.add_value('name', li.css('a::text').get())
            details_link = li.css('a::attr(href)').get()
            details_link = response.urljoin(details_link)
            loader.add_value('source', details_link)

            if response.url == 'https://www.gem.wiki/Category:Geothermal_power_plants_in_Indonesia':
                yield response.follow(url=details_link, callback=self.parse_details_geothermal, meta={'loader': loader})
            elif response.url == 'https://www.gem.wiki/Category:Solar_farms_in_Indonesia':
                continue
            else:
                yield response.follow(url=details_link, callback=self.parse_details, meta={'loader': loader})

    def parse_details(self, response):
        loader = response.meta['loader']
        desc = response.css('p::text').get()
        loader.add_value('capacity', find_powerplant_capacity(desc))

        location = response.css('h4 + table td:nth-child(2)::text').get(default='')
        # divide location string by comma and remove the last element
        location = location[0:-12].split(', ')
        # sublocation is all except the last element
        sublocation = ', '.join(location[0:len(location)-1])
        loader.add_value('location', location[-1])
        loader.add_value('sublocation', sublocation)
        # if response.get('div.mw-normal-catlinks li a::text').get() == 'Oil & Gas power stations':
        #     pass # TODO for solar and other than thermal types
        loader.add_value('plant_type', 'Thermal') # For now only thermal from gem wiki

        info_table = response.xpath('//h4[span[@id="Table_2:_Unit-level_details"]]/following-sibling::table[1]')
        headers = [th.css('::text').get().strip() for th in info_table.css('tr th')]
        units = {header: [] for header in headers}

        for tr in info_table.css('tr')[1:]:
            for idx, td in enumerate(tr.css('td')):
                units[headers[idx]].append(td.css('::text').get().strip())

        # Parse the third table and combine its data with the existing units dictionary
        ownership_table = response.xpath('//h4[span[@id="Table_3:_Unit-level_ownership_and_operator_details"]]/following-sibling::table[1]')
        ownership_headers = [th.css('::text').get().strip() for th in ownership_table.css('tr th')[1:]]  # Exclude the first column

        # Add ownership headers to units dictionary if not already present
        for header in ownership_headers:
            if header not in units:
                units[header] = []

        for tr in ownership_table.css('tr')[1:]:
            for idx, td in enumerate(tr.css('td')[1:]):  # Exclude the first column
                units[ownership_headers[idx]].append(td.css('::text').get().strip())

        if response.css('div.mw-normal-catlinks li a::text').get() == 'Oil & Gas power stations':
            for tr in info_table.css('tr')[1:]:
                if 'gas' in tr.css('td:nth-child(3)::text').get() or 'oil' in tr.css('td:nth-child(3)::text').get():
                    loader.add_value('primary_fuel', tr.css('td:nth-child(3)::text').get(default=''))
                    loader.add_value('status', tr.css('td:nth-child(2)::text').get(default=''))
                    loader.add_value('year_commissioned', tr.css('td:nth-child(7)::text').get(default=''))
                    loader.add_value('technology', tr.css('td:nth-child(5)::text').get(default=''))

                    yield loader.load_item()
                    break

        for tr in info_table.css('tr')[1:]:
            if 'operating' in tr.css('td:nth-child(2)::text').get() or 'cancelled' in tr.css('td:nth-child(2)::text').get() or 'Phase I' in tr.css('td:nth-child(1)::text').get() or 'Unit 1' in tr.css('td:nth-child(1)::text').get():
                loader.add_value('primary_fuel', tr.css('td:nth-child(3)::text').get(default=''))
                loader.add_value('status', tr.css('td:nth-child(2)::text').get(default=''))
                loader.add_value('year_commissioned', tr.css('td:nth-child(6)::text').get(default=''))
                break

        loader.add_value('units', units)

        yield loader.load_item()

    def parse_details_geothermal(self, response):
        loader = response.meta['loader']

        table = response.xpath('//h2[span[@id="Project_Details"]]/following-sibling::table[1]')
        # Find the index of the 'Nameplate capacity' column
        header_row = table.css('tr')[0]
        capacity_index = None
        status_index = None
        year_index = None
        technology_index = None

        for idx, th in enumerate(header_row.css('th')):
            text = th.css('::text').get(default='')
            if 'Nameplate capacity' in text:
                capacity_index = idx + 1  # CSS nth-child is 1-based
            elif 'Status' in text:
                status_index = idx + 1
            elif 'Commissioning year' in text:
                year_index = idx + 1
            elif 'Technology' in text:
                technology_index = idx + 1

        if capacity_index is not None:
            capacity = 0
            for tr in table.css('tr')[1:]:
                str_capacity = tr.css(f'td:nth-child({capacity_index})::text').get()
                if str_capacity:
                    str_capacity = str_capacity.strip()[:-3]  # Remove the last 3 characters (e.g., ' MW')
                    capacity += int(str_capacity)
            loader.add_value('capacity', capacity)

        loc_table = response.xpath('//h2[span[@id="Location"]]/following-sibling::table[1]')

        location_index = None
        header_row = loc_table.css('tr')[0]
        for idx, th in enumerate(header_row.css('th')):
            text = th.css('::text').get(default='')
            if 'Location' in text:
                location_index = idx + 1

        if location_index is not None:
            location = location[0:-12].split(', ')
            location = loc_table.css(f'tr + tr td:nth-child({location_index})::text').get(default='')
            # sublocation is all except the last element
            sublocation = ', '.join(location[0:len(location)-1])
            loader.add_value('location', location[-1])
            loader.add_value('sublocation', sublocation)

        loader.add_value('plant_type', 'Geothermal')
        if status_index is not None:
            loader.add_value('status', table.css(f'tr + tr td:nth-child({status_index})::text').get(default=''))
        if year_index is not None:
            loader.add_value('year_commissioned', table.css(f'tr + tr td:nth-child({year_index})::text').get(default=''))
        if technology_index is not None:
            loader.add_value('technology', table.css(f'tr + tr td:nth-child({technology_index})::text').get(default=''))

        headers = [th.css('::text').get().strip() for th in table.css('tr th')]
        units = {header: [] for header in headers}

        for tr in table.css('tr')[1:]:
            for idx, td in enumerate(tr.css('td')):
                units[headers[idx]].append(td.css('::text').get().strip())
        loader.add_value('units', units)

        yield loader.load_item()
