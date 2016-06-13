from WeatherServer import db


class Province(db.Document):

    id = db.StringField(verbose_name='id',
                        max_length=80,
                        required=True,
                        unique=True)

    name = db.StringField(verbose_name='省份名',
                          max_length=80,
                          required=True,
                          unique=True)

    cities = db.ListField(db.ReferenceField('City'))


class City(db.Document):

    id = db.StringField(verbose_name='id',
                        max_length=80,
                        required=True,
                        unique=True)

    name = db.StringField(verbose_name='城市名',
                          max_length=80,
                          required=True,
                          unique=True)

    countries = db.ListField(db.ReferenceField('Country'))


class Country(db.Document):

    id = db.StringField(verbose_name='id',
                        max_length=80,
                        required=True,
                        unique=True)

    weather_id = db.StringField(verbose_name='weather_id',
                                max_length=80,
                                required=True,
                                unique=True)

    name = db.StringField(verbose_name='县级名',
                          max_length=80,
                          required=True,
                          unique=True)
