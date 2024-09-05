import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class GlobalEnergyItemsLoader(ItemLoader):
    default_output_processor = TakeFirst()


class WikiItemsLoader(ItemLoader):
    default_output_processor = TakeFirst()