def format_time(datetime):
    hour = str(datetime.hour)
    minute = str(datetime.minute)
    if len(minute) == 1:
        minute = '0' + minute
    return hour + ':' + minute


def get_image_name(weather):
    data = {'晴': 'img/sun.png',
            '雷': 'img/storm.png',
            '暴': 'img/rain_large.png',
            '大': 'img/rain_large.png',
            '雨': 'img/rain.png',
            '中': 'img/rain.png',
            '阵': 'img/rain.png',
            '云': 'img/clouds.png',
            '阴': 'img/clouds.png'}
    storm = ['雷']
    rain_large = ['爆', '大']
    rain = ['雨', '中', '阵']
    cloud = ['云', '阴']
    sun = ['晴']

    for word_set in [storm, rain_large, rain, cloud, sun]:
        for word in word_set:
            if word in weather:
                return '/static/' + data[word]
    return None


def get_aqi_type(aqi):
    aqi = int(aqi)
    if aqi <= 50:
        return '优'
    elif aqi <= 100:
        return '良'
    elif aqi <= 150:
        return '轻度污染'
    elif aqi <= '200':
        return '中度污染'
    elif aqi <= '300':
        return '重读污染'
    else:
        return '严重污染'

def get_aqi_tips(aqi):
    tips = {
        '优': '此时空气质量令人满意，基本无空气污染，各类人群可正常活动。',
        '良': '此时空气质量可接受，但某些污染物可能对极少数异常敏感人群健康有较弱影响，建议极少数异常敏感人群应减少户外活动。',
        '轻度污染': '此时，易感人群症状有轻度加剧，健康人群出现刺激症状。建议儿童、老年人及心脏病、呼吸系统疾病患者应减少长时间、高强度的户外锻炼。',
        '中度污染': '此时，进一步加剧易感人群症状，可能对健康人群心脏、呼吸系统有影响，建议疾病患者避免长时间、高强度的户外锻练，一般人群适量减少户外运动。',
        '重度污染': '此时，心脏病和肺病患者症状显著加剧，运动耐受力降低，健康人群普遍出现症状，建议儿童、老年人和心脏病、肺病患者应停留在室内，停止户外运动，一般人群减少户外运动。',
        '严重污染': '此时，健康人群运动耐受力降低，有明显强烈症状，提前出现某些疾病，建议儿童、老年人和病人应当留在室内，避免体力消耗，一般人群应避免户外活动。'
        }
    type = get_aqi_type(aqi)
    return tips[type]
