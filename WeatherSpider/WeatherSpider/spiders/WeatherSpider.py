import scrapy
import json
from WeatherSpider import Country


class WeatherInfoSpider(scrapy.Spider):

    name = 'weather-info'
    base_url = 'http://weatherapi.market.xiaomi.com/wtr-v2/weather?cityId=%s'

    def make_url(self, weather_id):
        return self.base_url % weather_id

    def start_requests(self):
        for country in Country.objects:
            yield scrapy.Request(url=self.make_url(country.weather_id),
                                 meta={
                                    'location_id': country.location_id
                                 },
                                 callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        location_id = response.meta['location_id']
        yield {
            'data': data,
            'location_id': location_id
            }
