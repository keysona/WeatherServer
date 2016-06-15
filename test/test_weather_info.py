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
    _datetime = datetime.strptime(date, '%Y-%m-%d')
    city_name = json['forecast']['city']
    country = Country.objects(name=city_name).first()
    print(country)
    if not country.weather_infos.filter(date=_datetime):
        weather_info = \
            WeatherInfo(date=_datetime,
                        week=json['forecast']['week'],
                        today=get_today(json['today']),
                        realtime=get_realtime(json['realtime']),
                        aqi=get_aqi(json['aqi']),
                        index=get_index(json['index']),
                        forecast=get_forecast(json['forecast']))
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


def get_realtime(data):
    time = datetime.strptime(data['time'], '%H:%M')
    realtime = RealTimeInfo(
            humidity=data['SD'],
            wind_direction=data['WD'],
            wind_speed=data['WS'],
            temp=data['temp'],
            time=time,
            weather=data['weather']
        )
    return realtime


def get_index(data):
    res = []
    for item in data:
        index = IndexInfo(
                        code=item['code'],
                        details=item['details'],
                        index=item['index'],
                        name=item['name']
                    )
        res.append(index)
    return res


def get_forecast(data):
    res = []
    for i in range(1, 7):
        forecast = Forecast(
                        wind=data['fl%s' % str(i)],
                        wind_detail=data['wind%s' % str(i)],
                        temp=data['temp%s' % str(i)],
                        weather=data['weather%s' % str(i)],
                        week=get_week(data['week'], i)
                        )
        res.append(forecast)
    return res


def get_week(week, offset):
    weeks_to_int = {
        '星期一': 0,
        '星期二': 1,
        '星期三': 2,
        '星期四': 3,
        '星期五': 4,
        '星期六': 5,
        '星期日': 6
        }
    int_to_weeks = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期日'
        }
    mod = (weeks_to_int[week] + offset) % 7
    return int_to_weeks[mod]


def test_get_week():
    assert get_week('星期一', 3) == '星期四'

    assert get_week('星期日', 4) == '星期四'

if __name__ == '__main__':
    test(json())
