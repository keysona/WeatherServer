#!/bin/bash
cd WeatherSpider/WeatherSpider
scrapy crawl provinces
scrapy crawl cities
scrapy crawl countries
cd ../..
