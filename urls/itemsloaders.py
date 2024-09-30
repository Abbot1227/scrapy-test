import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst


class GlobalEnergyItemsLoader(ItemLoader):
    default_output_processor = TakeFirst()


class WikiItemsLoader(ItemLoader):
    default_output_processor = TakeFirst()


class GemWikiItemsLoader(ItemLoader):
    default_output_processor = TakeFirst()

class NuEnergyItemsLoader(ItemLoader):
    default_output_processor = TakeFirst()

class WikiMineItemsLoader(ItemLoader):
    default_output_processor = TakeFirst()

class WaterItemsLoader(ItemLoader):
    default_output_processor = TakeFirst()
