import os.path
import sys

dirname = os.path.dirname
sys.path.append(dirname(dirname(dirname(__file__))))

from WeatherServer.api import Province, City, Country,\
                RealTimeInfo, TodayInfo, AqiInfo,\
                IndexInfo, Forecast, WeatherInfo,\
                WeatherHistoryInfo, WeatherHistory
from WeatherServer.helpers import now_china
