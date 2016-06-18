#!/bin/bash
cd WeatherSpider/
scrapy crawl --logfile=location.log -L ERROR provinces
scrapy crawl --logfile=location.log -L ERROR cities
scrapy crawl --logfile=location.log -L ERROR countries
cd ..
py.test
