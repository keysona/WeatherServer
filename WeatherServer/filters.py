def format_time(datetime):
    return "%s:%s" % (datetime.hour, datetime.minute)


def get_image_name(weather):
    data = {'晴': 'img/sun.png',
            '雷阵雨': 'img/storm.png',
            '暴雨': 'img/rain_large.png',
            '大暴雨': 'img/rain_large.png',
            '大雨': 'img/rain_large.png',
            '小雨': 'img/rain.png',
            '多云': 'img/clouds.png',
            '阴': 'img/clouds.png',
            '中雨': 'img/rain.png',
            '阵雨': 'img/rain.png'}
    return '/static/' + data[weather]
