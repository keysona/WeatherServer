# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from datetime import datetime
from WeatherSpider import Province, City, Country,\
                RealTimeInfo, TodayInfo, AqiInfo,\
                IndexInfo, Forecast, WeatherInfo,\
                WeatherHistoryInfo, WeatherHistory,\
                now_china


class WeatherHistoryPipline(object):

    def process_item(self, item, spider):
        self.logger = spider.logger
        if spider.name != 'weather-history':
            return item

        country = WeatherHistory.objects(country=item['country']).first()
        if not country:
            country = WeatherHistory(country=item['country'])
            country.save()

        for data in item['weathers']:
            _datetime = datetime.strptime(data['date'], '%Y-%m-%d')
            if country.history_infos.filter(datetime=_datetime):
                self.logger.debug('<%s> %s has been insert' % (country.country,
                                                               data['date']))
            weather = WeatherHistoryInfo(date=data['date'],
                                         datetime=_datetime,
                                         temp_max=data['temp_max'],
                                         temp_min=data['temp_min'],
                                         weather=data['weather'],
                                         wind_direction=data['wind_direction'],
                                         wind_speed=data['wind_speed'],
                                         )
            country.history_infos.append(weather)
        country.save()
        self.logger.debug('save success: <%s> %s' % (item['country'], item['weathers'][0]['date']))


class WeatherLocationSpiderPipeline(object):


    def process_item(self, item, spider):
        self.logger = spider.logger
        self.logger.debug('item : %s' % item)
        if spider.name == 'provinces':
            return self.progress_province(item)
        elif spider.name == 'cities':
            return self.progress_city(item)
        elif spider.name == 'countries':
            return self.progress_country(item)
        else:
            return item

    def progress_province(self, data):
        self.logger.debug('data[id] : %s ' % data)
        province = Province.objects(location_id=data['id'])
        if province:
            return province[0]

        province = Province(
                        location_id=data['id'],
                        name=data['name'],
                        cities=[]
                    )
        province.save()
        return province

    def progress_city(self, data):
        city = City.objects(location_id=data['id'])
        if city:
            return city[0]

        city = City(
                location_id=data['id'],
                name=data['name'],
                countries=[]
            )
        city.save()
        # add to province
        # for example:
        # city['location_id'] = 2903
        # city['location_id'][:2] = 29
        # 29 is the number of province that the city belongs to.
        location_id = city['location_id'][:2]
        province = Province.objects(location_id=location_id).first()
        if city not in province.cities:
            province.cities.append(city)
            province.save()
        return city

    def progress_country(self, data):
        country = Country.objects(location_id=data['id'])
        if country:
            return country[0]

        country = Country(
                        location_id=data['id'],
                        weather_id=data['weather_id'],
                        name=data['name'],
                        weather_infos=[]
                    )
        country.save()

        # add to city
        # for example:
        # country['location_id'] = 290102
        # country['location_id'][:4] = 2901
        # 2901 is the number of city that the country belongs to.
        location_id = country['location_id'][:4]
        city = City.objects(location_id=location_id).first()
        if country not in city.countries:
            city.countries.append(country)
            city.save()
        return country


class WeatherInfoSpiderPipeline(object):

    def process_item(self, item, spider):
        self.logger = spider.logger
        if spider.name != 'weather-info':
            return item

        country = Country.objects(location_id=item['location_id']).first()
        if not country:
            self.logger.error('%s location_id is invalid'
                              % item['location_id'])
            return item

        self.progress_weather_info(country, item['data'])

    def progress_weather_info(self, country, data):
        date = data['today']['date']

        # maybe no data!
        if not date:
            self.logger.error('%s-%s-%s no data' % (country.name,
                                                    country.location_id,
                                                    country.weather_id))
            return

        _datetime = datetime.strptime(date, '%Y-%m-%d')
        weather_info = country.weather_infos.filter(datetime=_datetime).first()
        if not weather_info:
            weather_info = self.get_weather_info(_datetime, data)
            country.weather_infos.append(weather_info)
        else:
            self.update_weather_info(weather_info, data)
        country.save()

    def get_weather_info(self, _datetime, data):
        weather_info = \
            WeatherInfo(datetime=_datetime,
                        week=self.now_week(),
                        today=self.get_today(data['today']),
                        realtime=self.get_realtime(data['realtime']),
                        aqi=self.get_aqi(data['aqi']),
                        index=self.get_index(data['index']),
                        forecast=self.get_forecast(data['forecast']))
        self.logger.debug(weather_info['week'])
        return weather_info

    def update_weather_info(self, weather_info, data):

        self.update_realtime(weather_info, data['realtime'])

        if self.has_aqi(data['aqi']):
            self.update_aqi(weather_info, data['aqi'])

    def has_aqi(self, aqi):
        if aqi:
            self.logger.debug('no aqi data')
            return True
        return False

    def update_realtime(self, weather_info, data):
        _time = datetime.strptime(data['time'], '%H:%M')
        if weather_info.realtime.time != _time:
            self.logger.debug('update realtime info %s %s',
                              weather_info.realtime.time, _time)
            weather_info.realtime = self.get_realtime(data)

    def update_aqi(self, weather_info, data):
        datestr = data['pub_time']
        _datetime = datetime.strptime(datestr, '%Y-%m-%d %H:%M')
        if weather_info.aqi.pub_date != _datetime:
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
            self.logger.error('no aqi data')
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
            _now_week = self.now_week()
            forecast = Forecast(
                            wind=data['fl%s' % str(i)],
                            wind_detail=data['wind%s' % str(i)],
                            temp=data['temp%s' % str(i)],
                            weather=data['weather%s' % str(i)],
                            week=self.get_week(_now_week, i)
                            )
            res.append(forecast)
        return res

    def now_week(self):
        _int = now_china().weekday()
        return self.int_to_week(_int)

    def get_week(self, week, offset):
        mod = (self.week_to_int(week) + offset) % 7
        return self.int_to_week(mod)

    def week_to_int(self, week):
        return {
                '星期一': 0,
                '星期二': 1,
                '星期三': 2,
                '星期四': 3,
                '星期五': 4,
                '星期六': 5,
                '星期日': 6
            }[week]

    def int_to_week(self, _int):
        return {
                0: '星期一',
                1: '星期二',
                2: '星期三',
                3: '星期四',
                4: '星期五',
                5: '星期六',
                6: '星期日'
            }[_int]
