#!/bin/bash

SCRIPT_DIR=$(dirname ${0})
PROJECT_DIR=$(dirname ${SCRIPT_DIR})

source $SCRIPT_DIR/env.sh
workon weather-server

cd $PROJECT_DIR
cd WeatherSpider/
scrapy crawl --logfile=location.log -L ERROR provinces
scrapy crawl --logfile=location.log -L ERROR cities
scrapy crawl --logfile=location.log -L ERROR countries
cd $PROJECT_DIR
py.test
