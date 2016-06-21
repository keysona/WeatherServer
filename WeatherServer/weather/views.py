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
        country = None
        if isinstance(locations, list) and len(locations) == 3:
            country = get_country(locations[2])
            if not country:
                    return jsonify(message='No data!')
        if country and country.weather_infos:
            weather_info = country.weather_infos[-1]
            index_context = make_index_context(weather_info)
            index_context['ip'] = ip
            index_context['location'] = ' '.join(locations)
            return render_template('index.html', **index_context)
        return render_template('index.html', **{
                                                'ip': ip,
                                                'location': locations
                                            })

    def post(self):
        country_name = request.form.get('country_name')
        country = get_country(country_name)
        if country and country.weather_infos:
            weather = country.weather_infos[-1]
            index_context = make_index_context(weather)
            index_context['location'] = country.name
            return render_template('index.html', **index_context)
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
    #location = '中国\t广东\t佛山'
    if '中国' in location:
        return location.split('\t')
    return location


def get_country(country_name):
    country = Country.objects(name=country_name).first()
    if country:
        return country
    else:
        city = City.objects(name=country_name).first()
        if city:
            return city.countries[0]
        return None


def make_index_context(weather):
    realtime = weather.realtime
    aqi = weather.aqi
    indexs = weather.index
    forecasts = None
    if weather.forecast:
        forecasts = weather.forecast[:5]
    return dict(realtime=realtime, aqi=aqi,
                indexs=indexs, forecasts=forecasts)
