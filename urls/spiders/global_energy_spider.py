from scrapy import Spider

from urls.start_urls import global_energy_observatory_urls
from urls.itemsloaders import GlobalEnergyItemsLoader
from urls.items import GlobalEnergySpiderItem


class GlobalEnergySpider(Spider):
    name = 'global_energy'
    allowed_domains = ['globalenergyobservatory.org']
    start_urls = global_energy_observatory_urls

    def parse(self, response):
        for row in response.css('tr'):
            country = row.css('td:nth-child(3) label::text').get()
            if country and country.strip() == 'Indonesia':
                loader = GlobalEnergyItemsLoader(item=GlobalEnergySpiderItem(), selector=row)
                loader.add_value('name', row.css('td:nth-child(1) a::text').get())
                # creating absolute url for description page
                details_link = row.css('td:nth-child(1) a::attr(href)').get()
                details_link = response.urljoin(details_link)
                loader.add_value('source', details_link)
                loader.add_value('capacity', row.css('td:nth-child(2) label::text').get())
                loader.add_value('location', row.css('td:nth-child(4) label::text').get())

                yield response.follow(url=details_link,
                                      callback=self.parse_details,
                                      meta={'loader': loader})

    def parse_details(self, response):
        loader = response.meta['loader']
        loader.add_value('sublocation', response.css( 'input#Location::attr(value)').get())
        loader.add_value('plant_type', response.css('select#Type_of_Plant_enumfield_rng1 option[selected]::text').get())
        loader.add_value('primary_fuel', response.css(' input#Type_of_Fuel_rng1_Primary::attr(value)').get())
        loader.add_value('secondary_fuel', response.css('select#Type_of_Fuel_enumfield_rng2_Secondary option[selected]::text').get())
        loader.add_value('status', response.css('select#Status_of_Plant_enumfield_itf option[selected]::text').get())
        loader.add_value('capital_cost', response.css('input#Capital_Cost_of_Plant_nbr_rng1::attr(value)').get(default=''))
        loader.add_value('cost_usd', response.css('input#Capital_Cost_of_Plant_rng2_and\/or_In_US_Dollars_nbr::attr(value)').get(default=''))
        loader.add_value('year_commissioned', response.css('input#Capital_Cost_Currency_rng3_In_Year_\(YYYY\)_yr::attr(value)').get(default=''))

        yield loader.load_item()
