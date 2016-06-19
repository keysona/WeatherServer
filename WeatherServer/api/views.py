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

@api.errorhandler(404)
def page_not_found(e):
        return jsonify(
                status=FAIL
            )

class ProvinceView(MethodView):

    def get(self, location_id):
        if location_id is None:
            return self.province_list()
        else:
            return self.province_single(location_id)

    def province_list(self):
        provinces = []
        for province in Province.objects:
            provinces.append(province)
        return jsonify(
                status=SUCCESS,
                provinces=provinces
            )

    def province_single(self, location_id):
        province = Province.objects.get_or_404(location_id=location_id)
        return jsonify(
                status=SUCCESS,
                province=province
            )

class CityView(MethodView):

    def get(self, location_id):
        if location_id is None:
            return self.city_list()
        else:
            return self.city_single(location_id)

    def city_list(self):
       cities = []
       for city in City.objects:
           cities.append(city)
       return jsonify(
                status=SUCCESS,
                cities=cities
            )

    def city_single(self, location_id):
        city = City.objects.get_or_404(location_id=location_id)[0]
        return jsonify(
                status=SUCCESS,
                city=city
           )

class CountryView(MethodView):

    def get(self, location_id):
        if location_id is None:
            return self.country_list()
        else:
            return self.country_single(location_id)

    def country_list(self):
        countries = []
        for country in Country.objects:
            countries.append(country)
        return jsonify(
                status=SUCCESS,
                countries=countries
            )

    def country_single(slef, location_id):
        if location_id.isdigit():
            country = Country.objects.get_or_404(location_id=location_id)
        else:
            country = Country.objects.get_or_404(name=location_id)
        print(location_id)
        return jsonify(
                status=SUCCESS,
                country=country
            )

# province view
province_view = ProvinceView.as_view('province_api')
api.add_url_rule('/province/', view_func=province_view,
                 defaults={'location_id': None},
                 methods=['GET'])
api.add_url_rule('/province/<location_id>', view_func=province_view,
                 methods=['GET'])

# city view
city_view = CityView.as_view('city_api')
api.add_url_rule('/city/', view_func=city_view,
                 defaults={'location_id': None},
                 methods=['GET'])
api.add_url_rule('/city/<location_id>', view_func=city_view,
                 methods=['GET'])

# country view
country_view = CountryView.as_view('country_api')
api.add_url_rule('/country/', view_func=country_view,
                 defaults={'location_id': None},
                 methods=['GET'])
api.add_url_rule('/country/<location_id>', view_func=country_view,
                 methods=['GET'])


@api.route('/weather')
def hello():
    return 'hello'


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
