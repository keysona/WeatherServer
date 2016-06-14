import scrapy
import json


class BaseSpider(scrapy.Spider):
    allow_domains = ['weather.com.cn']
    start_urls = [
            'http://www.weather.com.cn/data/list3/city.xml'
        ]
    base_url = 'http://www.weather.com.cn/data/list3/city%s.xml'

    def _make_url(self, id):
        return self.base_url % id


class ProvincesSpider(BaseSpider):

    name = 'provinces'

    def parse(self, response):
        # pase provinces
        for item in response.text.split(','):
            id, name = item.split('|')
            yield {
                    'id': id,
                    'name': name
                }


class CitiesSpider(BaseSpider):

    name = 'cities'

    def parse(self, response):
        # pase provinces
        for item in response.text.split(','):
            id, name = item.split('|')
            url = self._make_url(id)
            yield scrapy.Request(url, callback=self.parse_cities)

    def parse_cities(self, response):
        for item in response.text.split(','):
            id, name = item.split('|')
            yield {
                    'id': id,
                    'name': name
                }


class CountryiesSpider(BaseSpider):

    name = 'countries'

    def parse(self, response):
        # pase provinces
        for item in response.text.split(','):
            id, name = item.split('|')
            url = self._make_url(id)
            yield scrapy.Request(url, callback=self.parse_cities)

    def parse_cities(self, response):
        for item in response.text.split(','):
            id, name = item.split('|')
            url = self._make_url(id)
            yield scrapy.Request(url, callback=self.parse_countries)

    def parse_countries(self, response):
        for item in response.text.split(','):
            id, name = item.split('|')
            url = self._make_url(id)
            yield scrapy.Request(url, callback=self.parse_weather_num,
                                 meta={'name': name})

    def parse_weather_num(self, response):
        name = response.meta['name']
        for item in response.text.split(','):
            id, weather_id = item.split('|')
            yield {
                    'id': id,
                    'weather_id': weather_id,
                    'name': name
                }
