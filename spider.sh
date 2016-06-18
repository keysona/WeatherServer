#!/bin/bash
cd WeatherSpider/WeatherSpider
scrapy crawl --logfile=location.log -L ERROR provinces
scrapy crawl --logfile=location.log -L ERROR cities
scrapy crawl --logfile=location.log -L ERROR countries
py.test
cd ../..
