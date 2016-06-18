from flask import Blueprint, request
from flask.views import MethodView
from flask.json import jsonify
from .models import Province, City, Country,\
                    RealTimeInfo, TodayInfo, AqiInfo,\
                    IndexInfo, Forecast, WeatherInfo

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


@api.route('/weather/countryId/<int:country_id>', methods=['GET'])
def weather_for_id(country_id):
    country = Country.objects.get_or_404(location_id=country_id)
    if country.weather_infos:
        return jsonify(
                    status=SUCCESS,
                    weather=country.weather_infos[-1],
                    city_name=country.name
                    )
    else:
        return jsonify(
                    status=FAIL,
                    message='No this country data!',
                )


@api.route('/weather/countryName/<country_name>', methods=['GET'])
def weather_for_name(country_name):
    country = Country.objects.get_or_404(name=country_name)
    print('{:%Y-%m-%d}'.format(country.weather_infos[-1].datetime))
    return jsonify(
                status=SUCCESS,
                weather=country.weather_infos[-1],
                city=country.name,
                date='{:%Y-%m-%d}'.format(country.weather_infos[-1].datetime),
            )
