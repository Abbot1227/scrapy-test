# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# Items for PowerPlants from global energy spider
class GlobalEnergySpiderItem(scrapy.Item):
    name = scrapy.Field()
    capacity = scrapy.Field()
    location = scrapy.Field()
    sublocation = scrapy.Field()
    plant_type = scrapy.Field()
    primary_fuel = scrapy.Field()
    secondary_fuel = scrapy.Field()


class WikiSpiderItem(scrapy.Item):
    name = scrapy.Field()
    capacity = scrapy.Field()
    location = scrapy.Field()
    sublocation = scrapy.Field()