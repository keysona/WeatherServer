#!/bin/bash
echo '************************'
echo 'Start crawl weather data'
echo `date`
SCRIPT_DIR=$(dirname ${0})
PROJECT_DIR=$(dirname ${SCRIPT_DIR})
source ${SCRIPT_DIR}/env.sh

workon weather-server
cd $PROJECT_DIR
cd WeatherSpider
scrapy crawl --logfile=weather.log -L ERROR weather-info
cd $PROJECT_DIR
echo `date`
echo '************************'
