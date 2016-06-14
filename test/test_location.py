import requests as req
import pytest
from test import Province, City, Country


def test_provinces():
    # <省份:香港 (32)>
    province = Province.objects(location_id='32').first()
    assert province['name'] == '香港',\
        'province location_id wrong/省份location_id出现 : %s' % r_province


def test_city():
    # <城市:白城 (0606)>
    location_id = '0606'
    name = '白城'
    city = City.objects(location_id=location_id).first()
    assert city['name'] == name,\
        "location_id wrong/location_id不匹配 : %s" % city

    # Is this city in its province?
    province = Province.objects(location_id=location_id[:2]).first()
    assert city in province.cities,\
        "%s not in %s" % (city, province.cities)

def test_country():
    pass



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

# def test_country_count(provinces):
#     t_country = 0
#     r_country = Country.objects.all().count()
#
#     for province in provinces:
#         for city in province['beans']:
#             t_country += len(city['beans'])
#     assert t_country == r_country,\
#         'country count wront/县级市数量出错'
