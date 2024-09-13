from typing import Any

from scrapy import Spider
from scrapy.http import Response

from urls.itemsloaders import WikiMineItemsLoader

from urls.items import MiningItem


class MiningTechnologySpider(Spider):
    name = "mining_tech"
    allowed_domains = ["www.mining-technology.com"]
    start_urls = [
        "https://www.mining-technology.com/projects/mabilo-copper-gold-project/",
        "https://www.mining-technology.com/projects/grasbergopenpit/",
        "https://www.mining-technology.com/projects/martabe/",
        "https://www.mining-technology.com/projects/kaltim/",
        "https://www.mining-technology.com/projects/batu/",
        "https://www.mining-technology.com/projects/pani-gold-project-sulawesi-indonesia/",
        "https://www.mining-technology.com/projects/tujuh-bukit-copper-project-east-java-province-indonesia/",
        "https://www.mining-technology.com/projects/awak-mas-gold-project/"
    ]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        loader = WikiMineItemsLoader(item=MiningItem(), response=response)
        loader.add_value('name', response.css('h1.article-header__title::text').get())
        loader.add_value('source', response.url)

        production = ''
        for div in response.css('div.info-box'):

            text = div.css('h5::text').get()
            if text == 'Location':
                location = div.css('p::text').get()
                location = location.split(', ')
                loader.add_value('province', location[len(location) - 1])
                loader.add_value('location', location[0])
            elif text == 'Produce' or text == 'Producer of' or text == 'Mineral Types':
                loader.add_value('products', div.css('p::text').get())
            elif text == 'Mine Type' or text == 'Mining method' or text == 'Mining':
                loader.add_value('type', div.css('p::text').get())
            elif text == 'Ownership':
                loader.add_value('company', div.css('p::text').get())
            elif text == 'Operator' or text == 'Contractor' or text == 'Contractors' or text == 'Developers':
                loader.add_value('contractor', div.css('p::text').get())
            elif text == 'Geology type' or text == 'Geology Type':
                loader.add_value('geology_type', div.css('p::text').get())
            elif text == 'Mineral type' or text == 'Mineral Type':
                loader.add_value('mineral_type', div.css('p::text').get())
            elif text == 'Reserve base' or text == 'Reserves' or text == 'Reserve Base':
                loader.add_value('reserve', div.css('p::text').get())
            elif text == 'First production':
                loader.add_value('financial_year', div.css('p::text').get())
            elif text == 'Mine life':
                loader.add_value('closed', div.css('p::text').get())
            elif text == 'Production':
                loader.add_value('production', div.css('p::text').get())
            elif text in ['Copper', 'Gold', 'Coal', 'Silver', 'Nickel', 'Zinc', 'Lead', 'Iron', 'Bauxite', 'Tin']:
                production += f"{text}: {div.css('p::text').get()}\n"
            elif text == 'Process Infrastructure/Equipment' or text == 'Processing method':
                loader.add_value('technology', div.css('p::text').get())
            elif text == 'Employment':
                loader.add_value('employment', div.css('p::text').get())

        if production != '':
            loader.add_value('production', production)

        yield loader.load_item()
