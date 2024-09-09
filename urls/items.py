# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# Items for PowerPlants from global energy spider
class GlobalEnergySpiderItem(scrapy.Item):
    name = scrapy.Field()
    source = scrapy.Field()
    capacity = scrapy.Field()
    location = scrapy.Field()
    sublocation = scrapy.Field()
    plant_type = scrapy.Field()
    primary_fuel = scrapy.Field()
    secondary_fuel = scrapy.Field()
    status = scrapy.Field()
    capital_cost = scrapy.Field()
    cost_usd = scrapy.Field()
    year_commissioned = scrapy.Field()


class WikiSpiderItem(scrapy.Item):
    name = scrapy.Field()
    source = scrapy.Field()
    capacity = scrapy.Field()
    location = scrapy.Field()
    sublocation = scrapy.Field()
    plant_type = scrapy.Field()
    primary_fuel = scrapy.Field()
    status = scrapy.Field()


class GemWikiSpider(scrapy.Item):
    name = scrapy.Field()
    source = scrapy.Field()
    capacity = scrapy.Field()
    location = scrapy.Field()
    sublocation = scrapy.Field()
    plant_type = scrapy.Field()
    primary_fuel = scrapy.Field()
    status = scrapy.Field()
    year_commissioned = scrapy.Field()
    technology = scrapy.Field()
    units = scrapy.Field()

class CommonPowerSpiderItem(scrapy.Item):
    name = scrapy.Field()
    capacity = scrapy.Field()
    location = scrapy.Field()
    sublocation = scrapy.Field()
    plant_type = scrapy.Field()
    primary_fuel = scrapy.Field()
    secondary_fuel = scrapy.Field()
    status = scrapy.Field()
    capital_cost = scrapy.Field()
    cost_usd = scrapy.Field()
    year_commissioned = scrapy.Field()
    units = scrapy.Field()
    technology = scrapy.Field()
    source = scrapy.Field()