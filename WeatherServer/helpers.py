from datetime import datetime, timezone, timedelta

UTC_TO_CHINA = timezone(timedelta(hours=8))


def now_china():
    return datetime.utcnow() + timedelta(hours=8)
