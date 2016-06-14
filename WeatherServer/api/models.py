from WeatherServer import db


class Province(db.Document):

    location_id = db.StringField(verbose_name='location_id',
                                 max_length=20,
                                 required=True,
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
                                 unique=True)

    name = db.StringField(verbose_name='省份',
                          max_length=30,
                          required=True)

    countries = db.ListField(db.ReferenceField('Country'))

    def __unicode__(self):
        return '<城市:%s (%s)>' % (self.name, self.id)


class Country(db.Document):

    location_id = db.StringField(verbose_name='location_id',
                                 max_length=20,
                                 required=True,
                                 unique=True)

    weather_id = db.StringField(verbose_name='weather_id',
                                max_length=80,
                                required=True,
                                unique=True)

    name = db.StringField(verbose_name='中文名',
                          max_length=30,
                          required=True)

    def __unicode__(self):
        return '<名称:%s weather-id(%s)>' % (self.name, self.weather_id)
