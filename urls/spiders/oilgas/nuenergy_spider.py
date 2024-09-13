from pandas.core.internals.construction import reorder_arrays
from scrapy import Spider
from twisted.words.protocols.jabber.xmpp_stringprep import resourceprep

from urls.items import OilGasItem
from urls.itemsloaders import NuEnergyItemsLoader

from urls.utils import nuenergy_clear


class NuenergySpider(Spider):
    name = "nuenergy"
    allowed_domains = ['www.nuenergygas.com']
    start_urls = ['https://www.nuenergygas.com/tanjung-enim-PSC.php',
                  'https://www.nuenergygas.com/muara-enim-PSC.php',
                  'https://www.nuenergygas.com/muara-enim-II-PSC.php',
                  'https://www.nuenergygas.com/muralim-PSC.php',
                  'https://www.nuenergygas.com/rengat-PSC.php']

    def parse(self, response):
        loader = NuEnergyItemsLoader(item=OilGasItem(), response=response)
        loader.add_value('name', response.css('h3.pageTitle::text').get())
        loader.add_value('source', response.url)

        location = response.css('h5 + ul li::text').get(default='')
        loader.add_value('location', location)

        loader.add_value('site_size', response.css('h5 span::text').get(default=''))

        announced_year = response.css('h3.pageTitle + p::text').get()
        year, contract_years = nuenergy_clear(announced_year)
        print(year, contract_years)
        loader.add_value('announced_year', f'{year} - {contract_years}')

        # Contractors
        contractors_table = response.css('table.projectdetails-table')
        contractors = ''
        for tr in contractors_table.css('tr'):
            name = tr.css('td + td::text').get()
            percentage = tr.css('td + td + td::text').get()

            contractors += f'{name} - {percentage}\n'
        loader.add_value('owner', contractors)

        # Resources:
        resources_table = response.css('table ~ table')
        gas_capacity = ''
        for tr in resources_table.css('tr'):
            if tr.css('td li::text').get() == 'Gas In Place':
                loader.add_value('gas_reserve', tr.css('td + td::text').get())
            else:
                name = tr.css('td li::text').get()
                capacity = tr.css('td + td::text').get()
                gas_capacity = f'{name} - {capacity}\n'
        loader.add_value('reserves', gas_capacity)

        loader.add_value('website', 'https://www.nuenergygas.com/index.php')

        yield loader.load_item()