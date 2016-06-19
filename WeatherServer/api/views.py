import json
from flask import Blueprint, request
from flask.views import MethodView
from flask.json import jsonify
from .models import Province, City, Country,\
                    RealTimeInfo, TodayInfo, AqiInfo,\
                    IndexInfo, Forecast, WeatherInfo
from WeatherServer.helpers import now_china

api = Blueprint('api', __name__, url_prefix='/api')

SUCCESS = 'success'
FAIL = 'fail'


@api.route('/weather')
def hello():
    return "Hello, welcome to keysona's weather"


@api.route('/weather/today/countryId/<country_id>', methods=['GET'])
def weather_for_id(country_id):
    country = Country.objects(location_id=country_id).first()
    return _weather_response(country)


@api.route('/weather/today/countryName/<country_name>', methods=['GET'])
def weather_for_name(country_name):
    country = Country.objects.get_or_404(name=country_name)
    return _weather_response(country)


def _weather_response(country):
    if country:
        if is_today(country.weather_infos[-1]):
            return make_weather_json(country)
        else:
            return make_fail_json('No today weather data!')
    else:
        return make_fail_json('No this country')


def make_weather_json(country):
    weather_info = country.weather_infos[-1]
    weather_json = json.loads(weather_info.to_json())

    # country name and status
    weather_json['country'] = country.name
    weather_json['status'] = SUCCESS
    weather_json['message'] = ''

    # Add a date and del datetime
    _datetime = weather_info['datetime']
    weather_json['date'] = '%s-%s-%s' % (_datetime.year,
                                         _datetime.month, _datetime.day)
    del weather_json['datetime']

    # change realtime.time
    if weather_info['realtime']:
        _time = weather_info['realtime']['time']
        weather_json['realtime']['time'] = '%s:%s' % (_time.hour,
                                                      _time.minute)

    # del aqi.pub_date and add aqi.time
    if weather_info['aqi']:
        _time = weather_info['aqi']['pub_date']
        weather_json['aqi']['time'] = '%s:%s' % (_time.hour,
                                                 _time.minute)
        del weather_json['aqi']['pub_date']

    return json.dumps(weather_json)


def make_fail_json(message):
    return json.dumps(dict(status=FAIL,
                           message=message))


def is_today(weather_info):
    ch = now_china()
    _datetime = weather_info.datetime
    return ch.year == _datetime.year and \
        ch.month == _datetime.month and \
        ch.day == _datetime.day
