from WeatherServer import db


class Province(db.Document):

    weather_id = db.StringField(verbose_name='id',
                                max_length=80,
                                required=True,
                                unique=True)

    ch = db.StringField(verbose_name='中文名',
                        max_length=30,
                        required=True)

    en = db.StringField(verbose_name='英文名',
                        max_length=30,
                        required=True)

    cities = db.ListField(db.ReferenceField('City'))

    def __unicode__(self):
        return '<省份:%s (%s)>' % (self.ch, self.weather_id)


class City(db.Document):

    weather_id = db.StringField(verbose_name='id',
                                max_length=80,
                                required=True,
                                unique=True)

    ch = db.StringField(verbose_name='中文名',
                        max_length=30,
                        required=True)

    en = db.StringField(verbose_name='英文名',
                        max_length=30,
                        required=True)

    countries = db.ListField(db.ReferenceField('Country'))

    def __unicode__(self):
        return '<城市:%s (%s)>' % (self.ch, self.weather_id)


class Country(db.Document):

    weather_id = db.StringField(verbose_name='id',
                                max_length=80,
                                required=True,
                                unique=True)

    ch = db.StringField(verbose_name='中文名',
                        max_length=30,
                        required=True)

    en = db.StringField(verbose_name='英文名',
                        max_length=30,
                        required=True)

    def __unicode__(self):
        return '<县级市:%s (%s)>' % (self.ch, self.weather_id)
