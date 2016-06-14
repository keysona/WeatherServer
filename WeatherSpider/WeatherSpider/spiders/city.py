import scrapy
import json


class LocationSpider(scrapy.Spider):

    name = 'location'
    allowed_domains = ["tianqi.cn"]
    start_urls = [
        'http://3g.tianqi.cn/getAllCitys.do'
        ]

    def parse(self, response):
        items = json.loads(response.text)
        # self.logger.info(items)
        for item in items:
            yield item


class WeatherInfoSpider(scrapy.Spider):
    name = 'weather'
    base_url =

    def start_requests():
