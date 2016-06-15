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
        self.logging = spider.logger
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
        city = City.objects(location_id=data['id']).first()
        if city:
            return city

        city = City(
                location_id=data['id'],
                name=data['name'],
                countries=[]
            )
        city.save()
        # add to province
        # for example:
        # city['location_id'] = 2903
        # city['location_id'][:2] = 29
        # 29 is the number of province that the city belongs to.
        location_id = city['location_id'][:2]
        province = Province.objects(location_id=location_id).first()
        if city not in province.cities:
            province.cities.append(city)
            province.save()
        return city

    def progress_country(self, data):
        country = Country.objects(location_id=data['id']).first()
        if country:
            return country

        country = Country(
                        location_id=data['id'],
                        weather_id=data['weather_id'],
                        name=data['name'],
                        weather_infos=[]
                    )
        country.save()

        # add to city
        # for example:
        # country['location_id'] = 290102
        # country['location_id'][:4] = 2901
        # 2901 is the number of city that the country belongs to.
        location_id = country['location_id'][:4]
        city = City.objects(location_id=location_id).first()
        if country not in city.countries:
            city.countries.append(country)
            city.save()
        return country
