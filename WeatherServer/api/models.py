from WeatherServer import db


class Province(db.Document):

    location_id = db.StringField(verbose_name='location_id',
                                 max_length=20,
                                 required=True,
                                 primary_key=True,
                                 unique=True)

    name = db.StringField(verbose_name='省份',
                          max_length=30,
                          required=True)

    cities = db.ListField(db.ReferenceField('City'))

    def __unicode__(self):
        return '<省份:%s (%s)>' % (self.name, self.location_id)


class City(db.Document):

    location_id = db.StringField(verbose_name='location_id',
                                 max_length=20,
                                 required=True,
                                 primary_key=True,
                                 unique=True)

    name = db.StringField(verbose_name='省份',
                          max_length=30,
                          required=True)

    countries = db.ListField(db.ReferenceField('Country'))

    def __unicode__(self):
        return '<城市:%s (%s)>' % (self.name, self.location_id)


class Country(db.Document):

    location_id = db.StringField(verbose_name='location_id',
                                 max_length=20,
                                 required=True,
                                 primary_key=True,
                                 unique=True)

    weather_id = db.StringField(verbose_name='weather_id',
                                max_length=80,
                                required=True,
                                unique=True)

    name = db.StringField(verbose_name='中文名',
                          max_length=30,
                          required=True)

    weather_infos = db.EmbeddedDocumentListField('WeatherInfo')

    def __unicode__(self):
        return '<名称:%s id-%s weather-id-%s>' % \
            (self.name, self.location_id, self.weather_id)


class RealTimeInfo(db.EmbeddedDocument):

    humidity = db.StringField(verbose_name='湿度',
                              max_length=10)

    wind_direction = db.StringField(verbose_name='风向',
                                    max_length=10)

    wind_speed = db.StringField(verbose_name='风力',
                                max_length=10)

    temp = db.StringField(verbose_name='温度',
                          max_length=10)

    time = db.StringField(verbose_name='时间',
                          max_length=10)

    weather = db.StringField(verbose_name='天气')


class TodayInfo(db.EmbeddedDocument):

    humidity_max = db.IntField(verbose_name='最高湿度')
    humidity_min = db.IntField(verbose_name='最低湿度')

    temp_max = db.IntField(verbose_name='最高温度')
    temp_min = db.IntField(verbose_name='最低温度')

    weather_start = db.StringField(verbose_name='开始天气',
                                   max_length=30)
    weather_end = db.StringField(verbose_name='结束天气',
                                 max_length=30)

    wind_direction_start = db.StringField(verbose_name='开始风向',
                                          max_length=30)
    wind_direction_end = db.StringField(verbose_name='结束风向',
                                        max_length=30)

    wind_max = db.IntField(verbose_name='最大风力')
    wind_min = db.IntField(verbose_name='最小风力')


class AqiInfo(db.EmbeddedDocument):

    pub_date = db.DateTimeField(verbose_name='更新日期')

    aqi = db.StringField(verbose_name='空气质量',
                         max_length=20)

    pm25 = db.StringField(verbose_name='pm2.5',
                          max_length=20)

    pm10 = db.StringField(verbose_name='pm10',
                          max_length=20)

    so2 = db.StringField(verbose_name='so2',
                         max_length=20)

    no2 = db.StringField(verbose_name='no2',
                         max_length=20)

    source = db.StringField(verbose_name='来源',
                            max_length=50)

    spot = db.StringField(verbose_name='地点',
                          max_length=50)

    def __unicode__(self):
        return '空气质量: %s' % self.aqi


class IndexInfo(db.EmbeddedDocument):

    code = db.StringField(verbose_name='code',
                          max_length=10)

    details = db.StringField(verbose_name='细节',
                             max_length=300)

    index = db.StringField(verbose_name='指数',
                           max_length=20)

    name = db.StringField(verbose_name='name',
                          max_length=20)

    def __unicode__(self):
        return '%s: %s' % (self.name, self.index)


class Forecast(db.EmbeddedDocument):

    wind = db.StringField(verbose_name='风力',
                          max_length=10)

    wind_detail = db.StringField(verbose_name='风力细节',
                                 max_length=20)

    temp = db.StringField(verbose_name='温度',
                          max_length=20)

    weather = db.StringField(verbose_name='天气描述',
                             max_length=20)

    week = db.StringField(verbose_name='星期几')

    def __unicode__(self):
        return '%s %s' % (self.week, self.weather)


class WeatherInfo(db.EmbeddedDocument):

    date = db.DateTimeField(verbose_name='datetime',
                            required=True,
                            unique=True)

    week = db.StringField(verbose_name='星期几')

    today = db.EmbeddedDocumentField('TodayInfo',
                                     verbose_name='今天天气')

    realtime = db.EmbeddedDocumentField('RealTimeInfo',
                                        verbose_name='实时天气')

    aqi = db.EmbeddedDocumentField('AqiInfo',
                                   verbose_name='空气指数')

    index = db.EmbeddedDocumentListField('IndexInfo',
                                         verbose_name='指数信息')

    forecast = db.EmbeddedDocumentListField('Forecast',
                                            verbose_name='预报信息')

    def __unicode__(self):
        date = self.date
        return '%s-%s-%s %s' % (date.year, date.month,
                                date.day, self,)
