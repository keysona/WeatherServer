import requests as req
import pytest
from test import Province, City, Country


@pytest.fixture(scope="module")
def provinces():
    resp = req.get(url='http://3g.tianqi.cn/getAllCitys.do')
    return resp.json()


def test_provinces(provinces):
    t_province = provinces[0]
    r_province = Province.objects(weather_id=t_province['id']).first()
    assert t_province['en'] == r_province['en'],\
        'province weather_id wrong/省份weather_id出错'


def test_city(provinces):
    t_city = provinces[0]['beans'][0]
    r_city = City.objects(weather_id=t_city['id']).first()
    assert t_city['en'] == r_city['en'], "weather_id wrong/weather_id不匹配"


def test_country(provinces):
    t_country = provinces[0]['beans'][0]['beans'][0]
    r_country = Country.objects(weather_id=t_country['id']).first()
    assert t_country['en'] == r_country['en'],\
        'country weather_id wrong/县级市weather_id出错'


def test_provinces_count(provinces):

    assert len(provinces) == Province.objects.all().count(),\
                        "provinces count wrong/省份数量出错"


def test_city_count(provinces):
    sum_internet = 0

    for province in provinces:
        sum_internet += len(province['beans'])

    assert sum_internet == City.objects.all().count(),\
        "city count wront/城市数量出错"


def test_country_count(provinces):
    t_country = 0
    r_country = Country.objects.all().count()

    for province in provinces:
        for city in province['beans']:
            t_country += len(city['beans'])
    assert t_country == r_country,\
        'country count wront/县级市数量出错'
