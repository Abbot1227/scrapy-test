from scrapy import Spider

from urls.items import OilGasItem
from urls.itemsloaders import GemWikiItemsLoader


class GemWikiOilGasSpider(Spider):
    name = "gemoilgas"
    allowed_domains = ['www.gem.wiki']
    start_urls = ['https://www.gem.wiki/Category:Oil_and_gas_extraction_in_Indonesia']


    def parse(self, response):
        for li in response.css('div.mw-category li'):
            loader = GemWikiItemsLoader(item=OilGasItem(), selector=li)

            loader.add_value('name', li.css('a::text').get())
            details_link = li.css('a::attr(href)').get()
            details_link = response.urljoin(details_link)
            loader.add_value('source', details_link)

            yield response.follow(url=details_link, callback=self.parse_details, meta={'loader': loader})


    def parse_details(self, response):
        loader = response.meta['loader']

        loc_table = response.xpath('//h2[span[@id="Location"]]/following-sibling::table[1]')

        # Searching for location header in the table
        loc_index = None
        for idx, th in enumerate(loc_table.css('tr th')):
            if th.css('::text').get().strip() == 'Location':
                loc_index = idx+1
                break

        if loc_index is not None:
            province = loc_table.css(f'tr + tr td:nth-child({loc_index})::text').get()
            block = loc_table.css('tr + tr td:first-child::text').get()
            location = province.split(', ')
            loader.add_value('province', block)
            loader.add_value('location', location[0])

        # Main Data table
        data_table = response.xpath('//h3[span[@id="Main_Data"]]/following-sibling::table[1]')
        status_idx = None
        operator_idx = None
        owner_idx = None
        discovery_year_idx = None
        prodstart_year_idx = None

        for idx, th in enumerate(data_table.css('tr th')):
            # Name of each table header
            text = th.css('::text').get().strip()
            if text == 'Status':
                status_idx = idx + 1
            elif text == 'Operator':
                operator_idx = idx + 1
            elif text == 'Owner':
                owner_idx = idx + 1
            elif text == 'Discovery year':
                discovery_year_idx = idx + 1
            elif text == 'Production start year':
                prodstart_year_idx = idx + 1

        if status_idx is not None:
            loader.add_value('status', data_table.css(f'tr + tr td:nth-child({status_idx})::text').get())
        if operator_idx is not None:
            loader.add_value('operator', data_table.css(f'tr + tr td:nth-child({operator_idx})::text').get())
        if owner_idx is not None:
            loader.add_value('owner', data_table.css(f'tr + tr td:nth-child({owner_idx})::text').get())
        if discovery_year_idx is not None:
            loader.add_value('discovery_year', data_table.css(f'tr + tr td:nth-child({discovery_year_idx})::text').get())
        if prodstart_year_idx is not None:
            loader.add_value('production_year', data_table.css(f'tr + tr td:nth-child({prodstart_year_idx})::text').get())

        # Production and/or Reserves
        reserve_table = response.xpath('//h3[span[@id="Production_and_Reserves"]]/following-sibling::table[1]')
        fuel_idx = None
        classification_idx = None
        quantity_idx = None
        units_idx = None
        data_year_idx = None

        for idx, th in enumerate(reserve_table.css('tr th')):
            text = th.css('::text').get().strip()
            if text == 'Fuel Description':
                fuel_idx = idx + 1
            elif text == 'Reserve Classification':
                classification_idx = idx + 1
            elif text == 'Quantity':
                quantity_idx = idx + 1
            elif text == 'Units':
                units_idx = idx + 1
            elif text == 'Data Year':
                data_year_idx = idx + 1

        prod_table = response.xpath('//h3[span[@id="Production_and_Reserves"]]/following-sibling::table[2]')
        if prod_table.css('tr th::text').get() == 'Category':
            category_idx = None
            fuel_desc_idx = None
            quantity_prod_idx = None
            units_prod_idx = None
            year_prod_idx = None

            for idx, th in enumerate(prod_table.css('tr th')):
                text = th.css('::text').get().strip()
                if text == 'Category':
                    category_idx = idx + 1
                elif text == 'Fuel Description':
                    fuel_desc_idx = idx + 1
                elif text == 'Quantity':
                    quantity_prod_idx = idx + 1
                elif text == 'Units':
                    units_prod_idx = idx + 1
                elif text == 'Data Year':
                    year_prod_idx = idx + 1

            production = ''
            for tr in prod_table.css('tr')[1:]:
                if category_idx is not None:
                    production += tr.css(f'td:nth-child({category_idx})::text').get() + ' - '
                if fuel_desc_idx is not None:
                    production += tr.css(f'td:nth-child({fuel_desc_idx})::text').get() + ' - '
                if quantity_prod_idx is not None:
                    production += tr.css(f'td:nth-child({quantity_prod_idx})::text').get() + ' '
                if units_prod_idx is not None:
                    production += tr.css(f'td:nth-child({units_prod_idx})::text').get() + ' - '
                if year_prod_idx is not None:
                    production += tr.css(f'td:nth-child({year_prod_idx})::text').get() + '\n'
            loader.add_value('production', production)

        reserves = ''
        for tr in reserve_table.css('tr')[1:]:
            if fuel_idx is not None:
                reserves += tr.css(f'td:nth-child({fuel_idx})::text').get() + ' - '
            if classification_idx is not None:
                reserves += tr.css(f'td:nth-child({classification_idx})::text').get() + ' - '
            if quantity_idx is not None:
                reserves += tr.css(f'td:nth-child({quantity_idx})::text').get() + ' '
            if units_idx is not None:
                reserves += tr.css(f'td:nth-child({units_idx})::text').get() + ' - '
            if data_year_idx is not None:
                reserves += tr.css(f'td:nth-child({data_year_idx})::text').get() + '\n'
        loader.add_value('reserves', reserves)

        yield loader.load_item()