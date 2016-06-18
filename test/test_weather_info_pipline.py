# -*- coding: utf-8 -*-
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


logger = logging.getLogger(__name__)


class WeatherInfoSpiderPipeline:

    def process_item(self, item, spider):

        if spider.name != 'weather-info':
            return

        country = Country.objects(location_id=item['location_id']).first()
        if not country:
            logger.error('%s location_id is invalid' % item['location_id'])
            return

        self.progress_weather_info(country, item['data'])

    def progress_weather_info(self, country, data):
        date = data['today']['date']

        # maybe no data!
        if not date:
            logger.error('%s-%s-%s no data' % (country.name,
                                               country.location_id,
                                               country.weather_id))
            return

        _datetime = datetime.strptime(date, '%Y-%m-%d')
        weather_info = country.weather_infos.filter(datetime=_datetime).first()
        if not weather_info:
            weather_info = self.get_weather_info(_datetime, data)
            country.weather_infos.append(weather_info)
        else:
            logger.debug('update weather info')
            self.update_weather_info(weather_info, data)
        country.save()

    def get_weather_info(self, _datetime, data):
        weather_info = \
            WeatherInfo(datetime=_datetime,
                        week=data['forecast']['week'],
                        today=self.get_today(data['today']),
                        realtime=self.get_realtime(data['realtime']),
                        aqi=self.get_aqi(data['aqi']),
                        index=self.get_index(data['index']),
                        forecast=self.get_forecast(data['forecast']))
        return weather_info

    def update_weather_info(self, weather_info, data):

        self.update_realtime(weather_info, data['realtime'])

        self.update_aqi(weather_info, data['aqi'])

    def update_realtime(self, weather_info, data):
        _time = datetime.strptime(data['time'], '%H:%M')
        print("realtime: %s | %s" % (weather_info.realtime.time, _time))
        if weather_info.realtime.time != _time:
            logger.debug('update realtime info')
            weather_info.realtime = self.get_realtime(data)

    def update_aqi(self, weather_info, data):
        datestr = data['pub_time']
        _datetime = datetime.strptime(datestr, '%Y-%m-%d %H:%M')
        print("aqi: %s | %s" % (weather_info.aqi.pub_date, _datetime))
        if weather_info.aqi.pub_date != _datetime:
            logger.debug('update aqi')
            weather_info.aqi = self.get_aqi(data)

    def get_today(self, data):
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

    def get_aqi(self, data):

        # may be no aqi
        if 'pub_time' not in data:
            logger.error('no aqi data')
            return

        datestr = data['pub_time']
        _datetime = datetime.strptime(datestr, '%Y-%m-%d %H:%M')
        aqi = AqiInfo(
                pub_date=_datetime,
                aqi=data['aqi'],
                pm25=data['pm25'],
                pm10=data['pm10'],
                so2=data['so2'],
                no2=data['no2'],
                source=data['src'],
                spot=data['spot']
            )
        return aqi

    def get_realtime(self, data):
        _time = datetime.strptime(data['time'], '%H:%M')
        realtime = RealTimeInfo(
                humidity=data['SD'],
                wind_direction=data['WD'],
                wind_speed=data['WS'],
                temp=data['temp'],
                time=_time,
                weather=data['weather']
            )
        return realtime

    def get_index(self, data):
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

    def get_forecast(self, data):
        res = []
        for i in range(1, 7):
            forecast = Forecast(
                            wind=data['fl%s' % str(i)],
                            wind_detail=data['wind%s' % str(i)],
                            temp=data['temp%s' % str(i)],
                            weather=data['weather%s' % str(i)],
                            week=self.get_week(data['week'], i)
                            )
            res.append(forecast)
        return res

    def get_week(self, week, offset):
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


class Spider:
    name = 'weather-info'


def test():
    url = 'http://weatherapi.market.xiaomi.com/wtr-v2/weather?cityId=101121301'
    resp = req.get(url=url)
    resp.encoding = 'utf-8'
    data = resp.json()
    item = {
        'data': data,
        'location_id': '121301'
        }

    print(data)
    spider = Spider()
    pipline = WeatherInfoSpiderPipeline()
    pipline.process_item(item, spider)

if __name__ == '__main__':
    test()
