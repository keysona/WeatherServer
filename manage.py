from flask_script import Manager, Server, Shell
from WeatherServer.api import Province, City, Country, WeatherHistory
from WeatherServer import app
import json


def _make_context():
    return dict(Province=Province, City=City,
                Country=Country, WeatherHistory=WeatherHistory)

manager = Manager(app)
manager.add_command('runserver', Server(host='0.0.0.0', port='5000',
                                        use_debugger=True))
manager.add_command('shell', Shell(make_context=_make_context))


@manager.command
def make_json():
    provinces = []
    for province in Province.objects:
        province_json = make_province(province)
        provinces.append(province_json)
    res = dict(provinces=provinces)
    with open('locations.json', 'w') as f:
        f.write(json.dumps(res))


def make_province(province):
    province_json = json.loads(province.to_json())
    del province_json['_id']
    for city in province.cities:
        id = city.location_id
        province_json['cities'].append(make_city(city))
        province_json['cities'].remove(id)
    return province_json


def make_city(city):
    city_json = json.loads(city.to_json())
    del city_json['_id']
    for country in city.countries:
        id = country.location_id
        city_json['countries'].append(make_country(country))
        city_json['countries'].remove(id)
    return city_json


def make_country(country):
    country_json = json.loads(country.to_json())
    del country_json['_id']
    del country_json['weather_id']
    del country_json['weather_infos']
    return country_json


if __name__ == '__main__':
    manager.run()
