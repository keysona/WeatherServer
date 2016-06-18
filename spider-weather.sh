#!/bin/bash
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

workon weather-server
cd WeatherSpider
scrapy crawl --logfile=weather.log -L ERROR weather-info
cd ..
