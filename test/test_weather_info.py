import requests as req
import pytest
import logging

import os.path
import sys

dirname = os.path.dirname
sys.path.append(dirname(dirname(dirname(__file__))))


from datetime import datetime
from WeatherServer.api import Province, City, Country,\
                RealTimeInfo, TodayInfo, AqiInfo,\
                IndexInfo, Forecast, WeatherInfo


@pytest.fixture
def json():
    url = 'http://weatherapi.market.xiaomi.com/wtr-v2/weather?cityId=101121402'
    resp = req.get(url=url)
    resp.encoding = 'utf-8'
    return resp.json()


def test(json):
    date = json['today']['date']
    city_name = json['forecast']['city']
    country = Country.objects(name=city_name).first()
    country.weather_infos = []
    print(country)
    weather_info = \
        WeatherInfo(date=datetime.strptime('2016-06-14', '%Y-%m-%d'))
    weather_info.today = get_today(json['today'])
    weather_info.aqi = get_aqi(json['aqi'])
    country.weather_infos.append(weather_info)
    country.save()


def get_today(data):
    today = TodayInfo(
                    humidity_max=data['humidityMax'],
                    humidity_min=data['humidityMin'],
                    temp_max=data['tempMax'],
                    temp_min=data['tempMin'],
                    weather_end=data['weatherEnd'],
                    weather_start=data['weatherStart'],
                    wind_direction_end=data['windDirectionEnd'],
                    wind_direction_start=data['windDirectionStart'],
                    wind_max=data['windMax'],
                    wind_min=data['windMin']
                )
    return today
    # weather_info.save()


def get_aqi(data):
    datestr = data['pub_time']
    date = datetime.strptime(datestr, '%Y-%m-%d %H:%M')
    aqi = AqiInfo(
            pub_date=date,
            aqi=data['aqi'],
            pm25=data['pm25'],
            pm10=data['pm10'],
            so2=data['so2'],
            no2=data['no2'],
            source=data['src'],
            spot=data['spot']
        )
    return aqi

if __name__ == '__main__':
    test(json())
