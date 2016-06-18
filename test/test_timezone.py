from datetime import datetime, timedelta
from . import now_china


def test_now_china():
    now = now_china()
    test_now = datetime.utcnow() + timedelta(hours=8)
    assert now.hour == test_now.hour and now.minute == now.minute
