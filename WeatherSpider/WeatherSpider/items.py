# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Province(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()


class City(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()


class Country(scrapy.Item):
    id = scrapy.Field()
    weather_id = scrapy.Field()
    name = scrapy.Field()
