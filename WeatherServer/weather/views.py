import IP
from flask import Blueprint, request, render_template, jsonify
from flask.views import MethodView
from WeatherServer.api import Province, City, Country,\
              RealTimeInfo, TodayInfo, AqiInfo,\
              IndexInfo, Forecast, WeatherInfo,\
              WeatherHistoryInfo, WeatherHistory,\
              make_weather_json

weather = Blueprint('weather', __name__, url_prefix='/weather')


class IndexView(MethodView):

    def get(self):
        ip = get_real_ip()
        locations = get_location(ip)
        if len(locations) == 3:
            country = get_country(locations[2])
            if not country:
                    return jsonify(message='No data!')
        if country.weather_infos:
            weather_info = country.weather_infos[-1]
            realtime = weather_info.realtime
            aqi = weather_info.aqi
            print(aqi.pub_date)
            return render_template('index.html',
                                   **{'ip': ip,
                                      'location': ' '.join(locations),
                                      'realtime': realtime,
                                      'aqi': aqi})

    def post(self):
        country_name = request.form.get('country_name')
        country = get_country(country_name)
        if country:
            return render_template('index.html')
        return render_template('index.html')

weather.add_url_rule('/', view_func=IndexView.as_view('index'))

# @weather.route('/', methods=['GET'])
# def index():
#     ip = get_real_ip()
#     locations = get_location(ip)
#     print(ip, locations)
#     # test
#     if len(locations) == 3:
#         country = get_country(locations[2])
#         if not country:
#                 return jsonify(message='No data!')
#     # return make_weather_json(country)
#     return render_template('index.html',
#                            **{'ip': ip, 'location': ' '.join(locations)})


def get_real_ip():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    return ip


def get_location(ip):
    location = IP.find(ip)
    # test
    location = '中国\t广东\t佛山'
    if '中国' in location:
        return location.split('\t')


def get_country(country_name):
    country = Country.objects(name=country_name).first()
    if country:
        return country
    else:
        city = City.objects(name=country_name).first()
        if city:
            return city.countries[0]
        return None
