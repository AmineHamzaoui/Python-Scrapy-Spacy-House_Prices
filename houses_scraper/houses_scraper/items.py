# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HousesScraperItem(scrapy.Item):
     #define the fields for your item here like:
    name = scrapy.Field()
    pass


class HouseItem(scrapy.Item):
    url = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    city_region = scrapy.Field()
    rooms=scrapy.Field()
    size=scrapy.Field()
    bathrooms=scrapy.Field()
    living_areas=scrapy.Field()
    bedrooms=scrapy.Field()
    type_of_property=scrapy.Field()
    city = scrapy.Field()
    region = scrapy.Field()