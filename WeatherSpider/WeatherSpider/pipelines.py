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
        if spider.name == 'provinces':
            return self.progress_province(item)
        elif spider.name == 'cities':
            return self.progress_city(item)
        elif spider.name == 'countries':
            return self.progress_country(item)
        else:
            return item

    def progress_province(self, data):
        province = Province.objects(location_id=data['id']).first()
        if province:
            return province

        province = Province(
                        location_id=data['id'],
                        name=data['name'],
                        cities=[]
                    )
        province.save()
        return province

    def progress_city(self, data):
        city = City.objects(location_id=data['id']).firse()
        if city:
            return city

        city = City(
                location_id=data['id'],
                name=data['ch'],
                countries=[]
            )
        city.save()
        return city

    def progress_country(self, data):
        country = Country.objects(location_id=data['id']).first()
        if country:
            return country

        country = Country(
                        location_id=data['id'],
                        weather_id=data['id'],
                        name=data['name'],
                    )
        country.save()
        return country
