
import requests as req
import pytest
from test import Province, City, Country


def test_provinces():
    # <省份:香港 (32)>
    province = Province.objects(location_id='32').first()
    assert province['name'] == '香港',\
        'province location_id wrong/省份location_id出现 : %s' % province


def test_city():
    # <城市:白城 (0606)>
    location_id = '0606'
    name = '白城'
    city = City.objects(location_id=location_id).first()
    assert city['name'] == name,\
        'name wrong/名称不匹配 : %s != %s' % (city, name)

    # Is this city in its province?
    province = Province.objects(location_id=location_id[:2]).first()
    assert city in province.cities,\
        '%s not in %s' % (city, province.cities)


def test_country():
    # <名称:长春 id-060101 weather-id-101060101>
    location_id = '060101'
    name = '长春'
    country = Country.objects(location_id=location_id).first()
    assert country['name'] == name,\
        'name wrong/名称不匹配 : %s != %s' % (city, name)

    # Is this country in its city?
    city = City.objects(location_id=location_id[:4]).first()
    assert country in city.countries,\
        '%s not in %s' % (country, city.countries)


def test_provinces_count():
    # all province count 34
    assert Province.objects.all().count() == 34,\
                        "provinces count wrong/省份数量出错"


def test_city_count():
    TOTAL = 381
    total = 0

    for province in Province.objects:
        total += len(province['cities'])

    assert total == TOTAL,\
        'cities count wront/城市数量出错: (total)%d != (TOTAL)%d' % (total, TOTAL)


def test_country_count():
    TOTAL = 2501
    total = 0

    for city in City.objects:
        total += len(city['countries'])

    assert total == TOTAL,\
        'countries count wront/城市数量出错: (total)%d != (TOTAL)%d' % (total, TOTAL)
