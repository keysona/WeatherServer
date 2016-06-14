# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from WeatherSpider import Province, City, Country

logger = logging.getLogger(__name__)


class WeatherspiderPipeline(object):

    def process_item(self, item, spider):
        pass

    def process_province(self, item):
        if 'ch' not in item:
            return item
        else:
            province = self.progress_province(item)
            logger.info(province)
            return province

    def progress_province(self, data):
        province = Province(
                        weather_id=data['id'],
                        ch=data['ch'],
                        en=data['en'],
                        cities=[]
                    )
        for item in data['beans']:
            city = self.progress_city(item)
            province.cities.append(city)
        province.save()
        return province

    def progress_city(self, data):
        city = City(
                weather_id=data['id'],
                ch=data['ch'],
                en=data['en'],
                countries=[]
            )
        for item in data['beans']:
            country = self.progress_country(item)
            city.countries.append(country)
        city.save()
        return city

    def progress_country(self, data):
        country = Country(
                        weather_id=data['id'],
                        ch=data['ch'],
                        en=data['en']
                    )
        country.save()
        return country
